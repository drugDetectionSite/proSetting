# DB 접속 코드 등 전반적인 설정이 담긴 파일입니다.

# 백앤드팀 작업 코드(DB 접속 코드)

import mysql.connector
import os
# .env파일은 자동으로 읽히지 않으므로 해당 모듈을 불러와서 .env파일을 읽을 수 있게 함.
from dotenv import load_dotenv
# .env에 숨겨둔 키를 가져와줍니다.
load_dotenv()

# TODO 프론트: 보안을 위해 환경변수를 지정하였습니다.
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PW"),
    "database": os.getenv("DB_NAME")
}

# DB 연결해주는 함수
def get_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        print("연결 성공")
        return conn
    except Exception as e:
        print("연결 실패:", e)
        return None

# 키 노출 방지를 위한 변수 활용
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")