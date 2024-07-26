from config import db, bcrypt
from flask import make_response, request, session
from flask_restful import Resource
from models import Job, SavedJob

class CreateJob (Resource):

    def post(self):
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


class DisplayJobs (Resource):

    def get(self):
        jobs = Job.query.all()

        if len(jobs)>1:
            jobs_dict = []
            for job in jobs:
                jobs_dict.append(job.to_dict())
            
            return make_response(jobs_dict, 200)

        else:
            return make_response({"message": "No jobs available"}, 200)


class SaveJob (Resource):

    def post(self,id):
        # job = Job.query.filter(job.id==job_id)

        # if job:
        saved_job = SavedJob (
            candidate_id = session['candidate_id'],
            job_id = id
        )

        db.session.add(saved_job)
        db.session.commit()
            
        return make_response({"message": "Added"}, 201)

        # else:
        #     return make_response({"error": "Unactionable"}, 400)

class ViewJob (Resource):

    def get(self):
        pass