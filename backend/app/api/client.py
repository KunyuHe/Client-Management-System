import logging

from app.models.model import User, Client, Income
from app.utils.auth import login_required
from app.utils.core import db
from app.utils.emailsender import EmailSender
from app.utils.response import ResponseCode, ResMsg
from app.utils.util import route, model_to_dict, EmailTool
from flask import Blueprint, session
from flask import request

bp = Blueprint("api_client", __name__, url_prefix='/client')
logger = logging.getLogger(__name__)


@route(bp, '/add', methods=["POST"])
@login_required
def add():
    res = ResMsg()

    user_name = session["user_name"]
    user_obj = User.query.filter(User.name == user_name).first()

    obj = request.get_json(force=True)
    if not all([obj, obj.get("name"), obj.get("email")]):
        res.update(code=ResponseCode.InvalidParameter)
        return res.data

    # 将客户添加到指定用户管理列表中
    client_obj = Client.query.filter(
        Client.name == obj.get("name")).first()
    if client_obj:
        client_obj.users.append(user_obj)
        db.session.commit()
        return res.data

    valid_email = EmailTool.check_email(obj.get("email"))
    if not valid_email:
        res.update(code=ResponseCode.InvalidEmail)
        return res.data

    # 添加新客户记录
    client_obj = Client(**obj, users=[user_obj])
    db.session.add(client_obj)
    db.session.commit()
    res.update(data=model_to_dict(client_obj))

    return res.data


@route(bp, '/remove', methods=["DELETE"])
@login_required
def remove():
    res = ResMsg()

    obj = request.get_json(force=True)
    if not obj or not obj.get("id"):
        res.update(ResponseCode.InvalidParameter)
        return res.data

    client_obj = Client.query.filter(Client.id == obj.get("id")).first()
    if not client_obj:
        res.update(ResponseCode.NoResourceFound)
        return res.data

    client_obj.users.clear()
    db.session.delete(client_obj)
    db.session.commit()

    return res.data


@route(bp, '/incomes', methods=["POST"])
@login_required
def get_incomes():
    res = ResMsg()

    obj = request.get_json(force=True)
    client_id = obj.get("id")
    if not obj or not client_id:
        res.update(ResponseCode.InvalidParameter)
        return res.data

    client_obj = Client.query.filter(Client.id == client_id).first()
    if not client_obj:
        res.update(code=ResponseCode.NoResourceFound)
        return res.data

    user_obj = User.query.filter(User.name == session["user_name"]).first()
    if user_obj not in client_obj.users:
        res.update(code=ResponseCode.AccessNotAuthorized)
        return res.data

    incomes_obj = Income.query.filter(Income.client_id == client_id).order_by(
        Income.date)
    income_json = model_to_dict(incomes_obj)
    res.update(data={key: [pair[key] for pair in income_json]
                     for key in ('date', 'value')})
    return res.data


@route(bp, '/email', methods=["POST"])
@login_required
def email_client():
    res = ResMsg()

    user_name = session["user_name"]
    client_id = request.form.get("id")
    logger.info(request.form)
    if not user_name or not client_id:
        res.update(code=ResponseCode.InvalidParameter)
        return res.data

    user_obj = User.query.filter(User.name == user_name).first()
    client_obj = Client.query.filter(Client.id == client_id).first()
    if not client_obj:
        res.update(code=ResponseCode.NoResourceFound)
        return res.data
    if user_obj not in client_obj.users:
        res.update(code=ResponseCode.AccessNotAuthorized)
        return res.data

    subject = request.form.get("subject", None)
    if not subject or subject == "undefined":
        subject = "估值表"
    body = request.form.get("body", None)
    if not body or body == "undefined":
        body = (f"尊敬的{client_obj.name}:\n\n"
                f"用户{user_obj.name}通过管理系统为您发送了估值表。请查收！\n\n"
                f"如有任何问题，请联系{user_obj.email}。\n\n"
                f"祝好，\n客户管理系统（CMS）")

    file = request.files.get('file', None)
    if file:
        result = EmailSender.send_email(client_obj.email, subject, body,
                                        file.stream.read(), file.filename)
    else:
        result = EmailSender.send_email(client_obj.email, subject, body)

    if not result:
        res.update(code=ResponseCode.SendEmailFailed)
        return res.data

    return res.data


# TODO: Add admin role
@route(bp, '/testRemoveAll', methods=["DELETE"])
def remove_all():
    """
    移除所有客户以及多对多关系
    """
    res = ResMsg()

    for client in Client.query:
        client.users.clear()
    Client.query.delete()
    db.session.commit()

    return res.data


@route(bp, '/testGetAll', methods=["GET"])
def get_all():
    res = ResMsg()

    clients_json = [{**model_to_dict(client),
                     'users': model_to_dict(client.users)}
                    for client in Client.query]
    res.update(data=clients_json)

    return res.data
