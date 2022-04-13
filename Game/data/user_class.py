from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash
import sqlalchemy
from flask_login import UserMixin
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    login = sqlalchemy.Column(sqlalchemy.String, nullable=False, primary_key=True, unique=True)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True, default='Информация отсутствует')
    email = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.now)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
