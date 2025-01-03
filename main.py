from fastapi import FastAPI, File, UploadFile, HTTPException, Request, Header
from fastapi.responses import JSONResponse, StreamingResponse
from contextlib import asynccontextmanager
from tools.gpt import process_with_gpt
from environ import env_collection
from tools.whisper import stt
from tools.tts import tts
from redis_client import (
    get_redis,
    close_redis,
    create,
    get,
    update,
    clear,
    delete
)
import uuid
import io

app = FastAPI()

@asynccontextmanager
async def lifespan():
    await get_redis()
    yield
    await close_redis()

@app.middleware("http")
async def auth_key_middleware(request: Request, call_next):
    auth_key = request.headers.get("Authorization-Key")
    if not auth_key or auth_key != env_collection["AUTH_KEY"]:
        raise HTTPException(status_code=401, detail="Not authorized")

    response = await call_next(request)
    return response


@app.get("/audio/session/create")
async def create_audio_session():
    try:
        session_id = str(uuid.uuid4())
        await create(session_id, '')
        return JSONResponse(
            content={
                "message": "Session created successfully",
                "session_id": session_id,
            },
            status_code=201,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/audio/session/add")
async def add_audio_to_session(
    audio_data: UploadFile = File(...),
    session_id: str = Header(..., alias="Session-Id"),
):
    try:
        audio_bytes = await audio_data.read()
        audio_buffer = io.BytesIO(audio_bytes)
        user_query = await stt(audio_data=audio_buffer)
        print(f"Current Text: {user_query}")

        await update(session_id, user_query)

        return JSONResponse(
            content={"message": "Audio chunk added to session"}, status_code=200
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/audio/session/delete")
async def delete_audio_session(session_id: str = Header(..., alias="Session-Id")):
    try:
        await delete(session_id)
        return JSONResponse(
            content={"message": "Session deleted successfully"}, status_code=200
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


async def process_query_to_audio(query):
    async for sentence in process_with_gpt(input=query):
        async for audio_chunk in tts(input_text=sentence):
            yield audio_chunk


@app.get("/voice/assistant/session/v0.1")
async def run_model_with_session(session_id: str = Header(..., alias="Session-Id")):
    try:
        user_query = await get(session_id)
        await clear(session_id)

        return StreamingResponse(
            process_query_to_audio(query=user_query), media_type="audio/opus"
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@app.post("/voice/assistant/file/v0.1")
async def run_model_with_file(audio: UploadFile = File(...)):
    if not audio.filename.endswith(".wav"):
        raise HTTPException(
            status_code=400, detail="Invalid file format. Please upload a .wav file."
        )

    try:
        audio_data = io.BytesIO(await audio.read())
        audio_data.seek(0)
        user_query = await stt(audio_data=audio_data)
        audio_data.close()

        return StreamingResponse(
            process_query_to_audio(query=user_query), media_type="audio/opus"
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
