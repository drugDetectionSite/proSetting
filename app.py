from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/textAno')
def textAno():
    # 백엔드에서 계산된 값 (실제 로직은 분석 결과에 따라 달라져야 함)
    
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

# 새로운 분석 API 엔드포인트 추가
@app.route('/api/analyze-text', methods=['POST'])
def analyze_text():
    # 클라이언트(JS)로부터 JSON 데이터를 받음
    data = request.get_json()
    text_to_analyze = data.get('text', '')
    
    # ----------------------------------------------------
    # 💡 실제 분석 및 계산 로직을 여기에 구현해야 합니다.
    # 아래는 테스트를 위한 임시 계산 로직입니다.
    # ----------------------------------------------------
    
    # 텍스트 길이에 따라 확률(prob) 계산 (테스트용)
    prob_score = min(len(text_to_analyze) * 5, 100) # 최대 100%
    
    # 확률 점수에 따라 마약 종류(kind) 결정 (테스트용)
    if prob_score >= 90:
        kind = "코카인"
    elif prob_score >= 80:
        kind = "필로폰"
    elif prob_score >= 40:
        kind = "대마초" # 40~79점대를 위한 새로운 값 추가
    else:
        kind = "아편"

    # 확률 점수에 따라 결과 문구(result_text) 결정
    if prob_score >= 80:
        result_text = "아주 높습니다"
    elif prob_score >= 60:
        result_text = "높습니다"
    elif prob_score >= 40:
        result_text = "보통입니다"
    else:
        result_text = "낮습니다"
        
    # JSON 응답 생성
    return jsonify({
        'probability': prob_score,
        'drug_kind': kind,
        'prob_result_text': result_text
    })


if __name__ == '__main__':
    print("start")
    app.run(debug=True)