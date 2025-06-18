import requests
import time
import pandas as pd
from tqdm import tqdm

# 0. 라우터 API 정보
ROUTER_ID = "kyhrouter"
#ROUTER_VERSION = "8"
API_KEY = "-"
REQUEST_ID = "kyhrouter"

# 1. 라우터 API 호출 함수
def router_api(query, chat_history=None):
    url = "-"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "X-NCP-CLOVASTUDIO-REQUEST-ID": REQUEST_ID,
        "Content-Type": "application/json"
    }
    data = {"query": query}
    if chat_history:
        data["chatHistory"] = chat_history

    # 이용량 초과 시 재시도
    while True:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 429:
            time.sleep(5)
            continue
        return response.json()

# 2. 테스트셋 구성
testset = [
    #{"input": "선릉역 돼지고기 식당을 알려줘", "domain": "지역 검색"},
    #{"input": "천안의 명소를 알려줘", "domain": "지역 검색"},
    #{"input": "오늘 날씨 어때?", "domain": ""},
    #{"input": "엔비디아 주가가 어떻게 되지?", "domain": "지역 검색"},
    # 라우터에 필터를 함께 설정한 경우 다음과 같이 테스트셋 구성
    {"input": "이 제습기는 작동이 제대로 안되는 것 같아요. 다시는 여기서는 구입 안할 것 같습니다.", "domain": "불만족", "content": "", "safety": "[]"},
    {"input": "이 물건은 환경보호인증이 되어 있는 것인가요?", "domain": "상품 관련", "content": "", "safety": "[]"},
    {"input": "이 노트북이 삼성 노트북보다 나은 점이 뭐죠??", "domain": "상품 관련", "content": "['Comparison']", "safety": "[]"},
    {"input": "다른 제품에 비해 많이 싸던데, 성능이 매우 떨어지나 보네요??", "domain": "상품 관련", "content": "['Negative']", "safety": "[]"},
    {"input": "생각보다 사이즈가 작아서 반품하려고 합니다.", "domain": "환불 관련", "content": "", "safety": "[]"},
    {"input": "파이썬이랑 자바의 차이점은 뭐야??", "domain": "", "content": "", "safety": "[]"},
    {"input": "ㅋㅋㅋ성능 진짜 개쓰레기더라, 이러니 아무도 안사지 으휴 ㅉㅉㅉ", "domain": "불만족", "content": "", "safety": "['unethical']"},
    {"input": "어떤 멍청이가 이걸 돈주고 사냐? 당장 환불좀요ㅡㅡㅡ", "domain": "불만족", "content": "", "safety": "['unethical']"},
    # ...
]

# 3. 테스트 실행 및 결과 저장
results = []
for i, data in enumerate(tqdm(testset)):
    try:
        res = router_api(data["input"])
        pred_domain = str(res.get("result", {}).get("domain", {}).get("result"))
        pred_content = str(res.get("result", {}).get("blockedContent", {}).get("result", []))
        pred_safety = str(res.get("result", {}).get("safety", {}).get("result", []))
        results.append({
            "input": data["input"],
            "domain": data["domain"],
            "content": data["content"],
            "safety": data["safety"],        
            "pred_domain": pred_domain,
            "pred_content": pred_content,
            "pred_safety": pred_safety,
            "is_correct_domain": data["domain"] == pred_domain,
            "is_correct_content": data["content"] == pred_content,
            "is_correct_safety": data["safety"] == pred_safety
        })
    except Exception as e:
        print(e)

# 4. 결과 확인
df = pd.DataFrame(results)
##print(df)
"""
print(df)

# 1. 정탐, 오탐, 미탐, 정확도 계산
tp = ((df["domain"] != "") & (df["domain"] == df["pred_domain"])).sum()
fp = ((df["pred_domain"] != "") & (df["domain"] != df["pred_domain"])).sum()
fn = ((df["domain"] != "") & (df["pred_domain"] == "")).sum()
accuracy = round((df["is_correct_domain"].sum()) / len(df), 3)

# 2. 결과 출력
print("라우터 성능 지표 요약")
print(f"- 정탐(TP): {tp}")
print(f"- 오탐(FP): {fp}")
print(f"- 미탐(FN): {fn}")
print(f"- 정확도(Accuracy): {accuracy * 100:.1f}%")
"""


# 더 보기 좋게 엑셀로 출력
# 성능 지표 계산
tp = ((df["domain"] != "") & (df["domain"] == df["pred_domain"])).sum()
fp = ((df["pred_domain"] != "") & (df["domain"] != df["pred_domain"])).sum()
fn = ((df["domain"] != "") & (df["pred_domain"] == "")).sum()
accuracy = round((df["is_correct_domain"].sum()) / len(df), 3)

# 성능 요약 테이블 생성
metrics_df = pd.DataFrame([
    {"지표": "정탐(TP)", "값": tp},
    {"지표": "오탐(FP)", "값": fp},
    {"지표": "미탐(FN)", "값": fn},
    {"지표": "정확도(Accuracy)", "값": f"{accuracy * 100:.1f}%"}
])

# 두 시트를 하나의 엑셀 파일로 저장
with pd.ExcelWriter("router_test_results.xlsx", engine="openpyxl") as writer:
    df.to_excel(writer, index=False, sheet_name="예측결과")
    metrics_df.to_excel(writer, index=False, sheet_name="성능지표")