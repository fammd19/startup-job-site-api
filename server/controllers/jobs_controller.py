from config import db, bcrypt
from flask import make_response, request, session
from flask_restful import Resource
from models import Job

class CreateJob (Resource):

    def post(self):
        
        if 'company_id' not in session:
            return make_response ({"error":"Unauthorised. No company logged in."}, 403)

        job = Job(
                title = request.json.get('title'),
                salary = request.json.get('salary'),
                salary_comments = request.json.get('salary_comments'),
                department = request.json.get('department'),
                role_description = request.json.get('role_description'),
                application_link = request.json.get('application_link'),
                location = request.json.get('location'),
                experience = request.json.get('experience'),
                company_id = 1
            )

        db.session.add(job)
        db.session.commit()

        
        if job.id:
            return make_response({"message": "Job posted"}, 201)

        else:
            
            return make_response({"error": "Unable to create job"}, 400)


class ViewJobs(Resource):

    def get(self):
        jobs = Job.query.all()

        if len(jobs) > 0:
            jobs_dict = [job.to_dict() for job in jobs]
            return make_response(jobs_dict, 200)
        else:
            return make_response({"message": "No jobs available"}, 200)


class ViewJobById (Resource):

    def get(self, id):
        
        job = Job.query.filter(Job.id == id).first()

        if job:
            return make_response(job.to_dict(), 200)
            
        else:
            return make_response({"message": "No jobs found with this ID"}, 404)


