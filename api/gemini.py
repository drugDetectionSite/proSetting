# 저희가 gemini를 활용하므로 만든 파일입니다.
# Gemini(llm)를 호출하며 DB 저장 로직은 여기서 안 하고 분석 결과만 반환합니다.

# 백앤드팀 정유림님 작성 코드(Gemini 호출 코드)

from google import genai
import os
# TODO 남혜진: .env(환경변수)에서 제미나이 키 호출을 위함
from dotenv import load_dotenv
import json
from google.genai.errors import ClientError
load_dotenv()

# 키 직접 노출 방지를 위한 우회, 환경 변수 값을 가져옴.
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key = GEMINI_API_KEY)

# TODO 남혜진: 서버는 계속 실행될 수 있는데 1)아래 방식은 한 번만 실행
# TODO 남혜진: 2) 사용자가 보낸 게시글 text가 AI에 들어가지 않음
# TODO 남혜진: 따라서 아래와 같은 함수 형식으로 수정하였습니다.1) 함수생성, 2)contents 변수에 프롬프트 넣음
"""
model="gemini-2.5-flash"

response = client.models.generate_content(
    model = model, contents = "Explain how AI works in a few words"
)

print(response.text)
"""

# TODO 남혜진: 안에 들어가는 f""" """ 부분은 주석이 아닌 멀티라인 문자열
# TODO 남혜진: 아래 제미나이에게 전송할 프롬프트를 함수화, json형식으로 받아서 프론트에서 가져오기 쉽게 함
def analyzeText_Gemini(text):
    model = "gemini-2.5-flash"

    prompt = f"""
다음 게시글을 분석하라.

1. 마약 게시글일 가능성을 0~100 사이 정수로 판단하라.
2. 글에 실제로 등장한 마약 은어, 거래 관련 단어를 suspicious_words로 추출하라.
3. 글에 포함된 해시태그 중 마약 거래와 연관된 것만 hashtags로 추출하라.
4. 글에 드러난 거래 방식(비대면, 좌표, 퀵 등)을 transaction_methods로 추출하라.

주의사항
- 글에 실제로 등장한 표현만 추출할 것
- 추론으로 만들어내지 말 것
- 해당 항목이 없다면 빈 배열([])로 반환할 것

반드시 아래 JSON 형식으로만 출력하라:

    {{
    "probability": 0,
    "suspicious_words": [],
    "hashtags": [],
    "methods": []
    }}

게시글:
\"\"\"{text}\"\"\"
"""
    try:
        response = client.models.generate_content(
            model=model,
            # 남혜진: 콘텐츠로 프롬프트를 받아오겠다는 뜻
            contents=prompt
        )
        result_text = response.text.strip()
        # TODO 남혜진: 제미나이 출력 결과 콘솔에서 보기 위함, 제거해도 작동에는 이상이 없으나 문제가 생겼는지 확인 가능
        print(result_text)
        return json.loads(result_text)

    # TODO 남혜진: 만약 프로그램 실행 중 아무거나 에러 발생 시 에러 객체 변수 e에 담을 것.
    # TODO 남혜진: 제미나이 API를 무료 버전으로 사용하느라 요청이 너무 많아지면 쿼터 초과에 걸리는 문제가 발생해 작성.
    except Exception as e: 
        # TODO 남혜진: 만약 에러 메시지에 요청이 너무 많다는 의미의 429라는 문자열이 포함되어 있거나 
        # TODO 남혜진: Gemini API에서 "RESOURCE_EXHAUSTED"라는 문구가 포함돼있을 경우(API 다 써서) 실행하는 조건문
        if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
            # TODO 남혜진: 조건(AI작동/요청 정상, 쿼터 초과)에 맞을 경우 아래와 같이 처리.(Json 형식)
            return {
                "error": "QUOTA_EXHAUSTED",
                "probability": 0,
                "suspicious_words": [],
                "hashtags": [],
                "methods": []
            }
        
        # TODO 남혜진: 기타 AI 호출 중 문제 발생(네트워크 오류, 응답 파싱 실패, 내부 에러 등...)
        return {
            "error": "AI_ERROR",
            # TODO 남혜진: 에러를 문자열 타입으로 변환 후 메시지라는 키에 담음. 
            "message": str(e),
            "probability": 0,
            "suspicious_words": [],
            "hashtags": [],
            "methods": []
        }