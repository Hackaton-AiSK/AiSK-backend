import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # CLIENT_ID: str = os.getenv("CLIENT_ID")
    CLIENT_SECRET: str = os.getenv("CLIENT_SECRET")
    CLOVA_SPEECH_URL: str = "https://clovaspeech-gw.ncloud.com/recog/v1/stt"
    CSR_URL: str = "https://naveropenapi.apigw.ntruss.com/recog/v1/stt?lang=Kor"
    CSR_ID: str = os.getenv("CSR_ID")
    CSR_SECRET: str = os.getenv("CSR_SECRET")
    HYP_ID: str = os.getenv("HYP_ID")
    HYP_SECRET: str = os.getenv("HYP_SECRET")
    HYP_PRIMARY: str = os.getenv("HYP_PRIMARY")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
settings = Settings()