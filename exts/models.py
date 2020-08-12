# -*- coding: utf-8 -*-

from flask import Flask
import pymysql
from flask_sqlalchemy import SQLAlchemy

#dialect+driver://username:password@host:port/database

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@localhost:3306/goods"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
#查询时显示原始sql语句
app.config["SQLALCHEMY_ECHO"] = True
db = SQLAlchemy(app)

"""
goods表：
0.gid
1.name
2.price
3.status
4.number
"""
class goods(db.Model):
    __tablename__ = 'goods'
    gid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    price = db.Column(db.Integer)
    status = db.Column(db.String(64))
    number = db.Column(db.Integer)


    def __repr__(self):
        return '<goods %r>' % self.name




if __name__ == "__main__":
    db.create_all()