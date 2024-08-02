# startup-job-site-api

Thanks for taking a look at my repo. This app is a submission for my phase 4 project with Academy XI. The brief was to build an API using Flask.

## Introduction
The Startup Job Site API is designed to mimic the (simplified) backend of a jobsite. There are two defined user groups:
- Companies who can create an account and post jobs
- Candidates who can create and account, view and save jobs. They will not be able to apply for jobs via the API.

This API something I hope to build upon to build out a fully fledged job site. 

## Installation
1. Clone the repo to your local machine
2. Run the following commands:
    - `pipenv install`
    - `cd server`
    - `pipenv shell`
    - `alembic upgrade head`
    This will create the models but leave the database blank since these can be populated by the defined routes.
3. To start the app, from the server folder run:
    `python app.py`

You will need to use Postman or a similar agent to test the API and its endpoints.
