# api 패키지 초기화, 블루프린트 등록하는 파일입니다.
# routes.py에 정의한 블루프린트를 가져와 외부에서 사용 가능하도록 합니다.
from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # 설정 불러오기 (instance/config.py 등)
    app.config.from_pyfile('config.py', silent=True)
    
    from .routes import main_bp
    app.register_blueprint(main_bp)
    
    return app