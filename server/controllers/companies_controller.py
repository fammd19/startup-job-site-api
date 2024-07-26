from config import db, bcrypt
from flask import make_response, request, session
from flask_restful import Resource
from models import Company

class CompanySignUp (Resource):

    def post(self):
        company = Company(
                name = request.json.get('name'),
                bsn = request.json.get('bsn'),
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
            db.session.rollback()
            return make_response({"error": "Unable to create company"}, 400)
