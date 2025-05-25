from flask_restful import Resource, marshal_with, fields, reqparse,abort
from app.models.course import CourseModel
from app.extension import db



#request parser
from flask_restful import reqparse

course_args = reqparse.RequestParser()
course_args.add_argument('code', type=str, required=True, help="Course code cannot be empty")
course_args.add_argument('name', type=str, required=True, help="Course name cannot be empty")
course_args.add_argument('credits', type=int, default=0, help="Credits must be an integer")
course_args.add_argument('teacher_id', type=int, required=True, help="Teacher ID is required")


#response fields
course_fields = {
    'id': fields.Integer,
    'code': fields.String,
    'name': fields.String,
    'credits': fields.Integer,
    'teacher_id': fields.Integer
    
}
# course resource
class Courses(Resource):
    @marshal_with(course_fields)
    def get(self):
        courses = CourseModel.query.all()
        if not courses:
            abort(404, message='Courses not found')
        return courses
    
    @marshal_with(course_fields)
    def post(self):
        args = course_args.parse_args()
        try:
            course = CourseModel(
                code=args['code'],
                name=args['name'],
                credits=args['credits'],
                teacher_id=args['teacher_id']
               
            )
            db.session.add(course)
            db.session.commit()
            return course, 201
        except Exception as e:
            db.session.rollback()
            abort(400, message=f"Error .could not create a course {str(e)}")
class Course(Resource):
    @marshal_with(course_fields)
    def get(self, id):
        course = CourseModel.query.filter_by(id=id).first()
        if not course:
            abort(404, message='Course not found')
        return course
    @marshal_with(course_fields)
    def put(self, id):
        args = course_args.parse_args()
        course = CourseModel.query.filter_by(id=id).first()
        if not course:
            abort(404, message='Course not found')
        try:
            course.code = args['code']
            course.name = args['name']
            course.credits = args['credits']
            course.teacher_id = args['teacher_id']
            db.session.commit()
            return course, 200
        except Exception as e:
            db.session.rollback()
            abort(400, message=f"Error .could not update a course {str(e)}")
    @marshal_with(course_fields)
    def patch(self, id):
        args = course_args.parse_args()
        course = CourseModel.query.filter_by(id=id).first()
        if not course:
            abort(404, message='Course not found')
        try:
            course.code = args['code']
            course.name = args['name']
            course.credits = args['credits']
            course.teacher_id = args['teacher_id']
            db.session.commit()
            return course, 200
        except Exception as e:
            db.session.rollback()
            abort(400, message=f"Error .could not update a course {str(e)}")
    @marshal_with(course_fields)
    def delete(self, id):
        course = CourseModel.query.filter_by(id=id).first()
        if not course:
            abort(404, message='Course not found')
        db.session.delete(course)
        db.session.commit()
        return '', 204

    