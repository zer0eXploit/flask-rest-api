import sqlite3
from db import db


class User_Model(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def get_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def upsert_user(self):
        db.session.add(self)
        db.session.commit()
