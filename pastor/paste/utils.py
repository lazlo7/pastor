from fastapi import HTTPException


def validate_paste(paste: bytes | str) -> None:
    """
    Validates paste and raises a relevant HTTPException on failure.
    """
    # No need to save empty pastes.
    if not paste:
        raise HTTPException(status_code=412, 
                            detail="paste is empty")
    # Limit the size to preserve disk space.
    if len(paste) > 4096:
        raise HTTPException(status_code=413, 
                            detail="paste is too long")
