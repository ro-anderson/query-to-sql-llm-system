import os
import re
from langchain_openai import ChatOpenAI
from langchain_experimental.sql import SQLDatabaseChain
from db.database import database
from prompts.sql_prompts import SQL_PROMPT
from utils.helpers import capture_output, clean_ansi, get_schema_info_from_file
from config.settings import settings

class LangchainService:
    def __init__(self):
      self.llm = ChatOpenAI(
          model=settings.OPENAI_MODEL,
          temperature=settings.OPENAI_TEMPERATURE,
          verbose=settings.OPENAI_VERBOSE,
          api_key=settings.OPENAI_API_KEY
      )
      self.db_chain = SQLDatabaseChain.from_llm(self.llm, database.db, prompt=SQL_PROMPT, verbose=settings.OPENAI_VERBOSE)

    @capture_output
    def invoke_chain(self, inputs):
        return self.db_chain.invoke(**inputs)

    def get_sql_query(self, question: str):
        try:
            schema_info = get_schema_info_from_file(os.path.join(settings.BASE_DIR, 'data', 'northwind.txt'))
            table_info = database.get_table_info() + "\n" + schema_info

            inputs = {
                "input": question,
                "dialect": "mysql",
                "table_info": table_info
            }
            result, output = self.invoke_chain(inputs)
            
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

langchain_service = LangchainService()