# 커넥션 풀 유틸 함수 등 DB를 연결하는 파일입니다.
# 백엔드팀 작성 코드

import mysql.connector
from config import DB_CONFIG

# SQL을 실행하는 공통 함수
def execute_query(sql, values = None):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    try:
        if values:
            cursor.execute(sql, values)
        else:
            cursor.execute(sql)
        conn.commit()
        return True
    except Exception as e:
        print(f"SQL 실행 오류: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

# 데이터를 가져오는 공통 함수
def fetch_all(sql, values = None):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    try:
        if values:
            cursor.execute(sql, values)
        else:
            cursor.execute(sql)
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()