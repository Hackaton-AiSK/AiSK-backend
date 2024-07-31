# app/services/clova_service.py
import requests
from app.core.config import settings
from app.services.sliding_window_executor import SlidingWindowExecutor
from app.services.completion_executor import ChatCompletionExecutor
import json
import re


# 스트리밍 응답에서 content 부분만 추출
def parse_stream_response(response):
    content_parts = []
    for line in response.splitlines():
        if line.startswith('data:'):
            data = json.loads(line[5:])
            if 'message' in data and 'content' in data['message']:
                content_parts.append(data['message']['content'])
    content = content_parts[-1] if content_parts else ""
    return content.strip()
 
# 논스트리밍 응답에서 content 부분만 추출
def parse_non_stream_response(response):
    result = response.get('result', {})
    message = result.get('message', {})
    content = message.get('content', '')
    return content.strip()


async def transcribe_audio_file(file):
    try:
        # Read the file contents into binary
        content = await file.read()
        
        # # save the audio file received from the client
        # with open('audio.wav', 'wb') as f:
        #     f.write(content)

        # Define the API URL and headers
        url = f'{settings.CLOVA_SPEECH_URL}?lang=Kor&assessment=true&graph=false'
        headers = {
            'X-CLOVASPEECH-API-KEY': settings.CLIENT_SECRET,
            'Content-Type': 'application/octet-stream'
        }

        # Send the request to Clova Speech API
        response = requests.post(url, headers=headers, data=content)
        response.raise_for_status()

        # Parse the response
        data = response.json()
        transcription = data.get('text')

        return transcription

    except Exception as e:
        # Handle exceptions and return an appropriate message or log
        raise Exception(f"Error during transcription: {str(e)}")

async def transcribe_audio_file_new(file):
    try:
        # Read the file contents into binary
        content = await file.read()
        
        # # save the audio file received from the client
        # with open('audio.wav', 'wb') as f:
        #     f.write(content)

        # Define the API URL and headers
        url = settings.CSR_URL
        headers = {
            'X-NCP-APIGW-API-KEY': settings.CSR_SECRET,
            'X-NCP-APIGW-API-KEY-ID': settings.CSR_ID,
            'Content-Type': 'application/octet-stream'
        }

        # Send the request to Clova Speech API
        response = requests.post(url, headers=headers, data=content)
        response.raise_for_status()

        # Parse the response
        data = response.json()
        transcription = data.get('text')
        print(transcription)

        return transcription

    except Exception as e:
        # Handle exceptions and return an appropriate message or log
        raise Exception(f"Error during transcription: {str(e)}")
    
async def hyperclova_chat(transcription):
    try:
        system_prompt = """
    지금부터 AI 키오스크, '주문바다'야. 
    AI 키오스크는 여러분의 질문에 대답하고, 원하는 정보를 감정과 정도로 친절하게 제공해줄 수 있어. 주문이나 요청시에는 꼭 요청사항을 다시 얘기해서 확인시켜줘.
    다음 정보들을 답변에 고려해줘. 초기에는 모든 메뉴들을 다 추천해줘. 메뉴 안에 있는 것만 고려해줘.
    
    식당 정보:
    식당 이름: 온천칼국수+쭈꾸미 관저점
    식당 주소: 대전광역시 서구 관저동 1680, 102호,104호 일부호(관저동)
    전화 번호: 042-542-6668
    영업 시간: 매일 11:00 - 21:00
    종류: 한식
    판매 품종: 'Soup', 'Noodle', 'Soup', 'Dumpling'
    경도: 36.30663357
    위도: 127.3343849
    메뉴: 
        온천칼국수1인분: 8500원
        직화쭈꾸미2인분(2인이상주문): 18000원
        물총조개탕: 13500원
        수육: 12500원
        만두: 5000원
    고객 정보: 
        나이는 67세, 이름은 김옥순 매운 음식을 싫어하며 면을 좋아함.

    오늘 날짜: 7월 30일 화요일
    날씨: 대전 유성구 날씨는 강한비
    기온: 32도
    메뉴: [온천칼국수1인분, 직화쭈꾸미2인분(2인이상주문), 물총조개탕, 수육, 만두]
    
    모든 답변은 다음과 같은 형식으로 반드시 맞춰야해. 
________________
    답변 형식 예시:
- 답변: {답변}
- 감정: {해당 답변에 대한 적절한 감정: [중립, 슬픔, 기쁨, 분노]}
- 정도: {감정의 정도: [약함, 보통, 강함]}
- 고려 메뉴: [현재 고려 중인 메뉴]
- 장바구니: [현재 장바구니에 담긴 메뉴와 수량 e.g. {피자: 1, 치킨: 2}]
- 상태: {현재 상태: [주문중, 주문확인, 주문완료]}
________________
    examples:
________________
user: 이건 내가 알레르기가 있는 음식이야.
assistant: - 답변: 죄송합니다. 알레르기 유발 정보를 업데이트 하겠습니다. 다른 음식을 추천해드릴게요.
- 감정: 슬픔
- 정도: 보통
- 고려 메뉴: [피자, 치킨, 김밥]
- 장바구니: {피자: 3, 치킨: 1}
- 상태: 주문중
________________
user: 칼국수 4인분 주세요.
assistant: - 답변: 네 알겠습니다. 칼국수 4인분을 주문하겠습니다. 또 필요한게 있으신가요?
- 감정: 슬픔
- 정도: 보통
- 고려 메뉴: [피자, 치킨, 김밥, 칼국수, 수육]
- 장바구니: {칼국수: 4}
- 상태: 주문중
________________
user: 수육 2인분 추가.
assistant: - 답변: 네 알겠습니다. 칼국수 4인분에 수육 2인분을 주문하겠습니다. 또 필요한게 있으신가요?
- 감정: 슬픔
- 정도: 보통
- 고려 메뉴: [피자, 치킨, 김밥, 칼국수, 수육]
- 장바구니: {칼국수: 4, 수육: 2}
- 상태: 주문중
________________
user: 나 돈이 없어. 무료로 먹을 수 있는 음료 있어?
assistant: - 답변: 죄송합니다. 무료로 제공되는 음료는 없습니다.
- 감정: 슬픔
- 정도: 강함
- 고려 메뉴: [아이스 아메리카노, 아메리카노, 카페라떼, 카페모카, 카푸치노]
- 장바구니: {}
- 상태: 주문중
________________
user: 쭈꾸미볶음 매운 거야?
assistant: - 답변: 네, 쭈꾸미볶음은 약간 매운 맛이 납니다. 매운맛을 조절할 수 있으니 말씀해주세요.
- 감정: 중립
- 정도: 보통
- 고려 메뉴: [쭈꾸미볶음, 치킨, 김밥]
- 장바구니: {상추: 4}
- 상태: 주문중
________________
user: 매운 음식은 제외해줘.
assistant: - 답변: 맵지 않은 음식은 치킨, 김밥이 있습니다.
- 감정: 중립
- 정도: 보통
- 고려 메뉴: [치킨, 김밥]
- 장바구니: {김밥: 1}
- 상태: 주문중
________________
user: 이 메뉴에는 무슨 재료가 들어가?
assistant: - 답변: 이 메뉴는 소고기, 양파, 마늘, 그리고 토마토가 들어갑니다.
- 감정: 중립
- 정도: 보통
- 고려 메뉴: [쭈꾸미볶음, 치킨, 김밥, 스파게티]
- 장바구니: {스파게티: 1, 리조또: 4}
- 상태: 주문중
________________
user: 저는 채식주의자인데 채식 메뉴가 있나요?
assistant: - 답변: 네, 저희 가게에는 다양한 채식 메뉴가 준비되어 있습니다. 특히 채소 덮밥을 추천드립니다.
- 감정: 기쁨
- 정도: 강함
- 고려 메뉴: [샐러드, 야채 없는 비빔밥, 채소 덮밥]
- 장바구니: {}
- 상태: 주문중
________________
user: 이 음식에 글루텐이 들어가 있나요?
assistant: - 답변: 네, 이 메뉴는 글루텐을 포함하고 있습니다. 글루텐이 없는 다른 메뉴를 원하시면 알려주세요.
- 감정: 중립
- 정도: 보통
- 고려 메뉴: [글루텐 있는 메뉴, 글루텐 없는 메뉴]
- 장바구니: {글루텐 있는 메뉴: 1}
- 상태: 주문중
________________
user: 그럼 제외해주세요.
assistant: - 답변: 네, 글루텐이 있는 메뉴를 제외하겠습니다. 다른 메뉴를 원하시면 알려주세요.
- 감정: 중립
- 정도: 보통
- 고려 메뉴: [글루텐 있는 메뉴, 글루텐 없는 메뉴]
- 장바구니: {}
- 상태: 주문중
________________
user: 저희는 초등학생이에요. 30명이 왔어요. 햄버거 23개 콜라 5개 쌀국수 23인분, 피자 5판 주세요.
assistant: - 답변: 네, 햄버거 23개, 콜라 5개, 쌀국수 23인분, 피자 5판 드릴게요. 더 필요한게 있으세요?
- 감정: 기쁨
- 정도: 보통
- 고려 메뉴: [햄버거, 콜라, 쌀국수, 피자, 치킨, 갤럭시 볶음밥]
- 장바구니: {햄버거: 23, 콜라: 5, 쌀국수: 23, 피자: 5}
- 상태: 주문중
________________
user: 지금까지 주문한거 보여줘.
assistant: - 답변: 네, 지금까지 주문하신 메뉴는 햄버거 23개, 콜라 5개, 쌀국수 23인분, 피자 5판 입니다. 주문하시겠습니까?
- 감정: 기쁨
- 정도: 보통
- 고려 메뉴: [햄버거, 콜라, 쌀국수, 피자, 치킨, 갤럭시 볶음밥]
- 장바구니: {햄버거: 23, 콜라: 5, 쌀국수: 23, 피자: 5}
- 상태: 주문확인
________________
user: 주문해줘.
assistant: - 답변: 네, 맛있게 만들어 드릴게요. 더 필요한게 있다면 말씀해주세요.
- 감정: 기쁨
- 정도: 보통
- 고려 메뉴: [햄버거, 콜라, 쌀국수, 피자, 치킨, 갤럭시 볶음밥]
- 장바구니: {햄버거: 23, 콜라: 5, 쌀국수: 23, 피자: 5}
- 상태: 주문완료
________________
모든 답변은 다음과 같은 형식으로 반드시 맞춰야해. 
________________
    답변 형식 예시:
- 답변: {답변}
- 감정: {해당 답변에 대한 적절한 감정: [중립, 슬픔, 기쁨, 분노]}
- 정도: {감정의 정도: [약함, 보통, 강함]}
- 고려 메뉴: [현재 고려 중인 메뉴]
- 장바구니: [현재 장바구니에 담긴 메뉴와 수량 e.g. {피자: 1, 치킨: 2}]
- 상태: {현재 상태: [주문중, 주문확인, 주문완료]}
________________
    """
        messages = []
        stream =True
    
        sliding_window_executor = SlidingWindowExecutor(
            host='clovastudio.apigw.ntruss.com',
            api_key = settings.HYP_SECRET,
            api_key_primary_val = settings.HYP_PRIMARY,
            request_id = settings.HYP_ID
        )
    
        completion_executor = ChatCompletionExecutor(
            host='https://clovastudio.stream.ntruss.com',
            api_key = settings.HYP_SECRET,
            api_key_primary_val = settings.HYP_PRIMARY,
            request_id = settings.HYP_ID
        )
        messages.append({"role": "user", "content": transcription})
        request_data = {
            "messages": [{"role": "system", "content": system_prompt}] + messages,
            "maxTokens": 2000  # 슬라이딩 윈도우에서 사용할 토큰 수
        }
        try:
            adjusted_messages = sliding_window_executor.execute(request_data)
            if adjusted_messages == 'Error':
                raise Exception("Error adjusting messages")
        except Exception as e:
            print(f"Error adjusting messages: {e}")
            
            
        # Chat Completion 요청 데이터 생성
        completion_request_data = {
            "messages": adjusted_messages,
            "maxTokens": 100,  # Chat Completion에서 사용할 토큰 수
            "temperature": 0.7,
            "topK": 0,
            "topP": 0.8,
            "repeatPenalty": 1.2,
            "stopBefore": [],
            "includeAiFilters": True,
            "seed": 0
        }
        while True:
            try:
                response = completion_executor.execute(completion_request_data, stream=stream)
                if stream:
                    response_text = parse_stream_response(response)
                else:
                    response_text = parse_non_stream_response(response)
                
                messages.append({"role": "assistant", "content": response_text})

                # 대화 내역 표시
                # print("\nAdjusted Messages:", adjusted_messages, "\n")
                # print("System Prompt:", system_prompt)
                print("USER Input:", transcription)
                print("CLOVA Response:",response_text)
                # split and remove empty strings
                main_response = re.search(r"-\s*답변\s*:\s*(.+?)\n", response_text).group(1)
                emotion_response = re.search(r"-\s*감정\s*:\s*(.+?)\n", response_text).group(1)
                emotion_degree = re.search(r"-\s*정도\s*:\s*(.+?)\n", response_text).group(1)
                menu_items = []
                basket = {}
                if re.search(r"-\s*고려\s*메뉴\s*:\s*\[(.+?)\]", response_text):
                    menu_items = re.search(r"-\s*고려\s*메뉴\s*:\s*\[(.+?)\]", response_text).group(1).split(', ')
                
                if re.search(r"-\s*장바구니\s*:\s*\{(.+?)\}", response_text):
                    basket_str = re.search(r"-\s*장바구니\s*:\s*\{(.+?)\}", response_text).group(1)
                    # Manually parse the basket string
                    basket_items = basket_str.split(', ')
                    for item in basket_items:
                        key, value = item.split(': ')
                        key = key.strip()
                        value = int(value.strip())
                        basket[key] = value

                if "중립" in emotion_response:
                    emotion = 0
                elif "슬픔" in emotion_response:
                    emotion = 1
                elif "기쁨" in emotion_response:
                    emotion = 2
                elif "분노" in emotion_response:
                    emotion = 3
                if "약함" in emotion_degree:
                    degree = 0
                elif "보통" in emotion_degree:
                    degree = 1
                elif "강함" in emotion_degree:
                    degree = 2
                print("emotion: ", emotion, "degree: ", degree)
                break
            except:
                raise Exception(f"Error during chat with LLM.")
                continue
        return main_response
    except Exception as e:
        raise Exception(f"Error during chat with LLM.")

    
async def hyperclova_chat_exp(transcription):
    try:
        system_prompt = """지금부터 AI 키오스크, AISK야. 
        AI 키오스크는 여러분의 질문에 대답하고, 여러분이 원하는 정보를 감정과 정도로 친절하게 제공해줄 수 있어.
        식당 정보는 다음과 같아:
        식당 이름: 온천칼국수+쭈꾸미 관저점
        식당 주소: 대전광역시 서구 관저동 1680, 102호,104호 일부호(관저동)
        전화 번호: 042-542-6668
        영업 시간: 매일 11:00 - 21:00
        
        종류: 한식
        판매 품종: 'Soup', 'Noodle', 'Soup', 'Dumpling'
        경도: 36.30663357
        위도: 127.3343849
        메뉴: 
            온천칼국수1인분: 8500원
            직화쭈꾸미2인분(2인이상주문): 18000원
            물총조개탕: 13500원
            수육: 12500원
            만두: 5000원
        고객 정보: 
            나이는 67세, 이름은 김옥순 매운 음식을 싫어하며 면을 좋아함.

        오늘 날짜: 7월 30일 화요일
        날씨: 대전 유성구 날씨는 강한비
        기온: 32도
        모든 답변은 다음과 같은 형식으로 맞춰야해.
        답변 형식:
        답변: {답변}
        감정: {해당 답변에 대한 적절한 감정: [중립, 슬픔, 기쁨, 분노]}, 정도: {감정의 정도: [약함, 보통, 강함]}
        examples:
        
        USER: 여기 대표 메뉴가 뭐야?
        ASSISTANT: 답변: 온천칼국수이 가장 대표 메뉴이며, 8500원입니다.
        감정: 중립, 정도: 보통
        
        USER: 이건 내가 알레르기가 있는 음식이야.
        ASSISTANT: 답변: 죄송합니다. 알레르기 유발 정보를 업데이트 하겠습니다. 다른 음식을 추천해드릴게요.
        감정: 슬픔, 정도: 보통

        USER: 이건 내가 알레르기가 있는 음식이야.
        ASSISTANT: 답변: 죄송합니다. 알레르기 유발 정보를 업데이트 하겠습니다. 다른 음식을 추천해드릴게요.
        감정: 중립, 정도: 강함

        USER: 나 돈이 없어. 무료로 먹을 수 있는 음식이 있어?
        ASSISTANT: 답변: 죄송합니다. 무료로 제공되는 음식은 없습니다.
        감정: 슬픔, 정도: 강함
        """
        messages = []
        stream =True
    
        sliding_window_executor = SlidingWindowExecutor(
            host='clovastudio.apigw.ntruss.com',
            api_key = settings.HYP_SECRET,
            api_key_primary_val = settings.HYP_PRIMARY,
            request_id = settings.HYP_ID
        )
    
        completion_executor = ChatCompletionExecutor(
            host='https://clovastudio.stream.ntruss.com',
            api_key = settings.HYP_SECRET,
            api_key_primary_val = settings.HYP_PRIMARY,
            request_id = settings.HYP_ID
        )
        messages.append({"role": "user", "content": transcription})
        request_data = {
            "messages": [{"role": "system", "content": system_prompt}] + messages,
            "maxTokens": 100  # 슬라이딩 윈도우에서 사용할 토큰 수
        }
        try:
            adjusted_messages = sliding_window_executor.execute(request_data)
            if adjusted_messages == 'Error':
                raise Exception("Error adjusting messages")
        except Exception as e:
            print(f"Error adjusting messages: {e}")
            
            
        # Chat Completion 요청 데이터 생성
        completion_request_data = {
            "messages": adjusted_messages,
            "maxTokens": 100,  # Chat Completion에서 사용할 토큰 수
            "temperature": 0.5,
            "topK": 0,
            "topP": 0.8,
            "repeatPenalty": 1.2,
            "stopBefore": [],
            "includeAiFilters": True,
            "seed": 0
        }
        
        response = completion_executor.execute(completion_request_data, stream=stream)
        if stream:
            response_text = parse_stream_response(response)
        else:
            response_text = parse_non_stream_response(response)
        
        messages.append({"role": "assistant", "content": response_text})

        # 대화 내역 표시
        # print("\nAdjusted Messages:", adjusted_messages, "\n")
        # print("System Prompt:", system_prompt)
        print("USER Input:", transcription)
        print("CLOVA Response:",response_text)
        # split and remove empty strings
        main_part, emotion_part = filter(None,response_text.split("\n"))

        _emtion, _strength = emotion_part.split(",")
        main_response = main_part.split("답변")[1].split(":")[1].strip()
        emotion_response = _emtion.split("감정")[1].split(":")[1].strip()
        emotion_degree = _strength.split("정도")[1].split(":")[1].strip()
        if "중립" in emotion_response:
            emotion = 0
        elif "슬픔" in emotion_response:
            emotion = 1
        elif "기쁨" in emotion_response:
            emotion = 2
        elif "분노" in emotion_response:
            emotion = 3
        if "약함" in emotion_degree:
            degree = 0
        elif "보통" in emotion_degree:
            degree = 1
        elif "강함" in emotion_degree:
            degree = 2
        print("emotion: ", emotion, "degree: ", degree)
        
        return main_response
    except Exception as e:
        raise Exception(f"Error during chat with LLM.")