from datetime import datetime, timedelta

from app.utils.core import db

# 用户-客户多对多
user_client = db.Table('user_client',
                       db.Column('user_id', db.Integer,
                                 db.ForeignKey('users.id'),
                                 primary_key=True),
                       db.Column('client_id', db.Integer,
                                 db.ForeignKey('clients.id'),
                                 primary_key=True))


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    clients = db.relationship('Client', secondary=user_client,
                              cascade="all,delete", backref="users")


class Client(db.Model):
    __tablename__ = "clients"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False)
    trade = db.Column(db.Boolean, default=False)

    incomes = db.relationship('Income', cascade="all,delete", backref="client")


class Income(db.Model):
    __tablename__ = "incomes"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey("clients.id"))
    value = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date,
                     default=(datetime.utcnow() + timedelta(hours=8)).strftime(
                         "%Y-%m-%d"),
                     nullable=False)
