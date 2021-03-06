# -*- coding: utf-8 -*-

from flask import Flask
import pymysql
from flask_sqlalchemy import SQLAlchemy
from flask import  request
from flask_restful import Api, Resource, reqparse, marshal, marshal_with, fields
from sqlalchemy import create_engine

#dialect+driver://username:password@host:port/database

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@localhost:3306/goods?charset=utf8"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
#查询时显示原始sql语句
app.config["SQLALCHEMY_ECHO"] = True
db = SQLAlchemy(app)
engine = create_engine("mysql+pymysql://root:root@localhost:3306/goods?charset=utf8", echo=True)


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

def table_exists(name):
    ret = engine.dialect.has_table(engine, name)
    print('Table "{}" exists: {}'.format(name, ret))
    return ret

def database_is_empty():
    table_names = SQLAlchemy.inspect(engine).get_table_names()
    is_empty = table_names == []
    print('Db is empty: {}'.format(is_empty))
    return is_empty

#步骤
# 创建API对象
api = Api(app=app)

#解析器
parser =reqparse.RequestParser()
parser.add_argument('gid', type=int, help='请输入商品编号', required=True, location=['form', 'args'])
parser.add_argument('name', type=str, help='请输入商品名称', required=True, location=['form', 'args'])
parser.add_argument('price', type=int, help='请输入商品价格', required=True, location=['form', 'args'])
parser.add_argument('number', type=int, help='请输入商品数量', location=['form'])
parser.add_argument('status', type=str, choices=['聚划算商品', '非聚划算商品'], help='必须正确填写状态', required=True, location=['form', 'args'])

goods_fields = {
    'gid': fields.Integer,
    'name': fields.String,
    'price': fields.Float,
    'number': fields.Integer,
    'status': fields.String
}

goods_obj_fields = {
    'msg': fields.String,
    'goods': fields.Nested(goods_fields)
}

goods_list_fields = {
    'goodsList': fields.List(fields.Nested(goods_fields))
}


#定义Resource子类
class GoodsResource(Resource):
    def get(self, gid):
        pass

    def patch(self,gid):
        pass

    def delete(self,gid):
        pass

class GoodsListResource(Resource):

    @marshal_with(goods_list_fields)
    def get(self):
        goods_list = goods.query.all()
        return {'goodsList': goods_list}

    # @marshal_with(goods_obj_fields)
    #商品的添加
    def post(self):
        ret = table_exists('goods')
        if ret != True:
            db.create_all()
        args = parser.parse_args()
        gid = args.get('gid')
        name = args.get('name')
        price = args.get('price')
        number = args.get('number')
        status = args.get('status')
        tmpgood = goods(gid=gid, name=name, price=price, number=number, status=status)
        db.session.add_all([tmpgood])
        db.session.commit()
        return {'msg': '添加商品成功'}

#添加路由
api.add_resource(GoodsResource, '/goods/<int:gid>')
api.add_resource(GoodsListResource, '/goodsList')

if __name__ == '__main__':
    app.debug = True # 设置调试模式，生产模式的时候要关掉debug
    app.run(host='172.17.0.8', port=4000)