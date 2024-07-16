import os
import re
from io import StringIO
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain.prompts.prompt import PromptTemplate

# Load environment variables
load_dotenv()

# Set your OpenAI API key
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Set up database connection
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")

# Create database connection string
db_uri = f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"

# Connect to the database
engine = create_engine(db_uri)
db = SQLDatabase(engine)

# Initialize OpenAI language model
llm = ChatOpenAI(temperature=0, verbose=True)

# Custom prompt template with Few-Shot CoT
_DEFAULT_TEMPLATE = """Given an input question, first create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.

Use the following format:

Question: "Question here"
SQLQuery: "SQL Query to run"
SQLResult: "Result of the SQLQuery"
Answer: "Final answer here"

Here are some example of step-by-step reasoning for similar tasks:

Example 1:
Question: "What is the total value of all sales made per year?"
SQLQuery: "SELECT YEAR(o.order_date) AS year, SUM(od.quantity * p.list_price) AS total_sales_value FROM order_details od JOIN products p ON od.product_id = p.id JOIN orders o ON od.order_id = o.id GROUP BY YEAR(o.order_date) ORDER BY year;"
SQLResult: [(2006, 68137.00)]
Answer: "The total value of all sales made per year is 68137.00 in 2006."

Only use the following tables and columns and schema information:
{table_info}

Question: {input}"""

PROMPT = PromptTemplate(
  input_variables=["input", "dialect", "table_info"],
  template=_DEFAULT_TEMPLATE,
)

def clean_ansi(text):
  ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
  return ansi_escape.sub('', text)


def capture_output(func):
  def wrapper(*args, **kwargs):
      # Capture stdout
      old_stdout = sys.stdout
      sys.stdout = StringIO()
      
      try:
          result = func(*args, **kwargs)
          output = sys.stdout.getvalue()
      finally:
          # Restore stdout
          sys.stdout = old_stdout
      
      return result, output
  return wrapper

@capture_output
def invoke_chain(inputs):
  return db_chain.invoke(**inputs)


# Fetch detailed schema information from GraphML file
def get_schema_info_from_file(file_path) -> str:
  with open(file_path, 'r') as file:
      return file.read()

# Fetch detailed table and column information from the database
def get_table_info(engine) -> str:
  inspector = inspect(engine)
  tables = inspector.get_table_names()
  table_info = []
  for table in tables:
      columns = inspector.get_columns(table)
      column_info = ", ".join([f"{col['name']} ({col['type']})" for col in columns])
      table_info.append(f"{table}: {column_info}")
  return "\n".join(table_info)

# Path to the GraphML file
graphml_file_path = os.path.join(os.path.dirname(__file__), 'northwind.txt')
schema_info = get_schema_info_from_file(graphml_file_path)
table_info = get_table_info(engine) + "\n" + schema_info

# Create the SQLDatabaseChain
db_chain = SQLDatabaseChain.from_llm(llm, db, prompt=PROMPT, verbose=True)

def get_sql_query(question: str):
  try:
      inputs = {
          "input": question,
          "dialect": "mysql",
          "table_info": table_info
      }
      result, output = invoke_chain(inputs)
      
      # Extract SQL query and result from the captured output
      sql_query_match = re.search(r'SQLQuery:(.*?)SQLResult:', output, re.DOTALL)
      sql_result_match = re.search(r'SQLResult:(.*?)Answer:', output, re.DOTALL)
      
      if sql_query_match and sql_result_match:
          sql_query = clean_ansi(sql_query_match.group(1).strip())
          sql_result = clean_ansi(sql_result_match.group(1).strip())
      else:
          sql_query = "N/A"
          sql_result = "N/A"
      
      answer = result['result'] if isinstance(result, dict) and 'result' in result else str(result)
      
      return sql_query, sql_result, answer
  except Exception as e:
      return None, None, f"An error occurred: {str(e)}"