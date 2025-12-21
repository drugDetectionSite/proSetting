# 커넥션 풀 유틸 함수 등 DB를 연결하는 파일

def get_db():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"DB 연결 실패: {e}")
        return None
