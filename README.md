# Pastor

Simple text-sharing service

## Configuration
Create a `.env` file in the root directory and set environment variables:
- `APP_WEB_PORT`: port for the web server (used only by docker)
- `APP_PASTE_STORAGE_PATH`: path to the directory where pastes are stored

An example is provided in the `.env.example` file 

## Running

### docker compose
Simply run `docker compose up` in the root directory.

### poetry
Initialize poetry with `poetry install` and run the app with `poetry run start`.

### pip
Project's dependencies are additionally provided in the `requirements.txt` file.  
Install them with `pip install -r requirements.txt` and run the app with `uvicorn pastor.main:app --host=<host> --port=<port>`.  
