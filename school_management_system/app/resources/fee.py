from flask_restful import Resource, marshal_with, fields, reqparse, abort
from app.models.fee import FeeModel
from app.extension import db
from datetime import datetime
from dateutil import parser as date_parser

# Request Parser
fee_args = reqparse.RequestParser()
fee_args.add_argument('student_id', type=int, required=True, help="Student ID cannot be empty.")
fee_args.add_argument('amount', type=float, required=True, help="Amount cannot be empty.")
fee_args.add_argument('payment_date', type=date_parser)
fee_args.add_argument('status', type=str, default='pending', help="Status defaults to 'pending'.")
fee_args.add_argument('semester', type=str, help="Semester cannot be empty.")
fee_args.add_argument('fee_type', type=str, required=True, help="Fee type cannot be empty.")

# Response Fields
fee_fields = {
    'id': fields.Integer,
    'student_id': fields.Integer,
    'amount': fields.Float,
    'status': fields.String,
    'semester': fields.String,
    'fee_type': fields.String
}

class Fees(Resource):
    @marshal_with(fee_fields)
    def get(self):
        fees = FeeModel.query.all()
        if not fees:
            abort(404, message='Fees not found.')
        return fees

    @marshal_with(fee_fields)
    def post(self):
        args = fee_args.parse_args()

        # Parse payment_date manually
        payment_date = None
        if args.payment_date:
            try:
                payment_date = datetime.fromisoformat(args.payment_date)
            except ValueError:
                abort(400, message="Invalid date format.")

        try:
            fee = FeeModel(
                student_id=args.student_id,
                amount=args.amount,
                payment_date=payment_date,
                status=args.status,
                semester=args.semester,
                fee_type=args.fee_type
            )
            db.session.add(fee)
            db.session.commit()
            return fee, 201
        except Exception as e:
            db.session.rollback()
            abort(400, message=f"Error: Could not create fee. {str(e)}")

class Fee(Resource):
    @marshal_with(fee_fields)
    def get(self, id):
        fee = FeeModel.query.filter_by(id=id).first()
        if not fee:
            abort(404, message='Fee not found')
        return fee
    
    @marshal_with(fee_fields)
    def patch(self, id):
        args = fee_args.parse_args()
        fee = FeeModel.query.filter_by(id=id).first()
        if not fee:
            abort(404, message='Fee not found')
        try:
            fee.student_id = args['student_id']
            fee.amount = args['amount']
            fee.payment_date = args['payment_date']
            fee.status = args['status']
            fee.semester = args['semester']
            fee.fee_type = args['fee_type']
            db.session.commit()
            return fee, 200
        except Exception as e:
            db.session.rollback()
            abort(400, message=f"Error .could not update a fee {str(e)}")
        
    @marshal_with(fee_fields)
    def delete(self, id):
        fee = FeeModel.query.filter_by(id=id).first()
        if not fee:
            abort(404, message='Fee not found')
        try:
            db.session.delete(fee)
            db.session.commit()
            return '', 204
        except Exception as e:
            db.session.rollback()
            abort(400, message=f"Error .could not delete a fee {str(e)}")



