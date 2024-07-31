from fastapi import APIRouter, File, UploadFile, HTTPException
from app.models.transcription_response import TranscriptionResponse, LLMResponse
from app.services.clova_services import transcribe_audio_file, transcribe_audio_file_new, hyperclova_chat, hyperclova_chat_exp
from app.services.llm_service import powerful_llm_chat, new_llm_chat
from app.services.naver_speech import make_tts
import io
from fastapi.responses import FileResponse, StreamingResponse

router = APIRouter()
messages = []
"""
        온천칼국수
        직화쭈꾸미
        물총조개탕
        수육
        만두
"""
menu_str_to_ids = {"온천칼국수" : 1, "직화쭈꾸미" : 2, "물총조개탕" : 3, "수육" : 4, "만두" : 5}
ids_to_menu_str = {1 : "온천칼국수", 2 : "직화쭈꾸미", 3 : "물총조개탕", 4 : "수육", 5 : "만두"}


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
        if (transcription.strip() == ""):
            return TranscriptionResponse(text="음성인식에 실패했습니다. 다시 시도해주세요.")
        # print(transcription)
        answer = await hyperclova_chat(transcription)
        
        # print(answer)
        return TranscriptionResponse(text=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/initialize_messages", response_model=TranscriptionResponse)
async def initialize_messages():
    global messages
    messages = new_llm_chat(messages)
    return TranscriptionResponse(text="메시지 초기화 완료")
             
@router.post("/transcribe_and_ask_to_powerful_llm", response_model=TranscriptionResponse)
async def chat_with_powerful_llm(file: UploadFile = File(...)):
    try:
        transcription = await transcribe_audio_file_new(file)
        if (transcription.strip() == ""):
            return TranscriptionResponse(text="음성인식에 실패했습니다. 다시 시도해주세요.")
        # print(transcription)
        answer = await powerful_llm_chat(transcription, messages, menu_str_to_ids, ids_to_menu_str)
        response = LLMResponse(llm_text=answer["llm_text"], llm_audio_path=answer["llm_audio_path"], now_menu_list=answer["now_menu_list"], order_num=answer["order_num"], state=answer["state"], basket=answer["basket"], emotion=answer["emotion"], emotion_degree=answer["emotion_degree"])
        return response
        
        # return TranscriptionResponse(text=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/ask_to_powerful_llm", response_model=TranscriptionResponse)
async def text_with_powerful_llm(transcription: str):
    
    try:
        answer = await powerful_llm_chat(transcription, messages, menu_str_to_ids, ids_to_menu_str)
        response = LLMResponse(llm_text=answer["llm_text"], llm_audio_path=answer["llm_audio_path"], now_menu_list=answer["now_menu_list"], order_num=answer["order_num"], state=answer["state"], basket=answer["basket"], emotion=answer["emotion"], emotion_degree=answer["emotion_degree"])
        return response#make_tts(response.llm_text, output_file=response.llm_audio_path)
        # return make_tts(response.llm_text, output_file=response.llm_audio_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/transcribe_and_ask_exp", response_model=TranscriptionResponse)
async def chat_with_llm_exp(file: UploadFile = File(...)):
    try:
        transcription = await transcribe_audio_file_new(file)
        if (transcription.strip() == ""):
            return TranscriptionResponse(text="음성인식에 실패했습니다. 다시 시도해주세요.")
        # print(transcription)
        answer = await hyperclova_chat(transcription)
        
        # print(answer)
        return TranscriptionResponse(text=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/tts")
async def tts(text: str):
    try:
        data=make_tts(text)
        # save the audio file
        path= "tts.mp3"
        with open(path, "wb") as f:
            f.write(data)
        return FileResponse(path, media_type="audio/mpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))