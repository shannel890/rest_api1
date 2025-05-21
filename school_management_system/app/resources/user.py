from flask_restful import Resource,Api,marshal_with,fields,reqparse,abort
from app.extension import db
#Database model
class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80),unique=True,nullable=False)
    email = db.Column(db.String(80),unique=True,nullable=False)

    def __repr__(self):
        return f'{self.username} {self.email}'
 # request Parser   
user_args = reqparse.RequestParser()
user_args.add_argument('username',type=str, required=True,help='username cannot be blank')
user_args.add_argument('email',type=str, required=True,help='username cannot be blank')
#output field
user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'email': fields.String
}
#resource for all users

class Users(Resource):
    @marshal_with(user_fields)
    #get all users
    def get(self):
        users = UserModel.query.all()
        if not users:
            abort(404,message='Users not found')
        return users
    @marshal_with(user_fields)
    #create a user
    def post(self):
        args = user_args.parse_args()
        new_user = UserModel(username=args['username'],email=args['email'])
        db.session.add(new_user)
        db.session.commit()
        users = UserModel.query.all()
        return users,201
    
class User(Resource):
    @marshal_with(user_fields)
    def get(self,id):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort (404,message='User not found')
        return user
    
    @marshal_with(user_fields)
    def patch(self,id):
        args = user_args.parse_args()
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404,message='no user with that id')
        user.username = args['username']
        user.email = args['email']
        db.session.commit()
        return user  

    @marshal_with(user_fields) 
    def delete(self,id):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404,message="cannot delete a non existing user")
        db.session.delete(user)
        db.session.commit()
        return f'user deleted successfully'
   





