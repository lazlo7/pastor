from pastor.config import APP_SEQID_PATH
from pastor.paste.constants import BASE64_ALPHABET, SQIDS_ID_MIN_LENGTH
from typing import Tuple
from fastapi import HTTPException
from sqids import sqids as sqids_


sqids = sqids_.Sqids(alphabet=BASE64_ALPHABET, min_length=SQIDS_ID_MIN_LENGTH)


def validate_paste(paste: bytes | str) -> None:
    """
    Validates paste and raises a relevant HTTPException on failure.
    """
    # No need to save empty pastes.
    if not paste:
        raise HTTPException(status_code=400, 
                            detail="paste is empty")
    # Limit the size to preserve disk space.
    if len(paste) > 4096:
        raise HTTPException(status_code=400, 
                            detail="paste too long")
        

def load_seq_id() -> int:
    try:
        with open(APP_SEQID_PATH, "r") as f:
            return int(f.read())
    except ValueError:
        # TODO: add logging.
        return 0
    except:
        return 0


def write_seq_id(seq_id: int):
    try:
        with open(APP_SEQID_PATH, "w") as f:
            f.write(str(seq_id))
    except:
        # TODO: add logging.
        pass


def get_next_paste_id() -> Tuple[int, str]:
    # TODO: optimize somehow maybe? maybe cache seq_id?
    seq_id = load_seq_id()
    paste_id = sqids.encode([seq_id])
    write_seq_id(seq_id + 1)
    return seq_id, paste_id
