from datetime import datetime, timedelta

from app.utils.core import db

# 用户-客户多对多
user_client = db.Table('user_client',
                       db.Column('user_id', db.Integer,
                                 db.ForeignKey('user.id'),
                                 primary_key=True),
                       db.Column('client_id', db.Integer,
                                 db.ForeignKey('client.id'),
                                 primary_key=True))


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(20), nullable=False)  # 用户名
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)

    clients = db.relationship('Client', secondary=user_client,
                              cascade="all,delete", backref="users")


class Client(db.Model):
    __tablename__ = "client"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)

    incomes = db.relationship('Income', cascade="all,delete", backref="client")


class Income(db.Model):
    __tablename__ = "income"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey("client.id"))
    value = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date,
                     default=(datetime.utcnow() + timedelta(hours=8)).strftime(
                         "%Y-%m-%d"),
                     nullable=False)
