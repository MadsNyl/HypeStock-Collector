import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

SYMBOL_LOOKUP_API = os.environ.get("SYMBOL_LOOKUP_API")