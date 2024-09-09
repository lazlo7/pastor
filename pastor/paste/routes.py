from pastor.dependencies import get_templates, get_db
from pastor.paste.utils import validate_paste, is_paste_id_valid
from pastor.paste.service import get_paste, create_paste
from fastapi import APIRouter, HTTPException, Request, Depends
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
# TODO: maybe di is_paste_id_valid() for paste_id?
@router.get("/{paste_id}")
async def get_paste_(paste_id: str,
                     r: Request, 
                     db: Session = Depends(get_db),
                     t: Jinja2Templates = Depends(get_templates)):
    if is_paste_id_valid(paste_id):
        paste = await get_paste(paste_id, db)
        if paste is not None:
            return t.TemplateResponse("read_paste.html", 
                                      {"request": r, "paste": paste, "paste_id": paste_id})
            
    raise HTTPException(status_code=404)


@router.get("/raw/{paste_id}")
async def get_paste_raw(paste_id: str,
                        db: Session = Depends(get_db)):
    if is_paste_id_valid(paste_id):
        paste = await get_paste(paste_id, db)
        if paste is not None:
            return PlainTextResponse(paste)
    
    raise HTTPException(status_code=404)


@router.get("/download/{paste_id}")
async def download_paste(paste_id: str,
                         db: Session = Depends(get_db)):
    if is_paste_id_valid(paste_id):
        paste = await get_paste(paste_id, db)
        if paste is not None:
            headers = {"Content-Disposition": f"attachment; filename={paste_id}.txt"}
            return PlainTextResponse(paste, headers=headers)
    
    raise HTTPException(status_code=404)
