import os
from dotenv import load_dotenv

load_dotenv()

env_collection = {
    "OPENAI_KEY": os.environ.get("OPENAI_KEY"),
    "ASSISTANT_ID": os.environ.get("ASSISTANT_ID"),
    "AUTH_KEY": os.environ.get("AUTH_KEY"),
    "REDIS_URL": os.environ.get("REDIS_URL"),
}