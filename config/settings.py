import os
from dotenv import load_dotenv

# Get the base directory of the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

load_dotenv(os.path.join(BASE_DIR, '.env'))

class Settings:
  BASE_DIR = BASE_DIR
  OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
  DB_USER = os.getenv("DB_USER")
  DB_PASSWORD = os.getenv("DB_PASSWORD")
  DB_HOST = os.getenv("DB_HOST")
  DB_NAME = os.getenv("DB_NAME")

  # ChatOpenAI settings
  OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo-0125")
  OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0"))
  OPENAI_VERBOSE = os.getenv("OPENAI_VERBOSE", "True").lower() == "true"

settings = Settings()