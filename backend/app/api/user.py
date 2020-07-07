import logging

from app.models.model import User, Client
from app.utils.auth import Auth, login_required
from app.utils.core import db
from app.utils.emailsender import EmailSender
from app.utils.filetool import FileTool
from app.utils.response import ResMsg, ResponseCode
from app.utils.util import model_to_dict, EmailTool, route
from flask import Blueprint, session, request

bp = Blueprint("api_user", __name__, url_prefix='/user')
logger = logging.getLogger(__name__)


@route(bp, '/register', methods=["POST"])
def register():
    res = ResMsg()

    obj = request.get_json(force=True)
    if not obj or not all(key in obj
                          for key in ("name", "email", "password")):
        res.update(code=ResponseCode.InvalidParameter)
        return res.data

    valid_email = EmailTool.check_email(obj.get("email"))
    if not valid_email:
        res.update(code=ResponseCode.InvalidEmail)
        return res.data

    uniq_name = User.query.filter(User.name == obj.get("name")).count() == 0
    if not uniq_name:
        res.update(code=ResponseCode.RepeatUserName)
        return res.data

    user_obj = User(**obj)
    db.session.add(user_obj)
    db.session.commit()

    return res.data


@route(bp, '/login', methods=["POST"])
def login():
    """登陆成功获取到数据获取token和刷新token"""
    res = ResMsg()

    obj = request.get_json(force=True)
    name = obj.get("name")
    if not all([obj, name, obj.get("password")]):
        res.update(code=ResponseCode.InvalidParameter)
        return res.data

    user_obj = User.query.filter(User.name == name).first()
    if user_obj and user_obj.password == obj.get("password"):
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


@route(bp, '/recover', methods=["POST"])
def recover_password():
    res = ResMsg()

    obj = request.get_json(force=True)
    email = obj.get("email", None)
    if not obj or not email:
        res.update(code=ResponseCode.InvalidParameter)
        return res.data

    user_obj = User.query.filter(User.email == email).first()
    if not user_obj:
        res.update(code=ResponseCode.NoResourceFound)
        return res.data

    subject = "客户管理系统（CMS）用户密码恢复"
    body = (f"用户{user_obj.name}：\n\n"
            f"您好！您的密码是：{user_obj.password}。\n\n"
            f"如果此用户密码恢复请求并非由您本人提出，请尽快联系管理员更改密码。谢谢！\n\n"
            f"祝好，\n客户管理系统（CMS）")
    logger.info(f"To send, {subject}, {body}")
    result = EmailSender.send_email(user_obj.email, subject, body)
    if not result:
        res.update(code=ResponseCode.SendEmailFailed)
        return res.data

    return res.data


@route(bp, '/info', methods=["GET"])
@login_required
def get_info():
    res = ResMsg()

    name = session["user_name"]
    user_obj = User.query.filter(User.name == name).first()
    user_json = model_to_dict(user_obj)
    user_json['n_clients'] = len(user_obj.clients)
    res.update(data=user_json)

    return res.data


@route(bp, '/clients', methods=["GET"])
@login_required
def get_clients():
    res = ResMsg()

    name = session["user_name"]
    user_obj = User.query.filter(User.name == name).first()
    res.update(data=model_to_dict(user_obj.clients))

    return res.data


@route(bp, '/upload', methods=["POST"])
@login_required
def upload():
    res = ResMsg()

    name = session["user_name"]
    file = request.files.get('file', None)
    file_tool = FileTool(name)
    file_tool.logger = logger

    return file_tool.save(file, res)


@route(bp, '/download', methods=["GET"])
def download():
    res = ResMsg()

    name = session["user_name"]
    file_tool = FileTool(name)
    file_tool.logger = logger

    res.update(data=file_tool.get())
    return res.data


# TODO: add admin for the following
@route(bp, '/testGetAll', methods=["GET"])
def test_get_all():
    """
    测试登陆保护下获取数据
    :return:
    """
    res = ResMsg()

    users_json = [model_to_dict(user) for user in User.query]
    res.update(data=users_json)

    return res.data


@route(bp, '/testRemoveAll', methods=["DELETE"])
def test_remove_all():
    """
    移除所有用户以及多对多关系
    """
    res = ResMsg()

    for user in User.query:
        if user.clients:
            user.clients.clear()
    User.query.delete()
    db.session.commit()

    return res.data
