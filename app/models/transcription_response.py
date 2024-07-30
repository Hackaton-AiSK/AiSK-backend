from pydantic import BaseModel

class TranscriptionResponse(BaseModel):
    text: str

class LLMResponse(BaseModel):
    llm_text: str
    llm_audio: str
    menu_list: list
    order_num: int
    state: str