
# -*- coding: utf-8 -*-
import requests
import json

class CompletionExecutor:
    def __init__(self, host, api_key, request_id):
        self._host = host
        self._api_key = api_key
        self._request_id = request_id

    def execute(self, completion_request):
        headers = {
            'Authorization': self._api_key,
            'X-NCP-CLOVASTUDIO-REQUEST-ID': self._request_id,
            'Content-Type': 'application/json; charset=utf-8',
            # 'Accept': 'text/event-stream'
        }

        with requests.post(
            self._host + '/v3/chat-completions/HCX-007',
            headers=headers, json=completion_request, stream=False
        ) as r:
            # print(r.status_code)
            # print(r.text)
            data_json = json.loads(r.text)

            content = data_json["result"]["message"]["content"]
            print(content)

if __name__ == '__main__':
    completion_executor = CompletionExecutor(
        host='https://clovastudio.stream.ntruss.com',
        api_key='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
        request_id='e120d76b93e241378c09e0b292968aaf'
    )

    request_data = json.loads("""{
        "messages" : [ {
            "role" : "system",
            "content" : [ {
            "type" : "text",
            "text" : "두 사람의 대화를 보고 상품이 완전 판매가 되었는지, 불안전한 판매가 되었는지 판별과 사유를 출력해주세요.\\n완전 판매 사유: 고객의 특성(연령, 배경지식 등)으로 인해 쉬운 표현으로 바꾸어 충분히 설명한 경우\\n불완전 판매 사유: 충분히 설명했으나 고객의 이해도가 떨어지는 경우,고지사항 중 일부가 잘못 설명된 경우, 표현이 불분명하여 판별이 어려운 경우"
            } ]
        }, {
            "role" : "assistant",
            "content" : [ {
            "type" : "text",
            "text" : " 완전판매로 분류됩니다. 이유는 고객의 특성(연령, 배경지식 등)으로 인해 쉬운 표현으로 바꾸어 충분히 설명한 경우이기 때문입니다."
            } ]
        }, {
            "role" : "user",
            "content" : [ {
            "type" : "text",
            "text" : "상담원: 고객님, 가입하실 상품은 ‘TIGER MSCI Korea ESG ETF’입니다. 국내 주식 기반이고, ESG 기준을 따릅니다.\\r\\n고객: 예에...\\r\\n상담원: ETF는 상장지수펀드로 주식처럼 거래되는 펀드입니다. 원금 손실 가능성 있고요, 수수료는 운용보수 연 0.3% 수준입니다. 예금자 보호는 없고요. 환율 영향 없습니다. 중간에 해지하면 주식처럼 팔면 됩니다. 이해되셨죠?\\r\\n고객: 네, 뭐... 그런가 보죠.\\r\\n상담원: ETF는 적립식으로도 가능하고, 최근 ESG 테마는 각광받고 있는 분야라 수익성도 기대해볼 수 있습니다.\\r\\n고객: 예에...\\r\\n상담원: 설명은 다 드렸고요. 전자서명 진행하겠습니다."
            } ]
        } ],           
      "thinking" : {"effort" : "none"},
      "topP" : 0.8,
      "topK" : 0,
      "maxCompletionTokens" : 300,
      "temperature" : 0.5,
      "repetitionPenalty" : 1.1,
      "seed" : 0,
      "includeAiFilters" : false,
      "responseFormat": {
        "type" : "json",
        "schema": {
          "type": "object",
          "properties": {
            "feeling": {"type": "string", "description": "대화의 감정"},
            "reason": {"type": "string","description": "이유"}
          },
          "required": ["feeling", "reason"]
        } 
      }
    }""")  #,strict=False

    completion_executor.execute(request_data)    