from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash
import sqlalchemy
from flask_login import UserMixin
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    login = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=True)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True, default='Информация отсутствует')
    email = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.now)
    banned = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True, default=False)
    elo = sqlalchemy.Column(sqlalchemy.Integer, default=1000)
    wins = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    loses = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    views = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    picture = sqlalchemy.Column(sqlalchemy.String, default='default')
    kills = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    deaths = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    accuracy = sqlalchemy.Column(sqlalchemy.Integer, default=100)
    hp_healed = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    saws_deaths = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    blood_spilled = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    shots = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    hits = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    
    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
