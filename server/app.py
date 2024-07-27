from flask import make_response
from config import app, api
from controllers.candidates_controller import CandidateSignUp, CandidateLogin, CandidateLogout, CandidateAccount
from controllers.companies_controller import CompanySignUp, CompanyLogin, CompanyLogout, CompanyAccount
from controllers.jobs_controller import CreateJob, AllJobs, JobById, JobsByCompany
from controllers.saved_jobs_controller import SaveJob, AllSavedJobs, SavedJobById

from flask_restful import Resource
from config import db, bcrypt
from flask import request


@app.route('/')
def index():
    return make_response({"message": "Welcome to the Startup Job Site API"}, 200)

#candidates
api.add_resource(CandidateSignUp, '/candidate/signup', endpoint="candidate_signup")
api.add_resource(CandidateLogin, '/candidate/login', endpoint="candidate_login")
api.add_resource(CandidateLogout, '/candidate/logout', endpoint="candidate_logout")
api.add_resource(CandidateAccount, '/candidate/account', endpoint="candidate_account")

#companies
api.add_resource(CompanySignUp, '/company/signup', endpoint="company_signup")
api.add_resource(CompanyLogin, '/company/login', endpoint="company_login")
api.add_resource(CompanyLogout, '/company/logout', endpoint="company_logout")
api.add_resource(CompanyAccount, '/company/account', endpoint="company_account")

#jobs
api.add_resource(CreateJob, '/jobs/create', endpoint="create_job")
api.add_resource(JobById, '/jobs/<int:id>', endpoint="job_by_id")
api.add_resource(AllJobs, '/jobs/all', endpoint="jobs")
api.add_resource(JobsByCompany, '/jobs/company/<int:id>', endpoint="jobs_by_company")
api.add_resource(SaveJob, '/jobs/<int:id>/save', endpoint="save_job")

#saved jobs
api.add_resource(AllSavedJobs, '/saved-jobs', endpoint="saved_jobs")
api.add_resource(SavedJobById, '/saved-jobs/<int:id>', endpoint="saved_job_by_id")


if __name__ == "__main__":
    app.run(port=4000, debug=True)

