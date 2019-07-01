#!/usr/bin/python
# -*- coding:utf-8 -*-
# author : b1ng0

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# 定义ORM
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.Integer) # 0 卫星 | 1 用户
    userId = db.Column(db.String(255), unique=True)
    userKey = db.Column(db.String(255), unique=True)
    preRandom = db.Column(db.String(255), unique=True)
    def __init__(self, role, userId, userKey, preRandom):
        self.role = role
        self.userId = userId
        self.userKey = userKey
        self.preRandom = preRandom
    def __repr__(self):
        return '<Uid %r>' % self.userId


def getAuthData(userId):
    user = User.query.filter_by(userId=userId).one()
    return {
        "userId": user.userId,
        "userKey": user.userKey,
        "preRandom": user.preRandom
    }