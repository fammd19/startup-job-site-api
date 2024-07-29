from config import db, bcrypt
from flask import make_response, request, session
from flask_restful import Resource
from models import Company

class CompanySignUp (Resource):

    def post(self):

        if 'candidate_id' in session or 'company_id' in session:
            return make_response ({"error":"Unauthorised. User already logged in."}, 401)

        company = Company(
                name = request.json.get('name'),
                abn = request.json.get('abn'),
                size = request.json.get('size'),
                industry = request.json.get('industry'),
                csr_tags = request.json.get('csr_tags'),
                website_link = request.json.get('website_link'),
                facebook_link = request.json.get('facebook_link'),
                instagram_link = request.json.get('instagram_link'),
                linkedin_link = request.json.get('linkedin_link'),
                admin_email = request.json.get('admin_email'),
                hashed_password = request.json.get('hashed_password'),
            )

        db.session.add(company)
        db.session.commit()

        if company.id:
                session['company_id'] = company.id
                return make_response({"message": "Company created"}, 201)

        else:            
            return make_response({"error": "Unable to create company"}, 400)


class CompanyLogin(Resource):
    
    def post(self):

        if 'company_id' in session or 'candidate_id' in session:
            return make_response ({"error":"Unauthorised. User already logged in."}, 401)

        admin_email = request.json.get('admin_email')
        password = request.json.get('hashed_password')

        if admin_email and password:
            company = Company.query.filter(Company.admin_email == admin_email).first()

            if company and company.authenticate(password):
                session['company_id'] = company.id
                return make_response({"message":f"Company {company.name} logged in"}, 200)

            else:
                return make_response({"error":"Unauthorised"}, 401)

        else:
            return make_response({"error":"Email and password are required for login"}, 400)



class CompanyLogout(Resource):
    def delete(self):

        if 'company_id' not in session:
            return make_response ({"error":"Unauthorised. No company logged in."}, 401)

        session.pop('company_id', None)
        return make_response({"message":"Logout successful"}, 204)


class CompanyAccount(Resource):

    def get(self):
        if 'company_id' not in session:
            return make_response ({"error":"Unauthorised. No company logged in."}, 401)

        company = Company.query.filter(Company.id == session['company_id']).first()

        if company:
            return make_response(company.to_dict(), 200)
        
        else: 
            return make_response({"message":"No company found."}, 404)

    def patch(self):

        if 'company_id' not in session:
            return make_response ({"error":"Unauthorised. No company logged in."}, 401)

        company = Company.query.filter(Company.id == session['company_id']).first()

        if company:
            for attr in request.json:
                setattr(company, attr, request.json[attr])
                
            db.session.commit()
            return make_response(company.to_dict(), 203)

    def delete(self):

        if 'company_id' not in session:
            return make_response ({"error":"Unauthorised. No company logged in."}, 401)

        company = Company.query.filter(Company.id == session['company_id']).first()

        if company:

            db.session.delete(company)
            db.session.commit()

            session.pop('company_id', None)
            return make_response({"message":"Company deleted"}, 204)

        else: 
            return make_response({"error":"No company account found"}, 404)


class CompanyById(Resource):

    def get(self, id):
        
        company = Company.query.filter(Company.id == id).first()

        if company:
            return make_response(company.to_dict(), 200)
            
        else:
            return make_response({"message": "No company found with this ID"}, 404)
