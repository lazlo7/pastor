from pastor.database import init_db
from pastor.dependencies import get_templates
from pastor.paste.routes import router as paste_router
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn


app = FastAPI()
app.mount("/static", StaticFiles(directory="pastor/static"), name="static")


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("pastor/static/img/favicon.jpg")


@app.exception_handler(404)
async def custom_404_handler(req: Request, _):
    t = get_templates()
    return t.TemplateResponse("404.html", {"request": req}, status_code=404)


app.include_router(paste_router)

# TODO: is there a better architectural way to initialize db?
init_db()


def start():
    """Launched with `poetry run start` at root level"""
    from pastor.config import APP_WEB_PORT
    uvicorn.run("pastor.main:app", host="0.0.0.0", port=APP_WEB_PORT, reload=True)
