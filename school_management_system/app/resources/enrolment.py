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
        """Get all enrollments
        ---
        tags:
            - Enrollments
        summary: Retrieve all enrollments
        description: This endpoint retrieves all enrollments from the system.
        responses:
            200:
                description: List of all enrollments retrieved successfully
                schema:
                    type: array
                    items:
                        type: object
                        properties:
                            id:
                                type: integer
                                description: The unique identifier of the enrollment
                            student_id:
                                type: integer
                                description: The ID of the student
                            course_id:
                                type: integer
                                description: The ID of the course
                            enrolment_date:
                                type: string
                                format: date-time
                                description: The enrollment date
                            grade:
                                type: string
                                description: The grade received
                            status:
                                type: string
                                description: The enrollment status
            404:
                description: No enrollments found
                schema:
                    type: object
                    properties:
                        message:
                            type: string
                            description: Enrollments not found!
        """
        enrolments = EnrolmentModel.query.all()
        if not enrolments:
            abort(404, message='Enrolments not found')
        return enrolments

    @marshal_with(enrolment_fields)
    def post(self):
        """Create a new enrollment
        ---
        tags:
            - Enrollments
        summary: Create a new enrollment
        description: This endpoint creates a new enrollment in the system.
        parameters:
            - in: body
              name: enrollment
              description: Enrollment data
              required: true
              schema:
                  type: object
                  required:
                      - student_id
                      - course_id
                  properties:
                      student_id:
                          type: integer
                          description: The ID of the student
                      course_id:
                          type: integer
                          description: The ID of the course
                      enrolment_date:
                          type: string
                          format: date-time
                          description: The enrollment date
                      grade:
                          type: string
                          description: The grade received
                      status:
                          type: string
                          description: The enrollment status
        responses:
            201:
                description: Enrollment created successfully
                schema:
                    type: object
                    properties:
                        id:
                            type: integer
                            description: The unique identifier of the created enrollment
                        student_id:
                            type: integer
                            description: The ID of the student
                        course_id:
                            type: integer
                            description: The ID of the course
                        enrolment_date:
                            type: string
                            format: date-time
                            description: The enrollment date
                        grade:
                            type: string
                            description: The grade received
                        status:
                            type: string
                            description: The enrollment status
            400:
                description: Bad request - validation error
                schema:
                    type: object
                    properties:
                        message:
                            type: string
                            description: Error message
        """
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
        """
        Get a specific enrolment by ID
        ---
        tags:
            - Enrollments
        summary: Retrieve an enrolment by ID
        description: This endpoint retrieves a specific enrolment by its ID.
        parameters:
            - in: path
              name: id
              type: integer
              required: true
              description: The unique identifier of the enrolment
        responses:
            200:
                description: Enrolment retrieved successfully
                schema:
                    type: object
                    properties:
                        id:
                            type: integer
                            description: The unique identifier of the enrollment
                        student_id:
                            type: integer
                            description: The ID of the student
                        course_id:
                            type: integer
                            description: The ID of the course
                        enrolment_date:
                            type: string
                            format: date-time
                            description: The enrollment date
                        grade:
                            type: string
                            description: The grade received
                        status:
                            type: string
                            description: The enrolment status
            404:
                description: Enrolment not found
                schema:
                    type: object
                    properties:
                        message:
                            type: string
                            description: Enrolment not found!
        """
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
        """Delete an enrollment by ID
        ---
        tags:
            - Enrollments
        summary: Delete an enrollment
        description: This endpoint deletes an enrollment from the system.
        parameters:
            - in: path
              name: id
              type: integer
              required: true
              description: The unique identifier of the enrollment
        responses:
            204:
                description: Enrollment deleted successfully
            404:
                description: Enrollment not found
                schema:
                    type: object
                    properties:
                        message:
                            type: string
                            description: Enrollment not found!
            400:
                description: Bad request - error deleting enrollment
                schema:
                    type: object
                    properties:
                        message:
                            type: string
                            description: Error message
        """
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