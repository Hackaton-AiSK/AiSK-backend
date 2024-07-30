from app.services.clovastudio_executor import CLOVAStudioExecutor
from http import HTTPStatus
import requests
 
class ChatCompletionExecutor(CLOVAStudioExecutor):
    def __init__(self, host, api_key, api_key_primary_val, request_id):
        super().__init__(host, api_key, api_key_primary_val, request_id)
 
    def execute(self, completion_request, stream=True):
        headers = {
            'X-NCP-CLOVASTUDIO-API-KEY': self._api_key,
            'X-NCP-APIGW-API-KEY': self._api_key_primary_val,
            'X-NCP-CLOVASTUDIO-REQUEST-ID': self._request_id,
            'Content-Type': 'application/json; charset=utf-8',
            'Accept': 'text/event-stream' if stream else 'application/json'
        }
 
        with requests.post(self._host + '/testapp/v1/chat-completions/HCX-003',
                           headers=headers, json=completion_request, stream=stream) as r:
            if stream:
                if r.status_code == HTTPStatus.OK:
                    response_data = ""
                    for line in r.iter_lines():
                        if line:
                            decoded_line = line.decode("utf-8")
                            response_data += decoded_line + "\n"
                    return response_data
                else:
                    raise ValueError(f"오류 발생: HTTP {r.status_code}, 메시지: {r.text}")
            else:
                if r.status_code == HTTPStatus.OK:
                    return r.json()
                else:
                    raise ValueError(f"오류 발생: HTTP {r.status_code}, 메시지: {r.text}")