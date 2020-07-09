import logging
import logging.config
import os

import yaml
from app.api.router import router
from app.task.trade import TradeNamespace
from app.utils.core import JSONEncoder, db
from app.utils.emailsender import EmailSender
from app.utils.util import create_dir
from flask import Flask, Blueprint
from flask_cors import CORS
from flask_socketio import SocketIO

logger = logging.getLogger(__name__)


def create_app(config_name, config_path=None):
    app = Flask(__name__)

    # 处理跨域
    CORS(app, resources=r"/*")

    # 读取配置文件
    if not config_path:
        pwd = os.getcwd()
        config_path = os.path.join(pwd, 'config/config.yaml')
    if not config_name:
        config_name = 'PRODUCTION'

    # 读取配置文件
    conf = read_yaml(config_name, config_path)
    app.config.update(conf)

    # 更新邮箱发送配置
    EmailSender.set_address(app.config.get("SEND_EMAIL").get('ADDRESS'))
    EmailSender.set_authcode(app.config.get("SEND_EMAIL").get('AUTHCODE'))
    EmailSender.set_stmphost(app.config.get("SEND_EMAIL").get('HOST'))
    EmailSender.set_stmpport(app.config.get("SEND_EMAIL").get('PORT'))

    # 注册接口
    register_api(app=app, routers=router)

    # 返回json格式转换
    app.json_encoder = JSONEncoder

    # 注册数据库连接
    db.app = app
    db.init_app(app)

    # 日志文件目录
    create_dir(app.config['LOGGING_PATH'])

    # 报表文件目录
    create_dir(app.config['REPORT_PATH'])

    # 日志设置
    with open(app.config['LOGGING_CONFIG_PATH'], 'r', encoding='utf-8') as f:
        dict_conf = yaml.safe_load(f.read())
    logging.config.dictConfig(dict_conf)

    # 读取msg配置
    with open(app.config['RESPONSE_MESSAGE'], 'r', encoding='utf-8') as f:
        msg = yaml.safe_load(f.read())
        app.config.update(msg)

    return app


def create_socketio(app):
    app.config['SECRET_KEY'] = 'secret!'

    socketio = SocketIO(app, cors_allowed_origins="*")
    socketio.on_namespace(TradeNamespace("/flask"))
    TradeNamespace.set_socketio(socketio)

    return socketio


def read_yaml(config_name, config_path):
    """
    config_name:需要读取的配置内容
    config_path:配置文件路径
    """
    if config_name and config_path:
        with open(config_path, 'r', encoding='utf-8') as f:
            conf = yaml.safe_load(f.read())
        if config_name in conf.keys():
            return conf[config_name.upper()]
        else:
            raise KeyError('未找到对应的配置信息！')
    else:
        raise ValueError('请输入正确的配置名称或配置文件路径！')


def register_form(app, router_api, url, method, view_func):
    if method in router_api.__methods__:
        app.add_url_rule('{}<string:key>'.format(url), view_func=view_func,
                         methods=[method, ])


def register_api(app, routers):
    for router_api in routers:
        if isinstance(router_api, Blueprint):
            app.register_blueprint(router_api)
        else:
            try:
                endpoint = router_api.__name__
                view_func = router_api.as_view(endpoint)
                # url默认为类名小写
                url = '/{}/'.format(router_api.__name__.lower())
                if 'GET' in router_api.__methods__:
                    app.add_url_rule(url, defaults={'key': None},
                                     view_func=view_func, methods=['GET', ])
                    register_form(app, router_api, url, "GET", view_func)
                if 'POST' in router_api.__methods__:
                    app.add_url_rule(url, view_func=view_func,
                                     methods=['POST', ])
                register_form(app, router_api, url, "PUT", view_func)
                register_form(app, router_api, url, "DELETE", view_func)
            except Exception as e:
                raise ValueError(e)
