# API 호출 경로 및 인증 정보 관리리


class Config:
    # 지역 검색의 라우터 호출 경로
    ROUTER_API = 'app url'

    # 지역 검색 스킬셋 호출 경로
    SKILLSET_API = 'app url'

    # 지역 검색 스킬셋에 정의된 스킬(API)의 인증 정보
    NAVER_LOCAL_CLIENT_ID = 'CLIENT_ID'
    NAVER_LOCAL_CLIENT_SECRET = 'CLIENT_secret'

    # Chat Completions 호출 경로
    CHAT_COMPLETIONS_API = 'app url'

    # CLOVA Studio API 인증 정보
    API_KEY = 'API Key'
    REQUEST_ID_ROUTER = 'kyhrouter' 
    REQUEST_ID_SKILLSET = 'kyhskillset'
    REQUEST_ID_CHAT = 'kyhchat'