import logging

from app.models.model import Client
from app.utils.core import db
from app.utils.response import ResponseCode, ResMsg
from app.utils.util import route
from flask import Blueprint
from flask import request

bp = Blueprint("api_trade", __name__, url_prefix='/trade')
logger = logging.getLogger(__name__)


@route(bp, '/add', methods=["PUT"])
def add():
    res = ResMsg()

    obj = request.get_json(force=True)
    if not obj:
        res.update(code=ResponseCode.InvalidParameter)
        return res.data

    client_obj = Client.query.filter(Client.id == obj.get("id")).first()
    if not client_obj:
        res.update(code=ResponseCode.NoResourceFound)
        return res.data

    client_obj.trade = True
    db.session.commit()
    return res.data
