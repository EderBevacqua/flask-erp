from flask import Flask
from flask_bootstrap import Bootstrap

from webApplication.vendors_app import vendors_app
from webApplication.products_app import products_app

from webApplication.apis.vendors_api import nameSpace_apivendor
from webApplication.apis.products_api import nameSpace_apiproduct

from webApplication.infra import db_config

from webApplication.apis import api, blueprintApi

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('settings.py')

    db_config.init()
    Bootstrap(app)

    app.register_blueprint(blueprintApi)

    api.add_namespace(nameSpace_apivendor)
    api.add_namespace(nameSpace_apiproduct)

    app.register_blueprint(vendors_app)
    app.register_blueprint(products_app)

    return app