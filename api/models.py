# INSERT, SELECT, DELETE, UPDATE 등 데이터를 조작하는 함수를 넣는 파일입니다.
# SQL을 직접 실행하거나 ORM을 호출할 수 있으며 DB와 상호작용 가능합니다.
# 유림님 코드 받아야됨
from db import get_db
import re

# 1. 사용자 은어를 추가하는 함수 (3-2 테이블)
def add_new_slang(term, definition, category, drug_code):
    conn = get_db()
    if conn:
        cursor = conn.cursor()
        # 어떤 칸에 데이터를 넣을지에 대한 결정
        sql = """
            INSERT INTO tbl_User_Slangs (UserTerm, UserDefinition, UserCatagory, DrugType)
            VALUES (%s, %s, %s, %s)
        """
        # %s 자리에 들어갈 실제 데이터
        values = (term, definition, category, drug_code)
        
        cursor.execute(sql, values)
        conn.commit()  # DB 저장
        
        print(f"'{term}' 은어 추가 완료")
        conn.close()

# 2. 사용자 마약 데이터를 추가하는 함수 (3-1 테이블)
def add_user_drug_data(text, source, sns):
    conn = get_db()
    if conn:
        cursor = conn.cursor()
        sql = """
            INSERT INTO tbl_User_Drug_Data (UserText, InputSourceType, SNSType)
            VALUES (%s, %s, %s)
        """
        values = (text, source, sns)
        
        cursor.execute(sql, values) # SQL 쿼리를 실행 후 결과 가지고 오는 코드
        conn.commit() # DB 저장
        
        print("마약 데이터 저장")
        conn.close()

# 3. 저장된 은어들을 구경(조회)하는 함수
def show_all_slangs():
    conn = get_db()
    if conn:
        cursor = conn.cursor()
        # 모든 은어 정보를 가져오는 명령어
        cursor.execute("SELECT * FROM tbl_User_Slangs")
        
        rows = cursor.fetchall() # 모든 줄을 다 가져오는 코드
        
        print("\n--- 현재 저장된 사용자 은어 목록 ---")
        for row in rows:
            print(f"\n단어: {row[2]}") # 마약 단어
            print(f"\n뜻: {row[3]}") # 마약 정의
            print(f"\n유의어: {row[4]}") #관련 단어
            print(f"\n예시: {row[5]}") # 예시
            
        conn.close()

# 4. 마약 종류 리스트를 조회하는 함수 (1-1 테이블)
def show_drug_types():
    conn = get_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT DrugWord, DrugEffect, DrugToxicity FROM tbl_Drug_Types")
        
        rows = cursor.fetchall()
        print("\n--- 등록된 마약 종류 ---")
        for row in rows:
            print(f"이름: {row[2]}")
            print(f"\n효과: {row[3]}")
            print(f"\n위험도: {row[4]}")
            
        conn.close()

# 5. AI(Gemini)가 분석한 결과를 저장하는 함수 (2-2 테이블)
def add_ai_detection(json_response):
    conn = get_db()
    if conn:
        cursor = conn.cursor()
        
        # 1) 파이썬 딕셔너리로 변경
        data = json.loads(json_response)
        
        # 2) DB 테이블(tbl_Slang_Detection) 구조에 맞춰서 작성
        sql = """
            INSERT INTO tbl_Slang_Detection (InputText, LLM_Reason, DataType)
            VALUES (%s, %s, %s)
        """
        
        # 3) JSON의 키(Key) 이름을 확인해서 매칭
        # 예: 프롬프트에 설정한 이름 유지
        values = (
            data.get('input_text'), 
            data.get('reason'), 
            data.get('result')
        )
        
        cursor.execute(sql, values)
        conn.commit()
        
        print("Gemini의 AI 분석 결과가 저장")
        conn.close()

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
