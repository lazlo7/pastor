from pastor.dependencies import get_templates
from pastor.paste.controller import PasteController
from pastor.paste.dependencies import get_controller
from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import PlainTextResponse
from fastapi.templating import Jinja2Templates
import nh3


router = APIRouter()


@router.post("/", status_code=201)
async def post_paste(r: Request, 
                     c: PasteController = Depends(get_controller)):
    body_bytes = await r.body()
    # No need to save empty pastes.
    if not body_bytes:
        raise HTTPException(status_code=400, 
                            detail="paste is empty")
    # Limit the size to preserve disk space.
    if len(body_bytes) > 4096:
        raise HTTPException(status_code=400, 
                            detail="paste too long")
    
    text = body_bytes.decode("utf-8")
    sanitized_text = nh3.clean(text)
    paste_id = c.create_paste(sanitized_text)
    return {"paste_id": paste_id}


@router.get("/")
async def get_root(r: Request, 
                   t: Jinja2Templates = Depends(get_templates)):
    return t.TemplateResponse("create_paste.html", {"request": r})


# TODO: add existing route paths to seqid blocklist to avoid collisions.
@router.get("/{paste_id}")
async def get_paste(paste_id: str,
                    r: Request, 
                    c: PasteController = Depends(get_controller),
                    t: Jinja2Templates = Depends(get_templates)):
    if PasteController.is_paste_id_valid(paste_id):
        paste = c.get_paste(paste_id)
        if paste is not None:
            return t.TemplateResponse("read_paste.html", 
                                      {"request": r, "paste": paste, "paste_id": paste_id})
            
    raise HTTPException(status_code=404)


@router.get("/raw/{paste_id}")
async def get_paste_raw(paste_id: str,
                        c: PasteController = Depends(get_controller)):
    if PasteController.is_paste_id_valid(paste_id):
        paste = c.get_paste(paste_id)
        if paste is not None:
            return PlainTextResponse(paste)
    
    raise HTTPException(status_code=404)


@router.get("/download/{paste_id}")
async def download_paste(paste_id: str,
                         c: PasteController = Depends(get_controller)):
    if PasteController.is_paste_id_valid(paste_id):
        paste = c.get_paste(paste_id)
        if paste is not None:
            return PlainTextResponse(paste, headers={"Content-Disposition": f"attachment; filename={paste_id}.txt"})
    
    raise HTTPException(status_code=404)
