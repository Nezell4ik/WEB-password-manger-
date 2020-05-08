import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Password(SqlAlchemyBase):
    __tablename__ = 'passwords'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    url = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    login = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = orm.relation('User')
