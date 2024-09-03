from pastor.dependencies import get_templates
from pastor.paste.controller import PasteController
from pastor.paste.dependencies import get_controller
from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.templating import Jinja2Templates


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
    paste_id = c.create_paste(text)
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
