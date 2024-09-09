from pastor.paste.models import Paste
from pastor.paste.utils import get_next_paste_id
from pastor.paste.dependencies import sqids
from sqlalchemy.orm import Session


async def create_paste(text: str, db: Session) -> str:
    id_, encoded_id = get_next_paste_id()
    paste = Paste(id=id_, text=text)
    db.add(paste)
    return encoded_id
    

async def get_paste(paste_id: str, db: Session) -> str | None:
    decoded_id = sqids.decode(paste_id)
    if len(decoded_id) != 1:
        return None
    paste = db.query(Paste).get(decoded_id[0])
    return paste.text if paste else None
