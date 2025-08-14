import re
import json
from datetime import datetime
from zoneinfo import ZoneInfo
import requests

API_KEY = "XXXXXXXXX"  
REQUEST_ID = "XXXXXX"

url = "https://clovastudio.stream.ntruss.com/v3/chat-completions/HCX-005"
headers = {
    "Authorization": API_KEY,
    "X-NCP-CLOVASTUDIO-REQUEST-ID": REQUEST_ID,
    "Content-Type": "application/json"
}

# (1) tool을 꼭 쓰게 힌트 주기
messages = [
    {"role": "system", "content": "날씨 관련 질문에는 반드시 get_weather 도구를 호출해라."},
    {"role": "user", "content": "서울 날씨 어때?"}
]

data = {
    "messages": messages,
    "tools": [
        {
            "type": "function",
            "function": {
                "description": "날씨를 알려줄 수 있는 도구",
                "name": "get_weather",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {"type": "string", "description": "서울, 대전, 부산 등의 도시 이름"},
                        "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                        "date": {"type": "string", "description": "YYYY-MM-DD 또는 YYYYMMDDHHMM"}
                    },
                    "required": ["location"]
                }
            }
        }
    ],
    "toolChoice": "auto"
}


STN_MAP = {
    "서울": "108", "부산": "159", "인천": "112", "대구": "143",
    "대전": "133", "광주": "156", "울산": "152", "제주": "184",
}

def _to_tm(date_str: str | None) -> str:
    if not date_str:
        now_kst = datetime.now(ZoneInfo("Asia/Seoul"))
        return now_kst.strftime("%Y%m%d%H%M")
    ds = re.sub(r"[^0-9]", "", str(date_str))
    if len(ds) == 8:
        return ds + "0900"
    if len(ds) == 12:
        return ds
    raise ValueError("date는 YYYY-MM-DD 또는 YYYYMMDDHHMM 형식이어야 합니다.")

def get_weather(location, unit="celsius", date=None):
    url_kma = "https://apihub.kma.go.kr/api/typ01/url/kma_sfctm2.php"
    tm = _to_tm(date)
    stn = STN_MAP.get(location, "0")
    help_flag = "1"
    authkey = "zxiqblJaSgSYqm5SWioEeA"  # 운영은 환경변수 사용 권장

    resp = requests.get(
        url_kma,
        params={"tm": tm, "stn": stn, "help": help_flag, "authKey": authkey},
        timeout=10,
    )
    # 디버그
    print("[KMA] status:", resp.status_code, resp.url)
    resp.raise_for_status()
    resp.encoding = resp.apparent_encoding or "utf-8"
    text = resp.text

    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    header = None
    for ln in lines:
        if ln.startswith("#"):
            cand = ln.lstrip("#").strip().split()
            if "stn" in cand and "tm" in cand:
                header = cand
    data_lines = [ln for ln in lines if not ln.startswith("#")]

    rows = []
    for ln in data_lines:
        parts = ln.split()
        cols = header or [f"col{i+1}" for i in range(len(parts))]
        rows.append(dict(zip(cols, parts)))

    if unit == "fahrenheit":
        for row in rows:
            for key in ("ta", "temp", "temperature"):
                if key in row:
                    try:
                        c = float(row[key])
                        row[key + "_f"] = round(c * 9 / 5 + 32, 1)
                    except Exception:
                        pass

    return {"request": {"tm": tm, "stn": stn, "help": help_flag}, "rows": rows, "raw_preview": text[:500]}
# ----------------------------------------------------------------------

# 1차 호출
response = requests.post(url, headers=headers, json=data)
result = response.json()
print("[RAW 1] ", json.dumps(result, ensure_ascii=False)[:1000], "...\n")  # 먼저 원본 응답 확인

status = result.get("status", {})
if status and status.get("code") not in (None, "20000"):
    print("[ERROR] status:", status)
    raise SystemExit

assistant_msg = result.get("result", {}).get("message", {}) or {}
tool_calls = assistant_msg.get("toolCalls", [])
print("[ToolCalls?] ->", bool(tool_calls))

if tool_calls:
    # 첫 번째 tool call만 처리 (여러 개면 loop)
    tc = tool_calls[0]
    tool_id = tc.get("id")
    fn = tc.get("function", {}).get("name")
    args = tc.get("function", {}).get("arguments", {})
    print("[Call]", fn, args)

    function_result = None
    if fn == "get_weather":
        function_result = get_weather(**args)
        print("[FunctionResult]", json.dumps(function_result, ensure_ascii=False)[:500], "...\n")

    # tool 결과를 role:"tool"로 전달하고, 최종 답변 받기
    followup_messages = messages + [
        {"role": "assistant", "content": assistant_msg.get("content", ""), "toolCalls": tool_calls},
        {"role": "tool", "toolCallId": tool_id, "content": json.dumps(function_result, ensure_ascii=False)}
    ]
    payload2 = {"messages": followup_messages, "tools": data["tools"], "toolChoice": "auto"}
    r2 = requests.post(url, headers=headers, json=payload2)
    j2 = r2.json()
    print("[RAW 2] ", json.dumps(j2, ensure_ascii=False)[:1000], "...\n")
    final_text = j2.get("result", {}).get("message", {}).get("content")
    print("[FINAL ANSWER]\n", final_text)
else:
    # 도구를 안 쓴 경우: 모델이 그냥 답했을 가능성
    plain_text = assistant_msg.get("content")
    print("[NO TOOL CALL] assistant content:\n", plain_text)
