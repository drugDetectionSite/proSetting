# Flask Blueprint로 앤드포인트를 정의하는 파일입니다.
# 프론트앤드와의 HTTP 인터페이스를 제공합니다.
# 요청을 받으면 비즈니스 로직을 호출합니다.

# 프론트팀 작업 파일
from flask import Blueprint, request
from api.models import insert_user_drug_data

bp = Blueprint("api", __name__)

@bp.route("/detect", methods=["POST"])
def detect():
    data = request.json

    insert_user_drug_data(
        user_text=data["text"],
        input_source="web",
        sns_type="sns",
        result="의심"
    )

    return {"result": "ok"}