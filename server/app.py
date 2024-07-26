from flask import make_response
from config import app, api
from controllers.candidates_controller import CandidateSignUp, CandidateLogin, CandidateLogout, CandidateAccount, CandidateJobs
from controllers.companies_controller import CompanySignUp
from controllers.jobs_controller import CreateJob, DisplayJobs, SaveJob, ViewJob

from flask_restful import Resource
from config import db, bcrypt
from flask import request


@app.route('/')
def index():
    return make_response({"message": "Welcome to the Startup Job Site API"}, 200)


#candidates
api.add_resource(CandidateSignUp, '/signup', endpoint="signup")
api.add_resource(CandidateLogin, '/login', endpoint="login")
api.add_resource(CandidateLogout, '/logout', endpoint="logout")
api.add_resource(CandidateAccount, '/account', endpoint="account")
api.add_resource(CandidateJobs, '/saved-jobs', endpoint="saved_jobs")



#companies
api.add_resource(CompanySignUp, '/company-signup', endpoint="company_signup")

#jobs
api.add_resource(CreateJob, '/jobs/create', endpoint="create_job")
api.add_resource(DisplayJobs, '/jobs/display', endpoint="display_jobs")
api.add_resource(SaveJob, '/jobs/<int:id>/save', endpoint="save_job")
api.add_resource(ViewJob, '/jobs/<int:id>/view', endpoint="view_job")

if __name__ == "__main__":
    app.run(port=4000, debug=True)