import sqlalchemy
from .db_session import SqlAlchemyBase


class Match(SqlAlchemyBase):
    __tablename__ = 'matches'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    player_name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    enemy_name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    results = sqlalchemy.Column(sqlalchemy.String, nullable=False)# -> 'WLWLW' где W это победа а L это поражение
    elo = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    kills = sqlalchemy.Column(sqlalchemy.Integer, default=0, nullable=False)
    deaths = sqlalchemy.Column(sqlalchemy.Integer, default=0, nullable=False)
    hp_healed = sqlalchemy.Column(sqlalchemy.Integer, default=0, nullable=False)
    saws_deaths = sqlalchemy.Column(sqlalchemy.Integer, default=0, nullable=False)
    blood_spilled = sqlalchemy.Column(sqlalchemy.Integer, default=0, nullable=False)
    shots = sqlalchemy.Column(sqlalchemy.Integer, default=0, nullable=False)
    hits = sqlalchemy.Column(sqlalchemy.Integer, default=0, nullable=False)
    #для игрока указанного в player_name
