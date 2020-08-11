from flask import Blueprint
from flask_restful import Resource, Api

from exts import api

goods_bp = Blueprint('goods', __name__, url_prefix='/goods')
goods_api = Api(goods_bp)

class GoodsResource(Resource):
    def get(self, gid):
        pass

class GoodsListResource(Resource):
    def get(self):
        pass

# api.add_resource(GoodsResource, '/goods/<int:gid>')
goods_api.add_resource(GoodsResource, '/<int:gid>')
goods_api.add_resource(GoodsListResource, '/list')

