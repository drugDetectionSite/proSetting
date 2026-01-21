// 남혜진 작업 파일

// 가장 가능성 높은 마약 종류 출력
document.addEventListener('DOMContentLoaded', function () {

    //1. DOM 요소
    const textBox = document.getElementById('textBox1');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const kindMessageOut = document.getElementById('kindMessage');
    const probResultMessage = document.getElementById('drugProbMessage');

    //2. 초기 UI 상태
    if (kindMessageOut) kindMessageOut.textContent = "분석 대기 중";
    if (probResultMessage) {
        probResultMessage.textContent = "마약 거래 게시글 가능성 분석";
    }

    //3. 상태 변수
    let isLoading = false;
    let requestId = 0;

    //4. 분석 함수 (단 하나)
    function analyzeText(text) {
        if (isLoading) return;
        // 빈 텍스트 차단을 위함, 최소 길이 조건
        if (!text || text.trim().length < 3) {
            alert("텍스트를 3자 이상 입력해주세요");
            return;
        }

        isLoading = true;
        const currentId = ++requestId;

        fetch('/api/analyzeText', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text })
        })
        .then(res => res.json())
        .then(data => {
            if (currentId !== requestId) return;

            const prob = Number(data.probability);
            renderSuspiciousParts(data.suspicious);

            let probText = "낮습니다";
            let className = "probLow";

            if (prob >= 80) {
                probText = "아주 높습니다";
                className = "probVeryHigh";
            } else if (prob >= 60) {
                probText = "높습니다";
                className = "probHigh";
            } else if (prob >= 40) {
                probText = "보통입니다";
                className = "probMedium";
            }
            kindMessageOut.textContent = `${data.drug_kind}의 가능성이 있음`;
            probResultMessage.innerHTML =
                    `이 게시글은 마약 게시글일 가능성이 ${prob}%로 
                    <span class="${className}">${probText}</span>`;
        })
        .catch(err => {
            console.error(err);
            probResultMessage.textContent = "분석 중 오류가 발생했습니다.";
        })
        .finally(() => {
            isLoading = false;
        });
    }

    /*
       5. 입력 이벤트 + debounce
    */
    analyzeBtn.addEventListener('click', () => {
        analyzeText(textBox.value);
    });
});

// toggleHeader 클릭 시 변화
document.querySelectorAll('.toggleHeader').forEach(btn => {
    btn.addEventListener('click', () => {
        btn.parentElement.classList.toggle('active');
    });
});

// toggleContent의 글자 숫자 카운트 세기
document.querySelectorAll('.toggleContent textarea').forEach(textarea => {
    const count = textarea.nextElementSibling;
    const MAX = 1000;

    textarea.addEventListener('input', () => {
        if (textarea.value.length > MAX) {
            textarea.value = textarea.value.slice(0, MAX);
        }
        count.textContent = `${textarea.value.length}/1000`;
    });
});

function renderSuspiciousParts(suspicious) {
    console.log("RENDER suspicious:", suspicious);

    const wordEl = document.getElementById('words');
    const hashEl = document.getElementById('hashtags');
    const methodEl = document.getElementById('methods');

    console.log("DOM CHECK:", wordEl, hashEl, methodEl);

    if (!wordEl || !hashEl || !methodEl) {
        console.error("suspicious DOM 요소 못 찾음");
        return;
    }

    wordEl.textContent =
        suspicious.words && suspicious.words.length
            ? suspicious.words.join(", ")
            : "없음";

    hashEl.textContent =
        suspicious.hashtags && suspicious.hashtags.length
            ? suspicious.hashtags.join(", ")
            : "없음";

    methodEl.textContent =
        suspicious.methods && suspicious.methods.length
            ? suspicious.methods.join(", ")
            : "없음";
}