# flask 앱을 생성하고 블루프린트 등록, 서버 실행 등의 역할을 맡은 파일입니다.
# 남혜진 작업 파일
from flask import Flask, render_template, request, jsonify
from api.routes import bp
from api.gemini import analyzeText_Gemini
from api.gemini import search_slang_with_gemini

DRUG_KEYWORDS = {
    "필로폰": ["아이스", "작대기", "히로뽕"],
    "대마초": ["대마", "weed", "420"],
    "코카인": ["코카인", "화이트"]
}

def guess_drug_kind(words):
    scores = {}

    for drug, keywords in DRUG_KEYWORDS.items():
        score = 0
        for w in words:
            for k in keywords:
                if k in w:
                    score += 1
        scores[drug] = score

    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "특정 불가"

app = Flask(__name__)
app.register_blueprint(bp)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/textAno')
def textAno():
    # 백엔드에서 계산된 값 (실제 로직은 분석 결과에 따라 달라져야 함)
    # 아래는 단순 테스트용입니다.
    
    # 1. 마약 종류 분석 결과 (예: 점수 85)
    score_from_analysis = 85 
    if score_from_analysis >= 90:
        drug_kind = "코카인"
    elif score_from_analysis >= 80:
        drug_kind = "필로폰"
    else:
        drug_kind = "아편"
        
    # 2. 확률 분석 결과 (예: 80%)
    drug_prob = 80
    
    # 두 변수를 HTML 템플릿으로 전달합니다.
    return render_template(
        'textAno.html',
        drug_prob=drug_prob,
        drug_kind=drug_kind
    )
    
@app.route('/drugDict')
def drugDict():
    return render_template('drugDict.html')

@app.route('/report')
def report():
    return render_template('report.html')

# 분석 API 엔드포인트 추가
@app.route('/api/analyzeText', methods=['POST'])
def analyzeText():
    # 클라이언트(JS)로부터 JSON 데이터를 받음
    data = request.get_json()
    text_to_analyze = data.get('text', '')

    # 너무 짧으면 AI 호출 X, quota 절약을 위함
    if len(text_to_analyze.strip()) < 10:
        return jsonify({
            "ai_used": False,
            "probability": 0,
            "drug_kind": "특정 불가",
            "suspicious": {
                "words": [],
                "hashtags": [],
                "methods": []
            },
            "message": "텍스트가 너무 짧음"
        })
    
    ai_result = analyzeText_Gemini(text_to_analyze)
    
    prob_score = ai_result.get("probability", 0)

    suspicious = {
        "words": ai_result.get("suspicious_words", []),
        "hashtags": ai_result.get("hashtags", []),
        "methods": ai_result.get("methods", [])
    }

    drug_kind = guess_drug_kind(suspicious["words"])
                
    # JSON 응답 생성
    if ai_result.get("error") == "QUOTA_EXHAUSTED":
        return jsonify({
            "ai_used": False,
            "probability": prob_score,
            "drug_kind": drug_kind,
            "message": "AI 사용량 초과 — 룰 기반 분석만 수행",
            "suspicious": suspicious
        })

    # 정상 응답
    return jsonify({
        "ai_used": True,
        "probability": prob_score,
        "drug_kind": drug_kind,
        "suspicious": suspicious
    })

# 은어 사전 부분

@app.route('/api/slangSearch', methods=['POST'])
def slang_search():
    data = request.get_json()
    term = data.get("term", "").strip()

    if not term:
        return jsonify({"error": "term required"}), 400

    result = search_slang_with_gemini(term)
    return jsonify(result)

# 배포 전 코드
#if __name__ == '__main__':
#    print("start")
#   app.run(debug=True)

# 배포 후 코드
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)