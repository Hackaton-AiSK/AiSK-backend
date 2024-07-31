from fastapi import APIRouter, File, UploadFile, HTTPException
from app.models.transcription_response import TranscriptionResponse, LLMResponse, InitialResponse
from app.services.clova_services import transcribe_audio_file, transcribe_audio_file_new, hyperclova_chat, hyperclova_chat_exp
from app.services.llm_service import powerful_llm_chat, new_llm_chat
from app.services.naver_speech import make_tts
import io
from fastapi.responses import FileResponse, StreamingResponse
import sqlite3
import math

router = APIRouter()
messages = []
"""
        온천칼국수
        직화쭈꾸미
        물총조개탕
        수육
        만두
"""
menu_str_to_ids = dict()
ids_to_menu_str = dict()
menu_items_frontend = []


@router.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    print(file)
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

@router.post("/initialize_messages", response_model=InitialResponse)
# get restaurant_id
async def initialize_messages(restaurant_id: int):
    global messages, menu_str_to_ids, ids_to_menu_str, menu_items_frontend
    messages = []
    menu_str_to_ids = dict()
    menu_items_frontend = []
    ids_to_menu_str = dict()
    messages, menu_str_to_ids, ids_to_menu_str, menu_items_frontend = new_llm_chat(messages, restaurant_id)
    return InitialResponse(menu_list=menu_items_frontend)
             
@router.post("/transcribe_and_ask_to_powerful_llm", response_model=LLMResponse)
async def chat_with_powerful_llm(file: UploadFile = File(...)):
    try:
        transcription = await transcribe_audio_file(file)
        if (transcription.strip() == ""):
            return TranscriptionResponse(text="음성인식에 실패했습니다. 다시 시도해주세요.")
        # print(transcription)
        answer = await powerful_llm_chat(transcription, messages, menu_str_to_ids, ids_to_menu_str)
        response = LLMResponse(llm_text=answer["llm_text"], llm_audio_path=answer["llm_audio_path"], now_menu_list=answer["now_menu_list"], order_num=answer["order_num"], state=answer["state"], basket=answer["basket"], emotion=answer["emotion"], emotion_degree=answer["emotion_degree"])
        return response
        
        # return TranscriptionResponse(text=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/ask_to_powerful_llm", response_model=LLMResponse)
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
    
@router.get("/get_restaurants")
async def get_restaurants():
    con = sqlite3.connect('/root/AiSK-backend/demo.db')
    res = []
    # get all the restaurants
    cur = con.cursor()
    cur.execute('SELECT * FROM restaurants')
    rows = cur.fetchall()
    for k,row in enumerate(rows):
        cur_lat = 36.37215465823047
        cur_lon = 127.36158193444183
        lat = float(row[3])
        lon = float(row[4])
        # calculate distance in kilometers
        distance = 6371.01 * math.acos(math.sin(math.radians(cur_lat)) * math.sin(math.radians(lat)) + math.cos(math.radians(cur_lat)) * math.cos(math.radians(lat)) * math.cos(math.radians(cur_lon) - math.radians(lon)))
        
        # parse the distance to 2 decimal points with km attached
        distance = "{:.2f}km".format(distance)
        
        res.append({"name": row[1], "address": row[2], "distance":distance, "id": k+1})
    return res