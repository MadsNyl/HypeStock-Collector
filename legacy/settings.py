import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

DOWNLOAD_API = os.environ.get("DOWNLOAD_API")
DOWNLOAD_PERIOD = os.environ.get("DOWNLOAD_PERIOD")
USER_AGENT = os.environ.get("USER_AGENT")