import os
import sys

os.chdir('/root/AiSK-backend/app')

# Ensure the directory is added to sys.path
sys.path.append('/root/AiSK-backend')

import asyncio
from app.models.transcription_response import TranscriptionResponse, LLMResponse
from app.services.llm_service import powerful_llm_chat, new_llm_chat
# Change the working directory to the specified path

messages = []
restaurant_id = 2
messages, menu_str_to_ids, ids_to_menu_str, menu_items_frontend = new_llm_chat(messages, restaurant_id)

async def main():
    answer = await powerful_llm_chat("메뉴가 뭐뭐 있어?.", messages, menu_str_to_ids, ids_to_menu_str)
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