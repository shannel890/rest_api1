from flask import Flask
from flask_restful import Api
from app.extension import db
from flask_migrate import Migrate
from flasgger import Swagger
from app.resources.user import Users,User
from app.resources.teacher import Teachers, Teacher
from app.resources.student import Students,Student
from app.resources.course import Courses,Course
from app.resources.fee  import Fees,Fee
from app.resources.enrolment import Enrolments,Enrolment
from config import Config


# Swagger configuration
Swagger_config = {
    "headers":[],
    "specs":[
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True  # all in
           
        }
    ], "static_url_path": "/flasgger_static",
    # "static_folder": "static",  # must be set by user
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}
#api information template
template = {
    "info": {
        "title": "School Management System API",
        "description": "API for managing school resources such as users, teachers, students, courses, fees, and enrolments.",
        "version": "1.0.0",
        "contact": {
            "name": "Support Team",
            "email": "admin@gmail.com"
        }
    },
        "host": "localhost:5000",
        "basePath": "/api",
        "schemes":["http","https"],
        "tags":[
            {
                "name": "Users",
                "description": "Operations related to users"
            },
            {
                "name": "Teachers",
                "description": "Operations related to teachers"
            },
            {
                "name": "Students",
                "description": "Operations related to students"
            },
            {
                "name": "Courses",
                "description": "Operations related to courses"
            },
            {
                "name": "Fees",
                "description": "Operations related to fees"
            },
            {
                "name": "Enrolments",
                "description": "Operations related to enrolments"
            }
        ]
        
}



app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
api = Api(app)
migrate = Migrate(app,db)
swagger = Swagger(app,config=Swagger_config,template=template)

 #api endpoints
api.add_resource(Users,'/api/users')
api.add_resource(User,'/api/users/<int:id>')
api.add_resource(Teachers,'/api/teachers')
api.add_resource(Teacher,'/api/teachers/<int:id>')
api.add_resource(Students,'/api/students')
api.add_resource(Student,'/api/students/<int:id>')
api.add_resource(Courses,'/api/courses')
api.add_resource(Course,'/api/courses/<int:id>')
api.add_resource(Fees,'/api/fees')
api.add_resource(Fee,'/api/fees/<int:id>')
api.add_resource(Enrolments,'/api/enrolments')
api.add_resource(Enrolment,'/api/enrolments/<int:id>')


         



