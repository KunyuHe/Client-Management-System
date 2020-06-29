import logging

from flask import Blueprint
from flask import request

from app.models.model import Client
from app.utils.response import ResponseCode, ResMsg
from app.utils.util import route

bp = Blueprint("api_trade", __name__, url_prefix='/trade')
logger = logging.getLogger(__name__)


@route(bp, '/add', methods=["POST"])
def add():
    res = ResMsg()

    obj = request.get_json(force=True)
    client_obj = Client.query.filter(Client.name == obj.get("name")).first()
    if not obj or not client_obj:
        res.update(ResponseCode.InvalidParameter)
        return res.data

    for user in client_obj.users:
        # Emit message to the users
        pass

    return res.data
