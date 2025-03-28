from flask import Blueprint

api_blueprint = Blueprint("api", __name__)

@api_blueprint.route("/test", methods=["GET"])
def test():
    return "API funcionando correctamente"
