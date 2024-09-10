from pastor.dependencies import get_templates, get_db
from pastor.paste.dependencies import valid_paste_id
from pastor.paste.utils import validate_paste
from pastor.paste.service import create_paste
from typing import Any
from fastapi import APIRouter, Request, Depends
from fastapi.responses import PlainTextResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import nh3


router = APIRouter()


@router.get("/")
async def get_root(r: Request, 
                   t: Jinja2Templates = Depends(get_templates)):
    return t.TemplateResponse("create_paste.html", {"request": r})


@router.post("/", status_code=201)
async def post_paste(r: Request, 
                     db: Session = Depends(get_db)):
    body_bytes = await r.body()
    validate_paste(body_bytes)
    
    text = body_bytes.decode("utf-8", errors="ignore")
    sanitized_text = nh3.clean(text)

    # Just to be sure, revalidate the paste after sanitization.
    validate_paste(sanitized_text)
    paste_id = await create_paste(sanitized_text, db)
    return {"paste_id": paste_id}


# TODO: add existing route paths to seqid blocklist to avoid collisions.
@router.get("/{paste_id}")
async def get_paste(r: Request,
                    paste: dict[str, Any] = Depends(valid_paste_id), 
                    t: Jinja2Templates = Depends(get_templates)):
    return t.TemplateResponse("read_paste.html", 
                              {"request": r, 
                               "paste": paste["text"], 
                               "paste_id": paste["id"]})


@router.get("/raw/{paste_id}")
async def get_paste_raw(paste: dict[str, Any] = Depends(valid_paste_id)):
    return PlainTextResponse(paste["text"])


@router.get("/download/{paste_id}")
async def download_paste(paste: dict[str, Any] = Depends(valid_paste_id)):
    headers = {"Content-Disposition": f"attachment; filename={paste["id"]}.txt"}
    return PlainTextResponse(paste["text"], headers=headers)
