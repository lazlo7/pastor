# Pastor

Simple text-sharing service

## Configuration
Create a `.env` file in the root directory and set environment variables:
- `APP_WEB_PORT`: port for the web server
- `POSTGRES_HOST`: host address of the postgres database
- `POSTGRES_PORT`: port of the postgres database
- `POSTGRES_USER`: user of the postgres database
- `POSTGRES_DB`: name of the postgres database
- `POSTGRES_PASSWORD`: password for the user of the postgres database

An example is provided in the `.env.example` file.  
You should definitely change the default `POSTGRES_PASSWORD` value.  
Other values may also need to be changed depending on how you want to run the app.  

## Running

### docker compose
Simply run `docker compose up` in the root directory.

### poetry
Configure postgres variables to match your local setup.  
Initialize poetry with `poetry install` and run the app with `poetry run start`.

### pip
Configure the environment variables as described in poetry section.
Project's dependencies are additionally provided in the `requirements.txt` file.  
Install them with `pip install -r requirements.txt` and run the app with `uvicorn pastor.main:app --host=<host> --port=<port>`.  
