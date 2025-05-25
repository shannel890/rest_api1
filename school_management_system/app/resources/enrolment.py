from flask_restful import Resource, marshal_with, fields, reqparse, abort
from app.models.enrolment import EnrolmentModel
from app.extension import db
from dateutil import parser as date_parser
#request parser
enrolment_args = reqparse.RequestParser()
enrolment_args.add_argument('student_id', type=int, required=True, help="Student ID cannot be empty")
enrolment_args.add_argument('course_id', type=int, required=True, help="Course ID cannot be empty")
enrolment_args.add_argument('enrolment_date', type=date_parser)
enrolment_args.add_argument('status', type=str, default='active')
#response fields    
enrolment_fields = {
    'id': fields.Integer,
    'student_id': fields.Integer,
    'course_id': fields.Integer,
    'enrolment_date': fields.DateTime,
    'status': fields.String
}
#enrolment resource
class Enrolments(Resource):
    @marshal_with(enrolment_fields)
    def get(self):
        enrolments = EnrolmentModel.query.all()
        if not enrolments:
            abort(404, message='Enrolments not found')
        return enrolments

    @marshal_with(enrolment_fields)
    def post(self):
        args = enrolment_args.parse_args()
        try:
            enrolment = EnrolmentModel(
                student_id=args['student_id'],
                course_id=args['course_id'],
                enrolment_date=args['enrolment_date'],
                status=args['status']
            )
            db.session.add(enrolment)
            db.session.commit()
            return enrolment, 201
        except Exception as e:
            db.session.rollback()
            abort(400, message=f"Error: Could not create an enrolment. {str(e)}")
class Enrolment(Resource):
    @marshal_with(enrolment_fields)
    def get(self, id):
        enrolment = EnrolmentModel.query.filter_by(id=id).first()
        if not enrolment:
            abort(404, message='Enrolment not found')
        return enrolment

    @marshal_with(enrolment_fields)
    def patch(self, id):
        args = enrolment_args.parse_args()
        enrolment = EnrolmentModel.query.filter_by(id=id).first()
        if not enrolment:
            abort(404, message='Enrolment not found')
        try:
            enrolment.student_id = args['student_id']
            enrolment.course_id = args['course_id']
            enrolment.enrolment_date = args['enrolment_date']
            enrolment.status = args['status']
            db.session.commit()
            return enrolment, 200
        except Exception as e:
            db.session.rollback()
            abort(400, message=f"Error: Could not update the enrolment. {str(e)}")
    @marshal_with(enrolment_fields)
    def delete(self, id):
        enrolment = EnrolmentModel.query.filter_by(id=id).first()
        if not enrolment:
            abort(404, message='Enrolment not found')
        try:
            db.session.delete(enrolment)
            db.session.commit()
            return '', 204
        except Exception as e:
            db.session.rollback()
            abort(400, message=f"Error: Could not delete the enrolment. {str(e)}")