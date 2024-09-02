from pastor.dependencies import get_templates
from pastor.paste.controller import PasteController
from pastor.paste.dependencies import get_controller
from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import PlainTextResponse


router = APIRouter()


@router.post("/", status_code=201)
async def post_paste(r: Request, 
                     c: PasteController = Depends(get_controller)):
    body_bytes = await r.body()
    # No need to save empty pastes.
    if not body_bytes:
        raise HTTPException(status_code=400, 
                            detail="empty paste")
    # Limit the size to preserve disk space.
    if len(body_bytes) > 4096:
        raise HTTPException(status_code=400, 
                            detail="paste too long (max 4096 bytes)")
    
    text = body_bytes.decode("utf-8")
    paste_id = c.create_paste(text)
    return {"paste_id": paste_id}


@router.get("/")
async def get_root(r: Request, 
                   t: Jinja2Templates = Depends(get_templates)):
    return t.TemplateResponse("create_paste.html", {"request": r})


# TODO: add existing route paths to seqid blocklist to avoid collisions.
@router.get("/{paste_id}")
async def get_paste(paste_id: str, 
                    c: PasteController = Depends(get_controller)):
    if not PasteController.is_paste_id_valid(paste_id):
        raise HTTPException(status_code=400, 
                            detail="invalid paste id")

    paste = c.get_paste(paste_id)
    if paste is None:
        raise HTTPException(status_code=404, 
                            detail="paste not found")
    
    # TODO: use StreamingResponse to better handle large pastes.
    return PlainTextResponse(content=paste)
