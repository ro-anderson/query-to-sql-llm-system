import re
from io import StringIO
import sys

def clean_ansi(text):
  ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
  return ansi_escape.sub('', text)

def capture_output(func):
  def wrapper(*args, **kwargs):
      old_stdout = sys.stdout
      sys.stdout = StringIO()
      try:
          result = func(*args, **kwargs)
          output = sys.stdout.getvalue()
      finally:
          sys.stdout = old_stdout
      return result, output
  return wrapper

def get_schema_info_from_file(file_path) -> str:
  with open(file_path, 'r') as file:
      return file.read()