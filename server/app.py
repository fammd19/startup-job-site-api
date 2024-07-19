from flask import make_response
from config import app, api
from controllers.candidates_controller import CandidateSignUp, CandidateLogin, CandidateLogout, CandidateAccount

from flask_restful import Resource
from models import Candidate
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



if __name__ == "__main__":
    app.run(port=4000, debug=True)