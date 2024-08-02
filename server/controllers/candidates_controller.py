from config import db, bcrypt
from flask import make_response, request, session
from flask_restful import Resource
from models import Candidate



class CandidateSignUp (Resource):

    def post(self):
        if 'candidate_id' in session or 'company_id' in session:
            return make_response ({"error":"Unauthorised. User already logged in."}, 401)

        candidate = Candidate(
                first_name = request.json.get('first_name'),
                last_name = request.json.get('last_name'),
                email = request.json.get('email'),
                hashed_password = request.json.get('hashed_password')
            )

        db.session.add(candidate)
        db.session.commit()

        if candidate.id:
            session['candidate_id'] = candidate.id
            return make_response(candidate.to_dict(), 201)

        else:
            return make_response({"error":"Bad request. Unable to create candidate"}, 400)


class CandidateLogin(Resource):
    
    def post(self):

        if 'company_id' in session or 'candidate_id' in session:
            return make_response ({"error":"Unauthorised. User already logged in."}, 401)

        email = request.json.get('email')
        password = request.json.get('hashed_password')

        if email and password:

            candidate = Candidate.query.filter(Candidate.email == email).first()

            if candidate and candidate.authenticate(password):
                session['candidate_id'] = candidate.id
                return make_response({"message":f"Candidate {candidate.first_name} is logged in"})

            else:
                return make_response({"error":"Unauthorised. Email or password incorrect."}, 401)

        else:
                
            return make_response({"error":"Bad request. Email and password are required for login"}, 400)


class CandidateLogout(Resource):
    def delete(self):

        if 'candidate_id' not in session:
            return make_response ({"error":"Unauthorised. No candidate logged in."}, 401)

        else:
            session.pop('candidate_id', None)
            return make_response({"message":"Logout successful."}, 204)



class CandidateAccount (Resource):

    def get(self):

        if 'candidate_id' not in session:
            return make_response ({"error":"Unauthorised. No candidate logged in."}, 401)

        candidate = Candidate.query.filter(Candidate.id == session['candidate_id']).first()

        if candidate:
            return make_response(candidate.to_dict(), 200)
        
        else: 
            return make_response({"message":"No candidate found."}, 403)

    def patch(self):

        if 'candidate_id' not in session:
            return make_response ({"error":"Unauthorised. No candidate logged in."}, 401)

        candidate = Candidate.query.filter(Candidate.id == session['candidate_id']).first()

        if candidate:
            for attr in request.json:
                setattr(candidate, attr, request.json[attr])
                
            db.session.commit()

            return make_response(candidate.to_dict(), 200)

    def delete(self):

        if 'candidate_id' not in session:
            return make_response ({"error":"Unauthorised. No candidate logged in."}, 401)

        candidate = Candidate.query.filter(Candidate.id == session['candidate_id']).first()

        if candidate:

            db.session.delete(candidate)
            db.session.commit()

            session.pop('candidate_id', None)

            return make_response({"message":"Candidated deleted"}, 204)

        else: 

            return make_response({"message":"No candidate found"}, 404)


