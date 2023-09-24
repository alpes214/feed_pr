Application is developed using FastAPI/SQLAlchemy libraries and Postgresql database. The database is supposed to be run in a separate container as well as web app has its own separate container.

First of all python environment must be configured. Assume we are in the root of the project.

1. Create python virtual environment `python -m venv ../venv3.11`
2. Activate this environment `. ../venv3.11/bin/activate`
3. Install dependencies `pip install -r requirements.txt`

How to run application:

1. Build docker images `docker-compose -f docker-compose.yml build`
2. Start db containers `docker-compose -f docker-compose.yml up -d`
3. Swagger access to application `http://localhost:8000/docs`
4. DB access through pgadmin `http://localhost:5050` in case some data changes are required
5. Application logs `docker-compose logs web`

How to test inside docker:

1. Build docker images `docker-compose -f docker-compose.test.yml build`
2. Start db containers `docker-compose -f docker-compose.test.yml up test`

How to test locally:

1. Build docker images `docker-compose -f docker-compose.test.yml build`
2. Start db containers `docker-compose -f docker-compose.test.yml up db_test`
3. Start db containers `docker-compose -f docker-compose.test.yml up web`
4. Copy .env_dev to .env `cp .env_dev .env`
5. Execute tests locally: `PYTHONPATH=. pytest -s -v ./tests/`

There is also dev mode when web application can be run in a host operating system. This allows immediately see change in the code.

How to run application in dev mode:

1. Setup environment file `cp .env_dev .env`
2. Build docker images `docker-compose -f docker-compose.test.yml build`
3. Start db containers `docker-compose -f docker-compose.test.yml up db_prod`
4. Start db containers `docker-compose -f docker-compose.test.yml up pgadmin`
5. Execute migrations: `alembic upgrade head`
6. Start application: `PYTHONPATH=./app/ uvicorn main:app --host 0.0.0.0 --port 8000 --reload`
7. Run unit tests: `PYTHONPATH=. pytest -s -v --cov=app ./tests/`
8. Swagger access to application `http://localhost:8000/docs`
9. DB access through pgadmin `http://localhost:5050` in case some data changes are required
