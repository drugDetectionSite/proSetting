1. 파이썬 버전: 3.12.1
2. venv로 가상환경 생성하기
   2-1. 터미널에 python -m venv venv 입력
   2-2. venv\Scripts\activate 입력
   2-3. flask 패키지 설치(venv 내부에만 저장) pip install flask
   2-4. deactivate로 가상환경 비활성화
3. requirements.txt 파일 사용해 패키지 설치하는 법
   3-1. 가상환경 활성화 후 pip freeze > requirements.txt 입력(현재 설치된 패키지 목록 저장)
   3-2. requirements.txt로 패키지 설치. 다른 컴퓨터 등에서 셋업 시 해당 명령어로 한 번에 설치 가능 pip install -r requirements.txt
4. 웹 실행방법
   4-1. 웹 실행 시 파워셀에서 python app.py 입력하면 됨.
   4-2. 실행 시 뜨는
   WARNING: This is a development server.
   Do not use it in a production deployment.
   Use a production WSGI server instead.
   라는 메시지는 개발용 서버라는 뜻이므로 개발에는 지장X
   추후 배포 시 WSGI 서버 사용하는 것이 좋음.
