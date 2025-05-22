from flask_restful import Resource,marshal_with,fields,reqparse,abort
from app.models.teacher import TeacherModel
from app.extension import db

teacher_args = reqparse.RequestParser()
teacher_args.add_argument('first_name',type=str,required=True,help="First Name is required")
teacher_args.add_argument('last_name',type=str,required=True,help="Last Name is required")
teacher_args.add_argument('email',type=str,required=True,help="Email Name is required")
teacher_args.add_argument('phone',type=str)
teacher_args.add_argument('department',type=str)
teacher_args.add_argument('credits',type=int,help="credit is required")


teacher_fields = {
    'id':fields.Integer,
    'first_name': fields.String,
    'last_name': fields.String,
    'email': fields.String,
    'phone': fields.String,
    'department': fields.String,
    'hire_date': fields.DateTime,
    'credits': fields.Integer,
    'courses': fields.String


}

class Teachers(Resource):
    @marshal_with(teacher_fields)
    def get(self):
        teachers = TeacherModel.query.all()
        if not teachers:
            abort(404, message='Teacher not found')
        return teachers
    
    @marshal_with(teacher_fields)
    def post(self):
        args = teacher_args.parse_args()
        try:
            new_teacher = TeacherModel(
                first_name=args['first_name'],
                last_name=args['last_name'],
                email=args['email'],
                phone=args['phone'],
                department=args['department'],
                credits=args['credits']
                )
            db.session.add(new_teacher)
            db.session.commit()
            return new_teacher, 201
        except Exception as e:
            db.session.rollback()
            abort(400, message=f"Error creating a teacher {str(e)}")

