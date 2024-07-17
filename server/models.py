#need to review saved job
from config import db, bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property
import re

#need to add data validation

class Candidate (db.Model, SerializerMixin):
    __tablename__ = "candidates"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    _hashed_password = db.Column(db.String, nullable=False)

#     # saved_jobs = db.relationship('SavedJob', back_populates='candidate', cascade='all,delete-orphan')
#     # jobs = association_proxy('saved_jobs', 'job', creator=lambda j:SavedJob(job=j))
    @validates('first_name', 'last_name')
    def validate_name(self, key, value):
        if not value:
            raise ValueError("First and last name are required fields")

        return value
    
    @validates('email')
    def validate_email(self, key, email):
        
        if not email:
            raise ValueError("Email is a required field")

        if Candidate.query.filter(Candidate.email == email).first():
            raise ValueError("Email already taken")

        if not re.match(r'^[A-Za-z0-9]+@[A-Za-z0-9.]+\.[A-Za-z]{2,7}$', email):
            raise ValueError("Email not valid")

        return email


    @hybrid_property
    def hashed_password (self):
        return self._hashed_password

    @hashed_password.setter
    def hashed_password(self, password):
        hashed_password=bcrypt.generate_password_hash(password.encode('utf-8'))

        self._hashed_password = hashed_password.decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._hashed_password, password.encode('utf-8'))

    def __repr__(self):
        return f"<Candidate {self.id}: {self.last_name}, {self.first_name}>"

# class Company (db.Model, SerializerMixin):
#     __tablename__ = "companies"

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String, nullable=False)
#     size = db.Column(db.Integer, nullable=False)
#     industry = db.Column(db.String, nullable=False)
#     certifications = db.Column(db.String, nullable=False) #list of options - db.Choice?
#     website_link = db.Column(db.String, nullable=False)
#     facebook_link = db.Column(db.String)
#     instagram_link = db.Column(db.String)
#     linkedin_link = db.Column(db.String)

#     # company_admin = db.relationship('CompanyAdmin', back_populates='company', cascade='all,delete-orphan')
#     # job = db.relationship('Job', back_populates='company', cascade='all,delete-orphan')


# class CompanyAdmin (db.Model, SerializerMixin):
#     __tablename__ = "company_admins"

#     id = db.Column(db.Integer, primary_key=True)
#     first_name = db.Column(db.String, nullable=False)
#     last_name = db.Column(db.String, nullable=False)
#     email = db.Column(db.String, nullable=False, unique=True)
#     role = db.Column(db.String)
#     _hashed_password = db.Column(db.String, nullable=False)

#     # company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
#     # company = db.relationship('Company', back_populates='company_admin')

    # @validates('first_name', 'last_name')
    # def validate_name(self, key, value):
    #     if not value:
    #         raise ValueError("First and last name are required fields")

    #     return value
    
    # @validates('email')
    # def validate_email(self, key, email):
        
    #     if not email:
    #         raise ValueError("Email is a required field")

    #     if Candidate.query.filter(Candidate.email == email).first():
    #         raise ValueError("Email already taken")

    #     if not re.match(r'^[A-Za-z0-9]+@[A-Za-z0-9.]+\.[A-Za-z]{2,7}$', email):
    #         raise ValueError("Email not valid")

    #     return email

#     @hybrid_property
#     def hashed_password (self):
#         return self._hashed_password

#     @hashed_password.setter
#     def hashed_password(self, password):
#         hashed_password=bcrypt.generate_password_hash(password.encode('utf-8'))

#         self._hashed_password = hashed_password.decode('utf-8')

#     def authenticate(self, password):
#         return bcrypt.check_password_hash(self._hashed_password, password.encode('utf-8'))

#     def __repr__(self):
#         return f"<Company admin {self.id}: {self.last_name}, {self.first_name}>"

# class Job (db.Model, SerializerMixin):
#     __tablename__ = "jobs"

#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String, nullable=False)
#     salary = db.Column(db.Integer, nullable=False)
#     salary_comments = db.Column(db.String)
#     department = db.Column(db.String, nullable=False)
#     role_description = db.Column(db.String, nullable=False)
#     application_link = db.Column(db.String, nullable=False)
#     location = db.Column(db.String, nullable=False)
#     experience = db.Column(db.String)

#     # company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))

#     # saved_jobs = db.relationship('SavedJob', back_populates='job')


    
# class SavedJob (db.Model, SerializerMixin):
#     __tablename__ = "saved_jobs"

#     id = db.Column(db.Integer, primary_key=True)

#     #review this
#     candidate_id = db.Column(db.Integer, db.ForeignKey('candidates.id'))
#     job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'))

#     # candidate = db.relationship('Candidate', back_populates='saved_jobs')
#     # job = db.relationship('Job', back_populates='saved_jobs')

