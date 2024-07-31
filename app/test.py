import os
import sys

os.chdir('/root/AiSK-backend/app')

# Ensure the directory is added to sys.path
sys.path.append('/root/AiSK-backend')

import asyncio
from app.models.transcription_response import TranscriptionResponse, LLMResponse
from app.services.llm_service import powerful_llm_chat, new_llm_chat
# Change the working directory to the specified path

from app.services.clova_services import hyperclova_chat
from app.services.llm_service import powerful_llm_chat
messages = []
messages = new_llm_chat(messages)

menu_str_to_ids = {"온천칼국수" : 1, "직화쭈꾸미" : 2, "물총조개탕" : 3, "수육" : 4, "만두" : 5}
ids_to_menu_str = {1 : "온천칼국수", 2 : "직화쭈꾸미", 3 : "물총조개탕", 4 : "수육", 5 : "만두"}

async def main():
    answer = await powerful_llm_chat("온천 칼국수 4인분 주문해줘.", messages, menu_str_to_ids, ids_to_menu_str)
    response = LLMResponse(llm_text=answer["llm_text"], llm_audio_path=answer["llm_audio_path"], now_menu_list=answer["now_menu_list"], order_num=answer["order_num"], state=answer["state"], basket=answer["basket"], emotion=answer["emotion"], emotion_degree=answer["emotion_degree"])
    print(response)

if __name__ == "__main__":
    asyncio.run(main())
    
# class LLMResponse(BaseModel):
#     llm_text: str
#     llm_audio_path: str
#     now_menu_list: list
#     basket: dict
#     order_num: int
#     state: str
#     emotion: str
#     emotion_degree: int