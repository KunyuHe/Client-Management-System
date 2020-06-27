from datetime import datetime, timedelta

from app.utils.core import db

BJ_TIME = 8

# 用户-客户多对多
user_customer = db.Table('user_customer',
                         db.Column('user_id', db.Integer,
                                   db.ForeignKey('tb_user.id'),
                                   primary_key=True),
                         db.Column('customer_id', db.Integer,
                                   db.ForeignKey('tb_customer.id'),
                                   primary_key=True))


class User(db.Model):
    __tablename__ = 'tb_user'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(20), nullable=False)  # 用户名
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)

    customers = db.relationship('Customer', secondary=user_customer,
                                cascade="all,delete", backref="users")


class Customer(db.Model):
    __tablename__ = "tb_customer"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)

    incomes = db.relationship('Income', cascade="all,delete",
                              backref="customer")


class Income(db.Model):
    __tablename__ = "tb_income"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("tb_customer.id"))
    value = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date,
                     default=(datetime.utcnow() +
                              timedelta(hours=BJ_TIME)).strftime("%Y-%m-%d"),
                     nullable=False)
