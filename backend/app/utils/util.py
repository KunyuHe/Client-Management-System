import re
from collections import Iterable
from functools import wraps
from pathlib import Path

from app.utils.response import ResMsg
from flask import jsonify


def get_root_dir():
    return Path(__file__).parent.parent.parent.parent


def model_to_dict(result):
    # 转换完成后，删除  '_sa_instance_state' 特殊属性
    try:
        if isinstance(result, Iterable):
            tmp = [dict(zip(res.__dict__.keys(), res.__dict__.values())) for res
                   in result]
            for t in tmp:
                t.pop('_sa_instance_state')
        else:
            tmp = dict(zip(result.__dict__.keys(), result.__dict__.values()))
            tmp.pop('_sa_instance_state')
        return tmp

    except BaseException as e:
        print(e.args)
        raise TypeError('Type error of parameter')


def route(bp, *args, **kwargs):
    """
    路由设置, 统一返回格式
    :param bp: 蓝图
    :return:
    """
    kwargs.setdefault('strict_slashes', False)

    def decorator(f):
        @bp.route(*args, **kwargs)
        @wraps(f)
        def wrapper(*args, **kwargs):
            rv = f(*args, **kwargs)
            # 响应函数返回整数和浮点型
            if isinstance(rv, (int, float)):
                res = ResMsg()
                res.update(data=rv)
                return jsonify(res.data)
            # 响应函数返回元组
            elif isinstance(rv, tuple):
                # 判断是否为多个参数
                if len(rv) >= 3:
                    return jsonify(rv[0]), rv[1], rv[2]
                else:
                    return jsonify(rv[0]), rv[1]
            # 响应函数返回字典
            elif isinstance(rv, dict):
                return jsonify(rv)
            # 响应函数返回字节
            elif isinstance(rv, bytes):
                rv = rv.decode('utf-8')
            return jsonify(rv)

        return wrapper

    return decorator


class EmailTool:
    @staticmethod
    def check_email(email):
        v_email = re.match((r"^([A-Za-z0-9_\-\.\u4e00-\u9fa5])+\@"
                            "([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,8})$"),
                           email)
        if v_email is None or v_email.group() is None:
            return False
        else:
            return True
