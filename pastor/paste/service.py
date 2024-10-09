from pastor.paste.models import Paste
from pastor.paste.seqid import Seqid
from sqlalchemy.orm import Session


seqid = Seqid()


async def create_paste(text: str, db: Session) -> str:
    id_, encoded_id = await seqid.get_next(db)
    paste = Paste(id=id_, text=text)
    db.add(paste)
    return encoded_id
    

async def get_paste(paste_id: str, db: Session) -> str | None:
    decoded_id = seqid.decode(paste_id)
    if decoded_id is None:
        return None
    paste = db.query(Paste).get(decoded_id)
    return paste.text if paste else None
