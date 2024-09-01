from pastor.dependencies import get_templates
from pastor.paste.routes import router as paste_router
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
import uvicorn


app = FastAPI()
app.mount("/static", StaticFiles(directory="pastor/static"), name="static")
app.include_router(paste_router)


@app.exception_handler(404)
async def custom_404_handler(req: Request, _):
    t = get_templates()
    return t.TemplateResponse("404.html", {"request": req}, status_code=404)


def start():
    """Launched with `poetry run start` at root level"""
    uvicorn.run("pastor.main:app", host="0.0.0.0", port=8000, reload=True)
