from flask import Flask
from app.extension import db
from flask_restful import Api
from app.resources.user import Users,User



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///api.db'
db.init_app(app)
api = Api(app)

 #api endpoints
api.add_resource(Users,'/api/users/')
api.add_resource(User,'/api/users/<int:id>')

         



