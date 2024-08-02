#need to add data validation

from config import db, bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property
import re


class Candidate (db.Model, SerializerMixin):
    __tablename__ = "candidates"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    _hashed_password = db.Column(db.String, nullable=False)

    saved_jobs = db.relationship('SavedJob', back_populates='candidate', cascade='all,delete-orphan')
    jobs = association_proxy('saved_jobs', 'job', creator=lambda j:SavedJob(job=j))

    serialize_rules = ('-saved_jobs.candidate', '-saved_jobs.candidate_id', '-jobs.saved_jobs','-_hashed_password','-abn')
    
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



class Company (db.Model, SerializerMixin):
    __tablename__ = "companies"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    abn = db.Column(db.Integer, unique=True)
    size = db.Column(db.Integer, nullable=False)
    industry = db.Column(db.String, nullable=False)
    about = db.Column(db.String, nullable=False)
    website_link = db.Column(db.String, nullable=False)
    facebook_link = db.Column(db.String)
    instagram_link = db.Column(db.String)
    linkedin_link = db.Column(db.String)
    admin_email = db.Column(db.String, nullable=False, unique=True)
    _hashed_password = db.Column(db.String, nullable=False)

    jobs = db.relationship('Job', back_populates='company', cascade='all,delete-orphan')

    serialize_rules = ('-jobs.company','-_hashed_password')

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Name cannot be blank")

        if Company.query.filter(Company.name == name).first():
            raise ValueError("Name registered to an existing company")

        return name

    @validates('size')
    def validate_name(self, key, size):
        if not isinstance(size, (int,)):
            raise ValueError("Size must be an integer")

        if size <= 0 or size > 200:
            raise ValueError("Size must be between 1 and 200")

        return size

    @validates('abn')
    def validate_abn(self, key, abn):
        
        if not abn or not isinstance(abn, (int,)):
            raise ValueError("ABN is a required field and must be a number")

        if not len(str(abn)) == 11:
            raise ValueError("ABN should have 11 digits")

        if Company.query.filter(Company.abn == abn).first():
            raise ValueError("ABN registered to an existing company")

        return abn

    @validates('industry')
    def validate_industry(self, key, industry):
        industries = ["agriculture","construction","health & education","financial services","hospitality","legal","manufactuting","retail & consumer goods","technology"]

        if industry.lower() not in industries:
            raise ValueError("Industry must be from the predefined list")

        return industry

    @validates('admin_email')
    def validate_email(self, key, admin_email):
        
        if not admin_email:
            raise ValueError("Email is a required field")

        if Company.query.filter(Company.admin_email == admin_email).first():
            raise ValueError("Email already taken")

        if not re.match(r'^[A-Za-z0-9]+@[A-Za-z0-9.]+\.[A-Za-z]{2,7}$', admin_email):
            raise ValueError("Email not valid")

        return admin_email

    @validates('website_link','facebook_link','instagram_link','linkedin_link')
    def validate_links(self, key, value):

        if value: 
            if not re.match(r'^(https?:\/\/)?(www\.)?([A-Za-z0-9._%+-]+\.[A-Za-z]{2,6})(\/[A-Za-z0-9._%+-]*)*$', value):
                raise ValueError("Link not valid")

        return value

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
        return f"<Company admin {self.id}: {self.name}>"



class Job (db.Model, SerializerMixin):
    __tablename__ = "jobs"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    salary = db.Column(db.Integer, nullable=False)
    salary_comments = db.Column(db.String)
    department = db.Column(db.String, nullable=False)
    role_description = db.Column(db.String, nullable=False)
    application_link = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    experience = db.Column(db.String)
    closing_date = db.Column(db.DateTime)
    date_posted = db.Column(db.DateTime)

    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    company = db.relationship('Company', back_populates='jobs')
    saved_jobs = db.relationship('SavedJob', back_populates='job')

    serialize_rules = ('-company_id', '-company.jobs', '-company._hashed_password', '-company.admin_email','-saved_jobs')

    @validates('department')
    def validate_department(self, key, department):
        departments = ["management","hr","finance","operations","tech","marketing","legal","customer services"]

        if department.lower() not in departments:
            raise ValueError("Department must be from the predefined list")

        return department


class SavedJob (db.Model, SerializerMixin):
    __tablename__ = "saved_jobs"

    id = db.Column(db.Integer, primary_key=True)

    candidate_id = db.Column(db.Integer, db.ForeignKey('candidates.id'))
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'))

    candidate = db.relationship('Candidate', back_populates='saved_jobs')
    job = db.relationship('Job', back_populates='saved_jobs')

    serialize_rules = ('-candidate_id','-job_id', '-candidate')



