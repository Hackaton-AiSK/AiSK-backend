from fastapi import APIRouter, File, UploadFile, HTTPException
from app.models.transcription_response import TranscriptionResponse
from app.services.clova_services import transcribe_audio_file, transcribe_audio_file_new, hyperclova_chat

router = APIRouter()

@router.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe_audio(file: UploadFile = File(...)):
    try:
        transcription = await transcribe_audio_file(file)
        return TranscriptionResponse(text=transcription)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
async def root():
    return {"message": "Hello World"}

@router.post("/transcribe2", response_model=TranscriptionResponse)
async def transcribe_audio(file: UploadFile = File(...)):
    try:
        transcription = await transcribe_audio_file_new(file)
        return TranscriptionResponse(text=transcription)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/transcribe_and_ask", response_model=TranscriptionResponse)
async def chat_with_llm(file: UploadFile = File(...)):
    try:
        transcription = await transcribe_audio_file_new(file)
        # print(transcription)
        answer = await hyperclova_chat(transcription)
        # print(answer)
        return TranscriptionResponse(text=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))