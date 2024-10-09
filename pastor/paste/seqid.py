from pastor.paste.models import Paste
from pastor.paste.constants import BASE64_ALPHABET, SQIDS_ID_MIN_LENGTH
from typing import Tuple
from sqlalchemy import func
from sqlalchemy.orm import Session
from sqids import sqids as sqids_


class Seqid:
    """Calculates next seqid from the database and caches it."""
    def __init__(self):
        self.__sqids = sqids_.Sqids(alphabet=BASE64_ALPHABET, min_length=SQIDS_ID_MIN_LENGTH)
        self.__seqid: int = -1


    @staticmethod
    async def __load_from_db(db: Session) -> int:
        """Assigns seqid the next value."""
        # We basically need to return the max id present + 1.
        # Note the 'or -1' part. This is to handle the case when the table is empty.
        lastest_id = db.query(func.max(Paste.id)).scalar() or -1
        return lastest_id + 1


    def decode(self, encoded_id: str) -> int | None:
        """Decodes the base64 encoded id, returns None if it's invalid."""
        decoded_id = self.__sqids.decode(encoded_id)
        return decoded_id[0] if len(decoded_id) == 1 else None


    def encode(self, id: int) -> str:
        """Encodes the id to base64."""
        return self.__sqids.encode([id])


    async def get_next(self, db: Session) -> Tuple[int, str]:
        """Returns the next seqid and its base64 encoded value."""
        if self.__seqid == -1:
            self.__seqid = await self.__load_from_db(db)

        encoded_id = self.__sqids.encode([self.__seqid])
        # Increment the seqid for the next call.
        self.__seqid += 1
        # Return the previous seqid and the encoded value.
        return self.__seqid - 1, encoded_id      
