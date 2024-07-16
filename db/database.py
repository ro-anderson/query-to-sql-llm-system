from sqlalchemy import create_engine, inspect
from langchain_community.utilities import SQLDatabase
from config.settings import settings

class Database:
  def __init__(self):
      self.db_uri = f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}/{settings.DB_NAME}"
      self.engine = create_engine(self.db_uri)
      self.db = SQLDatabase(self.engine)

  def get_table_info(self) -> str:
      inspector = inspect(self.engine)
      tables = inspector.get_table_names()
      table_info = []
      for table in tables:
          columns = inspector.get_columns(table)
          column_info = ", ".join([f"{col['name']} ({col['type']})" for col in columns])
          table_info.append(f"{table}: {column_info}")
      return "\n".join(table_info)

database = Database()