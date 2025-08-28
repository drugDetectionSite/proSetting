from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # 설정 불러오기 (instance/config.py 등)
    app.config.from_pyfile('config.py', silent=True)
    
    from .routes import main_bp
    app.register_blueprint(main_bp)
    
    return app