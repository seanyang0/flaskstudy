from flask import Flask,jsonify
from flask import  request
from flask_restful import Api, Resource, reqparse, marshal, marshal_with, fields

import settings

app = Flask(__name__)
app.config.from_object(settings)
#存放商品
goods_list = []

class Goods:
    def __init__(self, gid, gname, price, status):
        self.gid = gid
        self.gname = gname
        self.price = price
        self.status = status
        self.number = 0
    def __str__(self):
        return self.gname


#步骤
# 创建API对象
api = Api(app=app)

#解析器
parser =reqparse.RequestParser()
parser.add_argument('gid', type=int, help='请输入商品编号', required=True, location=['form', 'args'])
parser.add_argument('gname', type=str, help='请输入商品名称', required=True, location=['form', 'args'])
parser.add_argument('price', type=float, help='请输入商品价格', required=True, location=['form', 'args'])
parser.add_argument('number', type=int, help='请输入商品数量', location=['form'])
parser.add_argument('status', type=str, choices=['聚划算商品', '非聚划算商品'], help='必须正确填写状态', required=True, location=['form', 'args'])

goods_fields = {
    'gid': fields.Integer,
    'gname': fields.String,
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
        for goods in goods_list:
            if gid == goods.gid:
                return marshal(goods,goods_fields)
        return {'msg': '不存在商品'}

    def patch(self,gid):
        pass

    def delete(self,gid):
        pass

class GoodsListResource(Resource):

    # def get(self):
    #     return marshal(goods_list, goods_fields)

    @marshal_with(goods_list_fields)
    def get(self):
        return {'goodsList': goods_list}

    #商品的添加
    @marshal_with(goods_obj_fields)
    def post(self):
        args = parser.parse_args()
        gid = args.get('gid')
        gname = args.get('gname')
        price = args.get('price')
        number = args.get('number')
        status = args.get('status')
        goods = Goods(gid, gname, price, status)
        if number and number > 0:
            goods.number = number
        goods_list.append(goods)
        return {'msg': '添加商品成功', 'goods': goods}

#添加路由
api.add_resource(GoodsResource, '/goods/<int:gid>')
api.add_resource(GoodsListResource, '/goodsList')

if __name__ == '__main__':
    app.run(host='172.17.0.8', port=4000)