import pytest
from services.langchain_service import LangchainService

@pytest.fixture
def langchain_service():
  return LangchainService()

def test_get_sql_query(langchain_service):
  question = "What is the total value of all sales made per year?"
  sql_query, sql_result, answer = langchain_service.get_sql_query(question)
  
  assert sql_query is not None
  assert "SELECT" in sql_query.upper()
  assert "FROM" in sql_query.upper()
  assert sql_result is not None
  assert answer is not None

def test_invalid_question(langchain_service):
  question = "This is not a valid SQL question"
  sql_query, sql_result, answer = langchain_service.get_sql_query(question)
  
  assert "An error occurred" in answer