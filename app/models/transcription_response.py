from pydantic import BaseModel

class TranscriptionResponse(BaseModel):
    text: str
    
class InitialResponse(BaseModel):
    menu_list: list
    
class LLMResponse(BaseModel):
    llm_text: str
    llm_audio_path: str
    now_menu_list: list
    basket: dict
    order_num: int
    state: int
    emotion: int
    emotion_degree: int