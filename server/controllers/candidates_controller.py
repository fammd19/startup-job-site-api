#/candidate
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

            session[canddiate_id] = candidate.id

            return make_response(candidate.to_dict(), 201)

        else:
            make_response({"error":"Unable to create candidate"})


class CandidateLogin(Resource):
    
    def post(self):

        email = request.json.get('email')
        password = request.json.get('hashed_password')

        if email and password:

            candidate = Candidate.query.filter(Candidate.email == email).first()

            if candidate and candidate.authenticate(password):
                session['candidate_id'] = candidate.id
                return make_response({"message":f"Candidate {candidate.first_name} logged in"})

            else:
                return make_response({"error":"Unauthorised"}, 404)

        else:
            
            return make_response({"error":"Email and password are required for login"}, 404)



class CandidateLogout(Resource):
    def delete(self):

        session.pop('candidate_id', None)

        return make_response({"message":"Logout successful"}, 204)


class CandidateAccount (Resource):

    def get(self):

        if 'candidate_id' not in session:
            return make_response ({"error":"Unauthorised"}, 404)

        candidate_id = session['candidate_id']

        candidate = Candidate.query.filter(Candidate.id == candidate_id).first()

        if candidate:

            return make_response(candidate.to_dict(), 200)
        
        else: 

            return make_response({"message":"No candidate found"}, 404)

    def patch(self):

        candidate_id = session['candidate_id']

        candidate = Candidate.query.filter(Candidate.id == candidate_id).first()

        if candidate:
            for attr in request.json:
                setattr(candidate, attr, request.json[attr])
                
            db.session.commit()

            return make_response(candidate.to_dict(), 203)


###########    


# class CandidateAccount (Resource):

#     def get(self, id):
#         candidate = Candidate.query.filter(Candidate.id == id).first()

#         if candidate:

#             return make_response(candidate.to_dict(), 200)

#         else:
#             return make_response({"message":"No candidate found"}, 404)

#     def patch(self, id):
#         candidate = Candidate.query.filter(Candidate.id == id).first()


#         #check this func and status code
#         if candidate:
#             for attr in request.json:
#                 setAttr(candidate, attr, candidate['attr'])
                
#             db.session.update(candidate)
#             db.session.commit()

#             return make_response(candidate.to_dict(), 203)

    
#     def delete(self, id):

#         candidate = Candidate.query.filter(Candidate.id == id).first()

#         db.session.delete(candidate)
#         db.session.commit()

#         make_response(candidate.to_dict(), 204)

            
# class CandidateLogin(Resource):

#     def post(self):

#         if not session['candidate_id']:

#             candidate = Canidate.query.filter(Canidate.email == request.json.get('email')).first()

#             if candidate:
#                 session['canddiate_id'] = candidate.id

#                 return make_response({"message":"Login successful"}, 200)

#         else:
#             return make_response({"error":"Unathorised"}, 401)

#     def get (self):
#         if session['candidate_id']:

#             return make_response({"message":f"Candidate {session['candidate_id']} is logged in"}, 200)

#         else:
#             return make_response({"message":"Not candidate logged in"},403)

