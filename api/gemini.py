# 저희가 gemini를 활용하므로 만든 파일입니다.
# Gemini(llm)를 호출하며 DB 저장 로직은 여기서 안 하고 분석 결과만 반환합니다.

# 백앤드팀 정유림님 작성 코드(Gemini 호출 코드)

from google import genai
import os
# 수정 남혜진: .env에서 제미나이 키 호출을 위함
from dotenv import load_dotenv
load_dotenv()

# 키 직접 노출 방지를 위한 우회, 환경 변수 값을 가져옴.
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key = GEMINI_API_KEY)

# 수정 남혜진: 서버는 계속 실행될 수 있는데 1)아래 방식은 한 번만 실행
# 수정 남혜진: 2) 사용자가 보낸 게시글 text가 AI에 들어가지 않음
# 수정 남혜진: 따라서 아래와 같은 함수 형식으로 수정하였습니다.1) 함수생성, 2)contents 변수에 프롬프트 넣음
"""
model="gemini-2.5-flash"

response = client.models.generate_content(
    model = model, contents = "Explain how AI works in a few words"
)


print(response.text)
"""
# 안에 들어가는 f""" """ 부분은 주석이 아닌 멀티라인 문자열
def analyzeText_Gemini(text):
    model = "gemini-2.5-flash"

    prompt = f"""
너는 대한민국 마약 거래 게시글 탐지 AI다.

아래 게시글을 분석해서
1️⃣ 마약 거래 의심 확률을 0~100 숫자로만 출력하고
2️⃣ 가장 의심되는 마약 종류를 하나만 출력해라.

마약 종류 예시:
대마초, 필로폰, 코카인, LSD, MDMA, 기타, 없음

출력 형식 (반드시 지켜):
확률:숫자
종류:마약이름

게시글:
\"\"\"{text}\"\"\"
"""

    response = client.models.generate_content(
        model=model,
        contents=prompt
    )
    return response.text
