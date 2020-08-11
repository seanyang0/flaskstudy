from flask import Flask,jsonify
from flask import  request
from flask_restful import Api, Resource


import settings

app = Flask(__name__)
app.config.from_object(settings)

#步骤
# 创建API对象
api = Api(app=app)

users=[
    {'uname':'admin1','age':18,'address':'beijing'},
    {'uname':'admin2','age':18,'address':'beijing'},
    {'uname':'admin3','age':19,'address':'nanjing'},
    {'uname':'admin4','age':20,'address':'shanghai'}
]
# 创建resource子类,并定义该类的方法
class UserResource(Resource):
    #获取单个用户
    def get(self):
        uname= request.args.get('uname')
        if uname:
            for user in users:
                if uname == user.get('uname'):
                    return user
        return {'msg':'no user!'}
    #注册用户
    def post(self):
        user = {}
        uname = request.form.get('uname')
        user['uname'] = uname
        age = request.form.get('age')
        user['age'] = age
        address = request.form.get('address')
        user['address'] = address
        users.append(user)
        return {'msg':'注册成功', 'user':user}
    #修改用户
    def patch(self):
        uname = request.form.get('uname')
        new_address = request.form.get('address')
        if uname and new_address:
            for user in users:
                if uname == user.get('uname'):
                    user['address'] = new_address
                    return {'msg':'修改成功','user':user}
        return {'msg':'修改失败'}
    #删除用户
    def delete(self):
        uname = request.form.get('uname')
        if uname:
            for user in users:
                if uname == user.get('uname'):
                    f = users.remove(user)
                    print(f)
                    return {'msg':'删除成功'}
        return {'msg': '删除失败'}
class UsersResource(Resource):
    def get(self):
        return users

#绑定路由
api.add_resource(UserResource, '/user')
api.add_resource(UsersResource, '/users')
# @app.route('/')
# def hello_world():
#     return 'Hello World!'


if __name__ == '__main__':
    print(app.url_map)
    app.run()
