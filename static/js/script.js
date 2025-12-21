// 남혜진 작업 파일

// 가장 가능성 높은 마약 종류 출력
document.addEventListener('DOMContentLoaded', function () {

    //1. DOM 요소
    const textBox = document.getElementById('textBox1');
    const kindMessageOut = document.getElementById('kindMessage');
    const probResultMessage = document.getElementById('drugProbMessage');

    //2. 초기 UI 상태
    if (kindMessageOut) kindMessageOut.textContent = "분석 대기 중";
    if (probResultMessage) probResultMessage.textContent = "마약 거래 게시글 가능성 분석";

    //3. 상태 변수
    let debounceTimer = null;
    let isLoading = false;

    //4. 분석 함수 (단 하나)
    function analyzeText(text) {
        if (isLoading) return;
        if (!text || text.trim() === "") return;

        isLoading = true;

        fetch('/api/analyzeText', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text })
        })
        .then(res => res.json())
        .then(data => {
            const prob = data.probability;

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

            if (kindMessageOut) {
                kindMessageOut.textContent = `${data.drug_kind}의 가능성이 있음`;
            }

            if (probResultMessage) {
                probResultMessage.innerHTML =
                    `이 게시글은 마약 게시글일 가능성이 ${prob}%로 
                    <span class="${className}">${probText}</span>`;
            }
        })

        .catch(err => {
            console.error(err);
            if (probResultMessage) {
                probResultMessage.textContent = "분석 중 오류가 발생했습니다.";
            }
        })
        .finally(() => {
            isLoading = false;
        });
    }

    /*
       5. 입력 이벤트 + debounce
    */
    if (textBox) {
        textBox.addEventListener('input', (e) => {
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(() => {
                analyzeText(e.target.value);
            }, 1000);
        });
    }
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
    const wordEl = document.getElementById('sus-word');
    const hashEl = document.getElementById('sus-hashtag');
    const methodEl = document.getElementById('sus-method');

    if (!suspicious) {
        wordEl.textContent = "없음";
        hashEl.textContent = "없음";
        methodEl.textContent = "없음";
        return;
    }

    wordEl.textContent =
        suspicious.words?.length ? suspicious.words.join(", ") : "없음";
    hashEl.textContent =
        suspicious.hashtags?.length ? suspicious.hashtags.join(", ") : "없음";
    methodEl.textContent =
        suspicious.methods?.length ? suspicious.methods.join(", ") : "없음";
}
