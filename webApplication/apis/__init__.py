from flask_restplus import Api
from flask import Blueprint


blueprintApi = Blueprint('apis', __name__, url_prefix='/api')
api = Api(blueprintApi, ordered=False, title='Sample ERP API',
          version='1.0',
          description='ERP Test', doc='/documents/')
