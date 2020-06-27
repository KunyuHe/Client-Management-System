import logging

from app.models.model import User, Customer
from app.utils.auth import Auth, login_required
from app.utils.core import db
from app.utils.emailsender import EmailSender
from app.utils.response import ResMsg, ResponseCode
from app.utils.util import model_to_dict, route, EmailTool, PhoneTool
from flask import Blueprint, session, request

bp = Blueprint("api_user", __name__, url_prefix='/user')
logger = logging.getLogger(__name__)


@route(bp, '/register', methods=["POST"])
def register():
    res = ResMsg()

    obj = request.get_json(force=True)
    name = obj.get("name")
    email = obj.get("email")
    phone = obj.get("phone")
    if not all([obj, name, email, phone]):
        res.update(code=ResponseCode.InvalidParameter)
        return res.data

    valid_email = EmailTool.check_email(email)
    if not valid_email:
        res.update(code=ResponseCode.InvalidEmail)
        return res.data

    valid_phone = PhoneTool.check_phone(phone)
    if not valid_phone:
        res.update(code=ResponseCode.InvalidPhone)
        return res.data

    unique_name = db.session.query(User).filter(User.name == name).count() == 0
    if not unique_name:
        res.update(code=ResponseCode.RepeatUserName)
        return res.data

    user_obj = User(name=name, password=obj.get("password"),
                    phone=phone, email=email)
    db.session.add(user_obj)
    db.session.commit()

    return res.data


@route(bp, '/login', methods=["POST"])
def login():
    """登陆成功获取到数据获取token和刷新token"""
    res = ResMsg()

    obj = request.get_json(force=True)
    name = obj.get("name")
    password = obj.get("password")
    if not all([obj, name, password]):
        res.update(code=ResponseCode.InvalidParameter)
        return res.data

    user_obj = User.query.filter(User.name == name).first()
    if user_obj and user_obj.password == password:
        access_token, refresh_token = Auth.encode_auth_token(user_id=name)
        data = {
            "access_token": access_token.decode("utf-8"),
            "refresh_token": refresh_token.decode("utf-8"),
            "user": model_to_dict(user_obj)
        }
        res.update(data=data)

    else:
        res.update(code=ResponseCode.AccountOrPassWordErr)
    return res.data


@route(bp, '/refresh', methods=["GET"])
def refresh_token():
    """刷新token，获取新的access token"""
    res = ResMsg()

    refresh_token = request.args.get("refresh_token")
    if not refresh_token:
        res.update(code=ResponseCode.InvalidParameter)
        return res.data

    payload = Auth.decode_auth_token(refresh_token)
    # token被串改或过期
    if not payload:
        res.update(code=ResponseCode.PleaseSignIn)
        return res.data

    # 判断token正确性
    if "user_id" not in payload:
        res.update(code=ResponseCode.PleaseSignIn)
        return res.data

    # 获取新的token
    access_token = Auth.generate_access_token(user_id=payload["user_id"])
    data = {"access_token": access_token.decode("utf-8"),
            "refresh_token": refresh_token}
    res.update(data=data)

    return res.data


@route(bp, '/info', methods=["GET"])
@login_required
def get_info():
    res = ResMsg()

    name = session["user_name"]
    user_obj = User.query.filter(User.name == name).first()
    res.update(data=model_to_dict(user_obj))

    return res.data


@route(bp, '/customers', methods=["GET"])
@login_required
def get_customers():
    res = ResMsg()

    name = session["user_name"]
    user_obj = User.query.filter(User.name == name).first()
    res.update(data=model_to_dict(user_obj.customers))

    return res.data


@route(bp, '/email', methods=["POST"])
@login_required
def send_email():
    res = ResMsg()

    user_name = session["user_name"]
    customer_id = request.form.get("customer_id")
    file = request.files['file']
    if not all([user_name, customer_id, file]):
        res.update(code=ResponseCode.InvalidParameter)
        return res.data

    user = User.query.filter(User.name == user_name).first()
    customer = Customer.query.filter(Customer.id == customer_id).first()
    result = EmailSender.send_email(customer.email, user.name, user.email,
                                    file.stream.read(), file.filename)
    if not result:
        res.update(code=ResponseCode.SendEmailFailed)
        return res.data

    return res.data


# TODO: add admin for the following
@route(bp, '/testGetAll', methods=["GET"])
def test_get_all():
    """
    测试登陆保护下获取数据
    :return:
    """
    res = ResMsg()

    users_json = [model_to_dict(user) for user in User.query.all()]
    res.update(data=users_json)

    return res.data


@route(bp, '/testRemoveAll', methods=["DELETE"])
def test_remove_all():
    """
    移除所有用户以及多对多关系
    """
    res = ResMsg()

    for user in User.query.all():
        if user.customers:
            user.customers.clear()
    User.query.delete()
    db.session.commit()

    return res.data
