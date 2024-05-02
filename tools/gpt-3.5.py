from instances.openai import client
from openai import AsyncAssistantEventHandler
from environ import env_collection

def process_with_gpt(input, on_done, on_use_vision, on_delta_text):
    pass