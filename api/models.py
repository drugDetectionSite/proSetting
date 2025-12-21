# INSERT, SELECT, DELETE, UPDATE 등 데이터를 조작하는 함수를 넣는 파일입니다.
# SQL을 직접 실행하거나 ORM을 호출할 수 있으며 DB와 상호작용 가능합니다.
# 유림님 코드 받아야됨
from api.db import get_db
import re

'''
def insert_post(content):
    conn = get_db()
    try:
        with conn.cursor() as cur:
            sql = "INSERT INTO drug_posts (content) VALUES (%s)"
            cur.execute(sql, (content,))
        conn.commit()
    finally:
        conn.close()

def get_posts():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM drug_posts ORDER BY id DESC")
    result = cur.fetchall()

    cur.close()
    conn.close()
    return result

def delete_post(post_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("DELETE FROM drug_posts WHERE id = %s", (post_id,))
    conn.commit()

    cur.close()
    conn.close()

def get_post(post_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM drug_posts WHERE id = %s", (post_id,))
    result = cur.fetchone()

    cur.close()
    conn.close()
    return result
'''

SUSPICIOUS_WORDS = {
    "words": ["직거래", "퀵", "던짐", "좌표", "샘플", "비대면", "연락"],
    "hashtags": ["#던짐", "#퀵거래", "#직거래", "#비대면"],
    "methods": ["퀵거래", "좌표 전달", "비대면 거래", "던짐 방식"]
}

def extract_suspicious_parts(text):
    result = {
        "words": [],
        "hashtags": [],
        "methods": []
    }

    for key, keywords in SUSPICIOUS_WORDS.items():
        for word in keywords:
            if word in text:
                result[key].append(word)

    return result

def insert_user_drug_data(data):
    print("[DEBUG] insert_user_drug_data 호출됨:", data)
    return True