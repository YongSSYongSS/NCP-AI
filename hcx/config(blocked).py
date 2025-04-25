# API 호출 경로 및 인증 정보 관리리


class Config:
    # 지역 검색의 라우터 호출 경로
    ROUTER_API = 'https://clovastudio.stream.ntruss.com/testapp/v1/routers/2wjgrys0/versions/4/route'

    # 지역 검색 스킬셋 호출 경로
    SKILLSET_API = 'https://clovastudio.stream.ntruss.com/testapp/v1/skillsets/rdu3gp0f/versions/2/final-answer'
    
    # 지역 검색 스킬셋에 정의된 스킬(API)의 인증 정보
    NAVER_LOCAL_CLIENT_ID = 'mcLQwpVhlVaOj7WQysjI'
    NAVER_LOCAL_CLIENT_SECRET = 'yMwzPO3GBg'
    
    # Chat Completions 호출 경로
    CHAT_COMPLETIONS_API = 'https://clovastudio.stream.ntruss.com/testapp/v1/chat-completions/HCX-003'

    # CLOVA Studio API 인증 정보
    API_KEY = 'nv-a5f3ff49b79442c6af7b8d8995916b450me0'
    REQUEST_ID_ROUTER = 'kyhrouter' 
    REQUEST_ID_SKILLSET = 'kyhskillset'
    REQUEST_ID_CHAT = 'kyhchat'