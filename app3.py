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

@app.route('/',methods=['get'])
def test():
    uname= request.args.get('uname')
    if uname:
        for user in users:
            if uname == user.get('uname'):
                return user
    return {'msg':'no user!'}

# @app.route('/')
# def hello_world():
#     return 'Hello World!'


if __name__ == '__main__':
    print(app.url_map)
    app.run()
