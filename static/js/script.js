document.addEventListener('DOMContentLoaded', function() {  
    // 조건에 따라 변경될 변수 정의
    let score = 85;
    let drugKind; // 여기에 조건에 맞는 단어가 들어갈 변수

    // 조건에 따른 단어 할당 (if/else 또는 삼항 연산자 사용)
    if (score >= 90) {
        drugKind = "코카인";
    } else if (score >= 80) {
        drugKind = "필로폰";
    } else {
        drugKind = "아편";
    }

    const kindMessage = drugKind + "의 가능성이 있음";
    const kindMessageOut = document.getElementById('kindMessage');
    if (kindMessageOut) {
        kindMessageOut.textContent = kindMessage;
    }
});

document.addEventListener('DOMContentLoaded', function() {
    let drugProbInt = 80;
    let probResult = "";
    let className = "";

    if (drugProbInt >= 80) {
        probResult = "아주 높습니다";
        className = "probVeryHigh"
    } else if (drugProbInt >= 60) {
        probResult = "높습니다";
        className = "probHigh"
    } else if (drugProbInt >= 40) {
        probResult = "보통입니다";
        className = "probMedium"
    } else {
        probResult = "낮습니다";
        className = "probLow"
    }

    const drugProbMessage = "이 게시글은 마약 게시글일 가능성이 " + drugProbInt + "%로 <span class='" + className + "'>" + probResult + "</span>";
    const probResultMessage = document.getElementById('drugProbMessage');
    if (probResultMessage) {
        probResultMessage.innerHTML = drugProbMessage;
    }
});

document.addEventListener('DOMContentLoaded', function() {
    // 1. 필요한 HTML 요소 가져오기
    const textBox = document.getElementById('textBox1');
    const kindMessageOut = document.getElementById('kindMessage');
    const probResultMessage = document.getElementById('drugProbMessage');

    // 2. 비동기 분석 함수 정의
    function analyzeText(text) {
        // 입력된 텍스트가 없으면 초기 상태로 복귀하거나 분석을 중단
        if (text.trim() === "") {
            if (kindMessageOut) kindMessageOut.textContent = "분석 대기 중";
            if (probResultMessage) probResultMessage.textContent = "마약 거래 게시글 가능성 분석";
            return;
        }

        fetch('/api/analyze-text', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: text }), // 입력 텍스트를 JSON으로 서버에 전송
        })
        .then(response => response.json()) // 응답을 JSON 객체로 파싱
        .then(data => {
            // 서버에서 받은 데이터(data.probability, data.drug_kind 등)를 사용
            let className = "";
            if (data.prob_result_text === "아주 높습니다") className = "probVeryHigh";
            else if (data.prob_result_text === "높습니다") className = "probHigh";
            else if (data.prob_result_text === "보통입니다") className = "probMedium";
            else className = "probLow";

            // 1) 마약 종류 메시지 업데이트
            const kindMessage = data.drug_kind + "의 가능성이 있음";
            if (kindMessageOut) {
                kindMessageOut.textContent = kindMessage;
            }

            // 2) 확률 메시지 업데이트
            const drugProbMessage = "이 게시글은 마약 게시글일 가능성이 " + 
                                    data.probability + "%로 " + 
                                    data.prob_result_text;
            if (probResultMessage) {
                probResultMessage.innerHTML =
                "이 게시글은 마약 게시글일 가능성이 " +
                data.probability + "%로 " +
                "<span class='" + className + "'>" +
                data.prob_result_text +
                "</span>";
            }
        })
        .catch(error => {
            console.error('분석 요청 실패:', error);
            if (probResultMessage) probResultMessage.textContent = "분석 중 오류가 발생했습니다.";
        });
    }
    
    // 3. 텍스트 입력 이벤트 리스너 추가
    // 'input' 이벤트는 내용이 변경될 때마다(글자 입력, 삭제 등) 발생합니다.
    if (textBox) {
        textBox.addEventListener('input', (event) => {
            // 이벤트가 발생할 때마다 분석 함수를 호출
            analyzeText(event.target.value);
        });
        
        // 페이지 로드 시 초기 상태로 한 번 호출 (빈 문자열 분석)
        analyzeText(textBox.value);
    }
});

document.querySelectorAll('.toggleHeader').forEach(btn => {
    btn.addEventListener('click', () => {
        const box = btn.parentElement;
        box.classList.toggle('active');
    });
});

document.querySelectorAll('.toggleContent textarea').forEach(textarea => {
    const count = textarea.nextElementSibling;
    const MAX = 1000;

    textarea.addEventListener('input', () => {
        if (textarea.value.length > MAX) {
            textarea.value = textarea.value.slice(0, MAX); // ✅ 강제 잘라내기
        }
        count.textContent = `${textarea.value.length}/1000`;
    });
});