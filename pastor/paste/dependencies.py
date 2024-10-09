from pastor.dependencies import get_db
from pastor.paste.constants import SQIDS_ID_MIN_LENGTH
from pastor.paste.service import seqid
from pastor.paste.service import get_paste
from typing import Any
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session


async def valid_paste_id(paste_id: str, 
                         db: Session = Depends(get_db)) -> dict[str, Any]:
    """
    Checks that a given string can be a valid paste id.
    Returns the paste's text and the given id if a paste with this id exists, 
    otherwise raises an HTTPException.
    """
    # We specifically choose not validate paste_id using fastapi's Path() validation,
    # since it would raise exceptions different from 404, which we want to avoid.
    # Note that the fact that paste_id contains only base64 characters
    # is already checked by the sqids.decode() function.
    if len(paste_id) < SQIDS_ID_MIN_LENGTH:
        raise HTTPException(status_code=404, detail="paste not found")
    
    decoded_id = seqid.decode(paste_id)
    # Since sqids.decode() may return the same integer id for multiple ids,
    # we need to check that the decoded id is actually the same as the encoded one.
    if decoded_id is None or seqid.encode(decoded_id) != paste_id:
        raise HTTPException(status_code=404, detail="paste not found")
    
    paste = await get_paste(paste_id, db)
    if paste is None:
        raise HTTPException(status_code=404, detail="paste not found")

    return {"id": paste_id, "text": paste}
