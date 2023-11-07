from fastapi import APIRouter

from controller.search_controller import search_data

router = APIRouter()


@router.get('/search/{keyword}')
async def search(keyword: str):
    results = await search_data(keyword)
    return results
@router.get('/')
async def get_empty():
    return {"message": "RPA search"}


app = APIRouter()
app.include_router(router, prefix='/api', tags=["Search"])
