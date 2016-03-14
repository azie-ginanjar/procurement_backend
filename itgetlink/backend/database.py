from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)
from collections import namedtuple
from datetime import datetime

import requests
from requests_oauthlib import OAuth1Session
import re
from dictalchemy import make_class_dictable
from flask.ext.sqlalchemy import SQLAlchemy
from requests_oauthlib import OAuth1Session
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.event import listens_for

from .logger import sentry

db = SQLAlchemy()
db.Model.metadata.naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}
make_class_dictable(db.Model)


class SurrogatePK(object):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)


class Created(object):
    created_at = db.Column(db.DateTime(True), default=datetime.utcnow,
                           nullable=False)


class ProcurementUsers(db.Model):
    __tablename__ = "auth_users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Unicode(25), nullable=False)
    password = db.Column(db.Unicode(256), nullable=False)
    
    @classmethod
    def find_all(cls):
        query = cls.query
        
        return query.all()

    @classmethod
    def find_by_id(cls, id):
        query = cls.query
        query = query.filter(cls.id == id)
        return query.first()
        
    @classmethod
    def find_by_username_password(cls, username, password):
        query = cls.query
        query = query.filter(cls.username == username)
        query = query.filter(cls.password == password)
        return query.first()

class AuthenticationToken(db.Model):
    __tablename__ = "auth_token"

    access_token = db.Column(db.Unicode(256), nullable=False)
    user_id = db.Column(db.Integer, primary_key=True, nullable=False)
    status = db.Column(db.Integer, primary_key=True, nullable=False)
    created_date = db.Column(db.DateTime(True), default=datetime.utcnow, nullable=False)
    app_key = db.Column(db.Unicode(256), nullable=False)
    
    @classmethod
    def find_by_access_token_active(cls, access_token):
        query = cls.query
        query = query.filter(cls.access_token == access_token)
        uery = query.filter(cls.status == 1)
        return query.first()

class ApplicationKey(db.Model):
    __tablename__ = "auth_app_key"

    app_key = db.Column(db.Unicode(256), primary_key=True)
    description = db.Column(db.Unicode(256), nullable=False)
    
    @classmethod
    def find_by_app_key(cls, app_key):
        query = cls.query
        query = query.filter(cls.app_key == app_key)
        return query.first()
