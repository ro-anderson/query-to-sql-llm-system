from utils.helpers import clean_ansi, get_schema_info_from_file
import os

def test_clean_ansi():
  ansi_string = "\033[31mThis is red\033[0m"
  cleaned_string = clean_ansi(ansi_string)
  assert cleaned_string == "This is red"

def test_get_schema_info_from_file():
  # Create a temporary file for testing
  test_file_path = "test_schema.txt"
  test_content = "This is a test schema"
  with open(test_file_path, "w") as f:
      f.write(test_content)
  
  # Test the function
  schema_info = get_schema_info_from_file(test_file_path)
  assert schema_info == test_content
  
  # Clean up
  os.remove(test_file_path)