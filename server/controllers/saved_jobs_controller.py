from config import db, bcrypt
from flask import make_response, request, session
from flask_restful import Resource
from models import SavedJob


class SaveJob (Resource):

    def post(self, id):

        if 'candidate_id' not in session:
            return make_response ({"error":"Unauthorised. No user logged in."}, 403)

        existing_save = SavedJob.query.filter(SavedJob.candidate_id == session['candidate_id'], SavedJob.id == id).first()

        if not existing_save:

            saved_job = SavedJob (
                candidate_id = session['candidate_id'],
                job_id = id
            )

            db.session.add(saved_job)
            db.session.commit()
                    
            return make_response({"message": "Job successfully saved."}, 201)

        else:

            return make_response({"error": "This job has already been saved."}, 404)


class AllSavedJobs (Resource):

    def get(self):

        if 'candidate_id' not in session:
            return make_response ({"error":"Unauthorised. No user logged in."}, 403)

        jobs = SavedJob.query.filter(SavedJob.candidate_id == session['candidate_id']).all()

        if jobs:
            saved_jobs = [ job.to_dict() for job in jobs ]
            return make_response (saved_jobs, 200)

        else:
            return make_response ({"message":"No saved jobs."}, 200)


class SavedJobById (Resource):

    def get(self,id):

        if 'candidate_id' not in session:
            return make_response ({"error":"Unauthorised. No user logged in."}, 403)

        saved_job = SavedJob.query.filter(SavedJob.candidate_id == session['candidate_id'], SavedJob.id == id).first()

        if saved_job:
            return make_response(saved_job.to_dict(), 200)

        else: 
            return make_response({"error": "No saved job matching criteria"}, 400)

    def delete(self,id):

        if 'candidate_id' not in session:
            return make_response ({"error":"Unauthorised. No user logged in."}, 403)

        saved_job = SavedJob.query.filter(SavedJob.candidate_id == session['candidate_id'], SavedJob.id == id).first()

        if saved_job:
            db.session.delete(saved_job)
            db.session.commit()

            return make_response({"message": "Saved job deleted"}, 400)

        else:
            return make_response({"error": "Unable to delete saved job"}, 404)

