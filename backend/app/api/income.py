import logging

from app.models.model import Income, Client
from app.utils.core import db
from app.utils.response import ResponseCode, ResMsg
from app.utils.util import route
from flask import Blueprint
from flask import request

bp = Blueprint("api_income", __name__, url_prefix='/income')
logger = logging.getLogger(__name__)


@route(bp, '/add', methods=["POST"])
def add():
    res = ResMsg()

    obj = request.get_json(force=True)
    if not (obj, obj.get("client_id"), obj.get("value")):
        res.update(ResponseCode.InvalidParameter)
        return res.data

    client_obj = Client.query.filter(Client.id == obj.get("client_id")).first()
    if not client_obj:
        res.update(ResponseCode.NoResourceFound)
        return res.data

    income_obj = Income(**obj)
    db.session.add(income_obj)
    db.session.commit()

    return res.data
