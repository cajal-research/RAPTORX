import os

from dotenv import load_dotenv


def setup_openai_api_key():
    load_dotenv()
    os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")
