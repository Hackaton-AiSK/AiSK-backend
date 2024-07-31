import urllib.request
from app.core.config import settings

def make_tts( text, speaker="vyuna", volume=0, speed=-2, pitch=1, 
                format="mp3", emotion=2, end_pitch=0, emotion_strength=1):
    encText = urllib.parse.quote(text)
    data = f"speaker={speaker}&volume={volume}&speed={speed}&pitch={pitch}&format={format}&emotion={emotion}&emotion-strength={emotion_strength}&end-pitch={end_pitch}&text={encText}"

    
    client_id = settings.CSR_ID
    client_secret = settings.CSR_SECRET
    url = "https://naveropenapi.apigw.ntruss.com/tts-premium/v1/tts"
    request = urllib.request.Request(url)
    request.add_header("X-NCP-APIGW-API-KEY-ID", client_id)
    request.add_header("X-NCP-APIGW-API-KEY", client_secret)

    try:
        response = urllib.request.urlopen(request, data=data.encode('utf-8'))
        rescode = response.getcode()
        if rescode == 200:
            # audio file of TTS audio/mpeg
            response_body = response.read()
            
            # do not save the audio file but return it
            return response_body
                
        else:
            raise Exception(f"Error Code: {rescode}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Usage example:
# tts = NaverTTS("your_client_id", "your_client_secret")
# tts.make_tts("안녕하세요. 저는 아이스크에요. 무엇을 도와드릴까요?", output_file="1111.mp3")