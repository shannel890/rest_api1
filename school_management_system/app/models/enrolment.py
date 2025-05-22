from app.extension import db
from datetime import datetime,timezone

class EnrolmentModel(db.Model):
    __tablename__ = 'Enrolments'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('Courses.id'), nullable=False)
    enrolment_date = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    grade = db.Column(db.String(2))
    status = db.Column(db.String(20), default='enrolled') #enrolled,completed,dropped

    
    def __repr__(self):
        return f"Enrollment:{self.id}"