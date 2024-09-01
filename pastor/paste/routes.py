from fastapi import APIRouter


router = APIRouter()


@router.get("/")
async def create_paste():
    pass


@router.get("/{paste_id}")
async def get_paste(paste_id: str):
    pass
