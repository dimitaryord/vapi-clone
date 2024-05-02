import io
from instances.openai import client
from fastapi import HTTPException
import base64


async def stt(audio_data, model="whisper-1"):
    try:
        transcription = await client.audio.transcriptions.create(
            model=model,
            file=('audio.wav', audio_data, 'audio/wav'),
            response_format="text",
            language="en"
        )
        return transcription

    except Exception as e:
        print(e)
        raise HTTPException(status_code=501, detail=e)