from instances.openai import client
from fastapi import HTTPException


async def stt(audio_data, format="wav", model="whisper-1"):
    try:
        audio_data.seek(0)
        transcription = await client.audio.transcriptions.create(
            model=model,
            file=(f"audio.{format}", audio_data, f"audio/{format}"),
            response_format="text",
            language="en"
        )
        return transcription

    except Exception as e:
        print(f"Error during STT: {e}")
        raise HTTPException(status_code=501, detail="STT processing failed.")
