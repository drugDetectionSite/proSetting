# 커넥션 풀 유틸 함수 등 DB를 연결하는 파일입니다.
# 유림님 작성할 곳
from model import add_new_slang, show_all_slangs, extract_suspicious_parts

def get_db():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"DB 연결 실패: {e}")
        return None
