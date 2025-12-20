# INSERT, SELECT, DELETE, UPDATE 등 데이터를 조작하는 함수를 넣는 파일입니다.
# SQL을 직접 실행하거나 ORM을 호출할 수 있으며 DB와 상호작용 가능합니다.
# 유림님 코드 받아야됨
from api.db import get_db

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
def insert_user_drug_data(data):
    print("[DEBUG] insert_user_drug_data 호출됨:", data)
    return True