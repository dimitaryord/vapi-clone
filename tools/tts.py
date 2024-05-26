from fastapi import HTTPException
from instances.openai import client

async def tts(input_text: str, model="tts-1", voice="nova"):
    try:
        is_new_sentence = b'\x01'
        async with client.audio.speech.with_streaming_response.create(
            model=model, voice=voice, input=input_text, response_format="opus",
        ) as response:
            if response.status_code == 200:
                    async for chunk in response.iter_bytes(chunk_size=1024):
                        print(len(is_new_sentence + chunk))
                        yield is_new_sentence + chunk
                        if is_new_sentence == b'\x01':
                            is_new_sentence = b'\x00'
            else:
                raise HTTPException(
                    status_code=response.status_code, detail="TTS request failed"
                )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
