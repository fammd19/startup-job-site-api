from config import db, bcrypt
from flask import make_response, request, session
from flask_restful import Resource
from models import Candidate

class CandidateSignUp (Resource):

    def post(self):
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
            make_response({"error":"Unable to create candidate"})


class CandidateLogin(Resource):
    
    def post(self):

        if not session['candidate_id']: 

            email = request.json.get('email')
            password = request.json.get('hashed_password')

            if email and password:

                candidate = Candidate.query.filter(Candidate.email == email).first()

                if candidate and candidate.authenticate(password):
                    session['candidate_id'] = candidate.id
                    return make_response({"message":f"Candidate {candidate.first_name} logged in"})

                else:
                    return make_response({"error":"Unauthorised"}, 401)

            else:
                
                return make_response({"error":"Email and password are required for login"}, 404)

        else:
            return make_response({"error":"User already logged in"}, 404)

class CandidateLogout(Resource):
    def delete(self):

        if 'candidate_id' not in session:
            return make_response ({"error":"Unauthorised. No user logged in."}, 403)

        else:
            session.pop('candidate_id', None)
            return make_response({"message":"Logout successful."}, 204)



class CandidateAccount (Resource):

    def get(self):

        if 'candidate_id' not in session:
            return make_response ({"error":"Unauthorised. No user logged in."}, 403)

        candidate_id = session['candidate_id']

        candidate = Candidate.query.filter(Candidate.id == candidate_id).first()

        if candidate:

            return make_response(candidate.to_dict(), 200)
        
        else: 

            return make_response({"message":"No candidate found."}, 403)

    def patch(self):

        if 'candidate_id' not in session:
            return make_response ({"error":"Unauthorised. No user logged in."}, 403)

        candidate_id = session['candidate_id']

        candidate = Candidate.query.filter(Candidate.id == candidate_id).first()

        if candidate:
            for attr in request.json:
                setattr(candidate, attr, request.json[attr])
                
            db.session.commit()

            return make_response(candidate.to_dict(), 203)

    def delete(self):

        if 'candidate_id' not in session:
            return make_response ({"error":"Unauthorised. No user logged in."}, 403)

        candidate_id = session['candidate_id']

        candidate = Candidate.query.filter(Candidate.id == candidate_id).first()

        if candidate:

            db.session.delete(candidate)
            db.session.commit()

            session.pop('candidate_id', None)

            return make_response(candidate.to_dict(), 204)

        else: 

            return make_response({"message":"No candidate found"}, 403)


