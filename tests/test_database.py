import pytest
from db.database import Database

@pytest.fixture
def database():
  return Database()

def test_get_table_info(database):
  table_info = database.get_table_info()
  assert isinstance(table_info, str)
  assert len(table_info) > 0
  assert ":" in table_info  # Assuming the format is "table_name: column1, column2, ..."