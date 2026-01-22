1. 파이썬 버전: 3.14.2, 처음에 3.12.1이었으나 보안 및 모듈 활용 등의 문제로 변경
2. venv로 가상환경 생성하기
   2-1. 터미널에 python -m venv venv 입력
   2-2. venv\Scripts\activate 입력
   2-3. flask 패키지 설치(venv 내부에만 저장) pip install flask
   2-4. deactivate로 가상환경 비활성화
3. requirements.txt 파일 사용해 패키지 설치하는 법
   3-1. 가상환경 활성화 후 pip freeze > requirements.txt 입력(현재 설치된 패키지 목록 저장)
   3-2. requirements.txt로 패키지 설치. 다른 컴퓨터 등에서 셋업 시 해당 명령어로 한 번에 설치 가능 pip install -r requirements.txt
4. 웹 실행방법
   4-1. 웹 실행 시 파워셀에서 python app.py 입력하면 됨. 결과로 뜨는 http://127.0.0.1:5000 이라는 링크 컨트롤+마우스 좌클릭
   4-2. 실행 시 뜨는
   WARNING: This is a development server.
   Do not use it in a production deployment.
   Use a production WSGI server instead.
   라는 메시지는 개발용 서버라는 뜻이므로 개발에는 지장X
   추후 배포 시 WSGI 서버 사용하는 것이 좋음.

- 4번 실행 불가할 경우

1. cmd나 파워셀에 venv\Scripts\activate 코드 입력해 가상환경 활성화. 앞에 (venv) 표시 뜨는지 확인
2. pip install flask로 플라스크 설치
   2-1. pip list로 설치 확인 가능(flask가 있는지)
3. 4번 다시 실행

- venv 파일 삭제 이유: 저장공간 문제, 호환 문제 가능성, 보안 문제 등
  -> gitignore 파일에 venv 추가, gitignore 파일은 깃허브에 올리지 않을 파일이나 폴더 목록들을 담는 곳. gitignore파일은 건드리시면 안 됩니다.
  -> venv 대신 패키지 목록만 기록한 requirements.txt 공유

5. 깃허브 작업 간단 설명

- 풀 리퀘스트(pull request): 변경사항을 적용하고 싶을 때 사용. 풀리퀘를 했다고 바로 적용되진 않는 중간단계이며 변경 혹은 취소 가능. 풀리퀘와 달리 머지 리퀘스트는 바로 적용
- 깃허브에 풀 리퀘 된 변경사항 가져오기: git pull
  -> 내가 따로 변경한 게 있어 에러가 뜨면: git restore .(현재 디렉터리)
  -> git restore 후 다시 git pull
- 깃 푸쉬하기

1. git add .
2. git commit -m "feat:프로젝트 구현한 내용 메시지"
3. git branch: 브런치명 확인
4. git push -u origin (브랜치명)
   -> 팀원들은 메인 브런치 건드리면 안 됨

- push 오류 발생 시 index파일 문제나 .lock파일로 인해 푸시가 막힌 경우도 있고 윈도우 디펜더가 방화벽으로 막느라 발생하는 등 여러 원인이 있을 수 있습니다. 직접 해결해보시고 이해가 어렵거나 해결이 안 되시면 팀장에게 문의 부탁드립니다.

'''

- 풀 리퀘스트 하기(마스터 건드리지 X)
  -> 푸쉬 후 풀 리퀘스트로 깃허브에 저장. 깃허브 사이트 새로고침

1. 깃허브 사이트 접속 -> 좌상단 메뉴 -> 레포지토리 들어가기(지금 하는 작업은 Repositories의 drugDetectionSite/proSetting 클릭)
2. 네비케이션의 pull requests 클릭
3. 초록색 버튼인 New pull requests 클릭
4. compare: (브랜치명)의 Branches에서 푸쉬된 거 선택
5. 활성화 된 초록 버튼 create pull request 클릭
6. 내용에 -closes #(이슈 번호) 작성, 그 다음 내용은 자유롭게 첨언
   -> ex. -closes #5면 5번 이슈를 해결했으니 제거해달라는 뜻
7. 마지막으로 create pull request 클릭!
   '''

'''
남이 한 거 가져오기(처음하는 경우 1번, 아니면 2번부터)

1. 클론 먼저 하기

- clone: 깃허브 Repository에 있는 파일 내 로컬 컴퓨터로 복사해오는 작업.

- 리포지토리 주소 복사하여 git bash에서 작업하는 위치 정한 후 git clone 명령어로 복제
  https://ittrue.tistory.com/91

- Git Bash에서 저장할 공간 정하기 - pwd 명령어를 통해 현재 위치 확인 후 cd 명령어로 이동 후 clone

2. 가져올 브랜치 만들거나 기존 원하는 브랜치로 옮김

- 메인 브랜치 내용을 가져온다면 터미널에 git checkout main 입력

- git branch 브랜치명: 브랜치 생성

- git checkout -b 브랜치명: 브랜치를 생성하면서 옮기기

- git checkout 브랜치명: 브랜치 가져오기

3. pull 받아오기

- git pull origin (브런치 이름)

4. 새 브랜치 생성

- 브랜치 새로 만들어두면 망쳐도 되돌리기 쉬움
- git branch (브랜치명): 브랜치 만들기만 됨
- git checkout -b (브랜치명): 브랜치 만들고 그 브랜치로 이동
- 브랜치명은 보통 feat/작업할내용 으로 함.

* 번외: git fetch나 git log로 내역 볼 수 있음
