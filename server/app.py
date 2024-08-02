from flask import make_response, request, session
from flask_restful import Resource
from config import app, api, bcrypt
from models import db

from controllers.candidates_controller import CandidateSignUp, CandidateLogin, CandidateLogout, CandidateAccount
from controllers.companies_controller import CompanySignUp, CompanyLogin, CompanyLogout, CompanyAccount, CompanyById
from controllers.jobs_controller import CreateJob, AllJobs, JobById, JobsByCompany
from controllers.saved_jobs_controller import SaveJob, AllSavedJobs, SavedJobById

# @app.before_request
# def check_no_login():
#     return print("Testing before request")
    # restricted_endpoints = ['candidate_signup', 'candidate_login', 'company_signup', 'company_login']
    # if request.endpoint in restricted_endpoints and ('candidate_id' in session or 'company_id' in session):
    #     return make_response({"error": "Unauthorised. User already logged in."}, 401)

# def check_company_login():
#     restricted_endpoints = ['company_logout', 'company_account', 'create_job']
#     if request.endpoint in restricted_endpoints and ('candidate_id' not in session or 'company_id' not in session):
#         return make_response({"error": "Unauthorised. No user logged in."}, 401)

# def check_candidate_login():
#     restricted_endpoints = ['candidate_logout', 'candidate_account', 'save_job', 'saved_jobs', 'saved_job_by_id']
#     if request.endpoint in restricted_endpoints and ('candidate_id' not in session or 'company_id' not in session):
#         return make_response({"error": "Unauthorised. No user logged in."}, 401)


@app.route('/')
def index():
    return make_response({"message": "Welcome to the Startup Job Site API"}, 200)


#candidates
api.add_resource(CandidateSignUp, '/candidate/signup', endpoint='candidate_signup')
api.add_resource(CandidateLogin, '/candidate/login', endpoint='candidate_login')
api.add_resource(CandidateLogout, '/candidate/logout', endpoint='candidate_logout')
api.add_resource(CandidateAccount, '/candidate/account', endpoint='candidate_account')

#companies
api.add_resource(CompanySignUp, '/company/signup', endpoint='company_signup')
api.add_resource(CompanyLogin, '/company/login', endpoint='company_login')
api.add_resource(CompanyLogout, '/company/logout', endpoint='company_logout')
api.add_resource(CompanyAccount, '/company/account', endpoint='company_account')
api.add_resource(CompanyById, '/company/<int:id>', endpoint='company_by_id')

#jobs
api.add_resource(CreateJob, '/jobs/create', endpoint='create_job')
api.add_resource(JobById, '/jobs/<int:id>', endpoint='job_by_id')
api.add_resource(AllJobs, '/jobs/all', endpoint='jobs')
api.add_resource(JobsByCompany, '/jobs/company/<int:id>', endpoint='jobs_by_company')
api.add_resource(SaveJob, '/jobs/<int:id>/save', endpoint='save_job')

#saved jobs
api.add_resource(AllSavedJobs, '/saved-jobs', endpoint='saved_jobs')
api.add_resource(SavedJobById, '/saved-jobs/<int:id>', endpoint='saved_job_by_id')




if __name__ == "__main__":
    app.run(port=4000, debug=True)

