from flask import Flask

import settings
from app.apis.goods_api import goods_bp
from exts import db, api, cache

config = {}

def create_app():
    app = Flask(__name__)
    app.config.from_object(settings)
    db.init_app(app)
    # api.init_app(app)
    cache.init_app(app, config=config)
    app.register_blueprint(goods_bp)
    print(app.url_map)
    return app