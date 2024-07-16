from flask import make_response
from flask_cors import CORS
from config import app, api
from models import Candidate
from flask_cors import CORS

#, Company, CompanyAdmin, Job, SavedJob 


@app.route('/')
def index():
    return make_response({"message": "Welcome to the Startup Job Site API"}, 200)


CORS(app)


if __name__ == "__main__":
    app.run(port=4000, debug=True)