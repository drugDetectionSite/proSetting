# INSERT, SELECT, DELETE, UPDATE 등 데이터를 조작하는 함수를 넣는 파일입니다.
# SQL을 직접 실행하거나 ORM을 호출할 수 있으며 DB와 상호작용 가능합니다.
# 백엔드팀 정유림님 작성 코드

from .db import execute_query, fetch_all
import json

# 1. 사용자 은어를 추가하는 함수 (3-2 테이블)
def add_new_slang(term, definition, category, drug_code):
    # DB 삽입 코드
    sql = "INSERT INTO tbl_User_Slangs (UserTerm, UserDefinition, UserCatagory, DrugType) VALUES (%s, %s, %s, %s)"
    # sql에 채워넣을 파트
    values = (term, definition, category, drug_code)
    # db.py에 있는 execute_query에게 실행
    execute_query(sql, values) 
    
    print(f"'{term}' 은어 추가 완료")

# 2. 사용자 마약 데이터를 추가하는 함수 (3-1 테이블)
def add_user_drug_data(text, source, sns):
    # DB 삽입 코드 
    sql = """
        INSERT INTO tbl_User_Drug_Data (UserText, InputSourceType, SNSType)
        VALUES (%s, %s, %s)
    """
    # sql에 채워넣을 파트
    values = (text, source, sns)
    
    # db.py에 있는 execute_query에게 실행
    execute_query(sql, values)
    
    print("마약 데이터 저장 완료")

# 3. 저장된 은어들을 조회하는 함수
def show_all_slangs():
    # 1) 실행할 SQL 문 준비
    sql = "SELECT * FROM tbl_User_Slangs"
    
    # 2) fetch_all을 사용하여 데이터를 rows에 저장
    rows = fetch_all(sql)
    
    # 3) 가져온 데이터를 화면에 출력
    print("\n--- 현재 저장된 사용자 은어 목록 ---")
    if rows:
        for row in rows:
            print(f"\n단어: {row[2]}")  # 마약 단어
            print(f"뜻: {row[3]}")     # 마약 정의
            print(f"유의어: {row[4]}")  #관련 단어
            print(f"예시: {row[5]}")    # 예시
    else:
        print("저장된 데이터가 없습니다.")

# 4. 마약 종류 리스트를 조회하는 함수 (1-1 테이블)
def show_drug_list():
    # 1) SQL 작성 (필요한 컬럼 3개만 선택)
    sql = "SELECT DrugWord, DrugEffect, DrugToxicity FROM tbl_Drug_Types"
    
    # 2) fetch_all로 데이터 가져오기
    rows = fetch_all(sql)
    
    print("\n--- 등록된 마약 종류 ---")
    
    # 3) 결과 출력
    for row in rows:
            print(f"이름: {row[2]}")
            print(f"\n효과: {row[3]}")
            print(f"\n위험도: {row[4]}")

# 5. 마약 종류 리스트를 조회하는 함수 (1-1 테이블)
def show_drug_details():
    # 1) SQL 작성
    sql = "SELECT DrugWord, DrugEffect, DrugToxicity FROM tbl_Drug_Types"
    
    # 2) fetch_all을 사용하여 데이터를 한 번에 가져옴
    rows = fetch_all(sql)
    
    print("\n--- 등록된 마약 상세 정보 ---")
    
    # 3) 결과 출력
    for row in rows:
            print(f"이름: {row[2]}")
            print(f"\n효과: {row[3]}")
            print(f"\n위험도: {row[4]}")

# 6. AI(Gemini)가 분석한 결과를 저장하는 함수 (2-2 테이블)
def add_ai_detection(json_response):
    try:
        # 1) 문자열 형태의 JSON을 파이썬 딕셔너리로 변환
        data = json.loads(json_response)

        # 2) DB 테이블 구조에 맞춘 SQL 작성
        sql = """
            INSERT INTO tbl_Slang_Detection (InputText, LLM_Reason, DataType)
            VALUES (%s, %s, %s)
        """

        # 3) 딕셔너리에서 데이터를 꺼내서 values로 묶음
        values = (
            data.get('input_text'), # 분석한 원문
            data.get('reason'),     # 판단 근거
            data.get('result')      # 최종 결과 (정상/의심 등)
        )

        # 4) db.py의 함수를 이용해 실제 DB 저장 실행
        execute_query(sql, values)

        print("AI 분석 결과가 성공적으로 저장")

    except Exception as e:
        print(f" 결과 저장 중 오류 발생: {e}")

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