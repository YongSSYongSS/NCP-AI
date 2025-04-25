#지역 검색 스킬셋 API를 호출하여 실시간 검색 데이터를 기반으로 한 답변 생성

import requests
from config import Config

def get_skillset(query, chat_history=None):
    url = Config.SKILLSET_API
    headers = {
        'Authorization': f'Bearer {Config.API_KEY}',
        'X-NCP-CLOVASTUDIO-REQUEST-ID': f'{Config.REQUEST_ID_SKILLSET}',
        'Content-Type': 'application/json',
    }

    data = {
        'query': query,
        'requestOverride': {
            'baseOperation': {
                'header': {
                    'X-Naver-Client-Id': Config.NAVER_LOCAL_CLIENT_ID,
                    'X-Naver-Client-Secret': Config.NAVER_LOCAL_CLIENT_SECRET
                }
            }
        }
    }

    if chat_history:
        # 직전 user 턴의 발화 및 assistant 턴의 답변을 가져옵니다.
        filtered_chat_history = chat_history[-3:-1]
        data['chatHistory'] = filtered_chat_history

    response = requests.post(url, headers=headers, json=data)
    return response.json()