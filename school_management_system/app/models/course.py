from app.extension import db 
from app.models.enrolment import EnrolmentModel


class CourseModel(db.Model):
    __tablename__ = 'Courses'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(120), unique=True, nullable=False)
    credits = db.Column(db.Integer, nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    enrolments = db.relationship('EnrolmentModel', backref='course',lazy=True)

    def __repr__(self):
        return f"{self.code} - {self.name}"
