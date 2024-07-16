from langchain.prompts.prompt import PromptTemplate

SQL_PROMPT_TEMPLATE = """Given an input question, first create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.

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

SQL_PROMPT = PromptTemplate(
  input_variables=["input", "dialect", "table_info"],
  template=SQL_PROMPT_TEMPLATE,
)