import logging

from app.models.model import User, Customer, Income
from app.utils.auth import login_required
from app.utils.core import db
from app.utils.response import ResponseCode, ResMsg
from app.utils.util import route, model_to_dict, EmailTool
from flask import Blueprint, session
from flask import request

bp = Blueprint("api_customer", __name__, url_prefix='/customer')
logger = logging.getLogger(__name__)


@route(bp, '/add', methods=["POST"])
@login_required
def add():
    res = ResMsg()

    user_name = session["user_name"]
    user_obj = User.query.filter(User.name == user_name).first()

    obj = request.get_json(force=True)
    customer_name = obj.get("name")
    customer_email = obj.get("email")
    if not all([obj, customer_name, customer_email]):
        res.update(code=ResponseCode.InvalidParameter)
        return res.data

    # 将客户添加到指定用户管理列表中
    customer_obj = Customer.query.filter(
        Customer.name == customer_name).first()
    if customer_obj:
        customer_obj.users.append(user_obj)
        db.session.commit()
        return res.data

    valid_email = EmailTool.check_email(customer_email)
    if not valid_email:
        res.update(code=ResponseCode.InvalidEmail)
        return res.data

    # 添加新客户记录
    customer_obj = Customer(name=customer_name, email=customer_email,
                            users=[user_obj])
    db.session.add(customer_obj)
    db.session.commit()
    res.update(data=model_to_dict(customer_obj))

    return res.data


@route(bp, '/remove', methods=["DELETE"])
@login_required
def remove():
    res = ResMsg()

    obj = request.get_json(force=True)
    if not obj or not obj.get("id"):
        res.update(ResponseCode.InvalidParameter)
        return res.data

    customer_obj = Customer.query.filter(Customer.id == obj.get("id")).first()
    customer_obj.users.clear()
    db.session.delete(customer_obj)
    db.session.commit()

    return res.data


@route(bp, '/incomes', methods=["GET"])
@login_required
def get_incomes():
    res = ResMsg()

    obj = request.get_json(force=True)
    if not obj or not obj.get("id"):
        res.update(ResponseCode.InvalidParameter)
        return res.data
    customer_obj = Customer.query.filter(Customer.id == obj.get("id")).first()
    res.update(data=model_to_dict(customer_obj.incomes))

    return res.data


# TODO: Add admin role
@route(bp, '/testRemoveAll', methods=["DELETE"])
def remove_all():
    """
    移除所有客户以及多对多关系
    """
    res = ResMsg()

    for customer in Customer.query.all():
        customer.users.clear()
    Customer.query.delete()
    db.session.commit()

    return res.data


@route(bp, '/testGetAll', methods=["GET"])
def get_all():
    res = ResMsg()

    customers = db.session.query(Customer).filter().all()
    customers_json = [{**model_to_dict(customer),
                       'users': model_to_dict(customer.users)}
                      for customer in customers]
    res.update(data=customers_json)

    return res.data
