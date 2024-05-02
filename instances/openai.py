from openai import AsyncOpenAI
from environ import env_collection

client = AsyncOpenAI(
    api_key=env_collection["OPENAI_KEY"]
)