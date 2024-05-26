from instances.openai import client
from environ import env_collection
import re

def is_complete_sentence(string):
    return re.search(r'[.?!](?=\s|$)', string) is not None

thread_id=''

async def process_with_gpt(input):
    global thread_id
    if len(thread_id) == 0:
        thread = await client.beta.threads.create()
        await client.beta.threads.messages.create(
            thread_id=thread.id, content=input, role="user"
        )
        thread_id = thread.id
    else:
        await client.beta.threads.messages.create(
            thread_id=thread_id, content=input, role="user"
        )

    buffer = ''

    try:
        async with client.beta.threads.runs.stream(
            thread_id=thread_id,
            assistant_id=env_collection["ASSISTANT_ID"],
        ) as stream:
            async for event in stream:
                if event.event == "thread.message.delta" and event.data.delta.content:
                    buffer += event.data.delta.content[0].text.value

                    while is_complete_sentence(buffer):
                        end_index = re.search(r'[.!?](\s|$)', buffer).end()
                        sentence = buffer[:end_index].strip()
                        buffer = buffer[end_index:]
                        print(sentence)

                        yield sentence + "\n"
    except Exception as e:
        print(f"Error processing stream: {e}")
                

