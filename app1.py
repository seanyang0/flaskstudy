from flask import Flask,jsonify
from flask import  request
from flask_restful import Api, Resource, reqparse

import settings

app = Flask(__name__)
app.config.from_object(settings)
#存放商品
goods_list = []

class Goods:
    def __init__(self,gname,price,status):
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
parser.add_argument('gname', type=str, help='请输入商品名称', required=True, location=['form', 'args'])
parser.add_argument('price', type=float, help='请输入商品价格', required=True, location=['form', 'args'])
parser.add_argument('number', type=int, help='请输入商品数量', location=['form'])
parser.add_argument('status', type=str, choices=['聚划算商品', '非聚划算商品'], help='必须正确填写状态', required=True, location=['form', 'args'])


#定义Resource子类
class GoodsResource(Resource):
    def get(self, gid):
        for goods in goods_list:
            if gid == goods.get('gid'):
                return goods
        return {'msg': '不存在商品'}

    def patch(self,gid):
        pass

    def delete(self,gid):
        pass

class GoodsListResource(Resource):
    goods_number = 1
    def get(self):
        return goods_list
    #商品的添加
    def post(self):
        args = parser.parse_args()
        goods = {}
        goods['gid'] = GoodsListResource.goods_number
        goods['gname'] = args.get('gname')
        goods['price'] = args.get('price')
        goods['number'] = args.get('number')
        goods['status'] = args.get('status')
        goods_list.append(goods)
        GoodsListResource.goods_number += 1
        return {'msg': '添加商品成功', 'goods':goods}

#添加路由
api.add_resource(GoodsResource, '/goods/<int:gid>')
api.add_resource(GoodsListResource, '/goodsList')

if __name__ == '__main__':
    app.run()