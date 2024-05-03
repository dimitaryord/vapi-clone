from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from tools.whisper import stt
from tools.gpt import process_with_gpt_and_stream_audio
import io

app = FastAPI()

@app.post("/voice/assistant/v0.1")
async def receive_audio(audio: UploadFile = File(...)):
    if not audio.filename.endswith('.wav'):
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload a .wav file.")
    
    try:
        audio_data = io.BytesIO(await audio.read())
        audio_data.seek(0)
        user_query = await stt(audio_data=audio_data)
        audio_data.close()

        return StreamingResponse(process_with_gpt_and_stream_audio(input=user_query), media_type='audio/opus')
    
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
