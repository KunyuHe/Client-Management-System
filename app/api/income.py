from app.api.base import Service
from app.models.model import Income


class IncomeAPI(Service):
    __model__ = Income

    # 指定需要启用的请求方法
    __methods__ = ["GET", "POST", "PUT", "DELETE"]

    service_name = 'income'
