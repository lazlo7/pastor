from pastor.config import APP_SEQID_PATH
from pastor.paste.constants import SQIDS_ID_MIN_LENGTH
from pastor.paste.dependencies import sqids
from typing import Tuple
from fastapi import HTTPException


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


def is_paste_id_valid(paste_id: str) -> bool:
    """
    Checks that a given string can be a valid paste id.
    """
    # Note that the fact that paste_id contains only base64 characters
    # is already checked by the sqids.decode() function.
    if len(paste_id) < SQIDS_ID_MIN_LENGTH:
        return False
    
    decoded_id = sqids.decode(paste_id)
    # Since sqids.decode() may return the same integer id for multiple ids,
    # we need to check that the decoded id is actually the same as the encoded one.
    return len(decoded_id) == 1 and \
           sqids.encode([decoded_id[0]]) == paste_id
        

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
