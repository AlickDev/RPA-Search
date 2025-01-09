from fastapi import APIRouter, Request, Body, HTTPException
from controller.search_controller import search_data, get_data_index_order_goods_match
from Services.logger import create_logger
from typing import Optional

router = APIRouter()
logger = create_logger()

# Utility function for logging request details
def log_request_info(request: Request, message: str):
    client_ip = request.client.host
    method = request.method
    endpoint = request.url.path
    logger.info(f"{message} | Method: {method}, Endpoint: {endpoint}, Client IP: {client_ip}")

# @router.get('/search/{keyword}')
# async def search(keyword: str, request: Request):
#     log_request_info(request, f"Search request for keyword: {keyword}")
#     try:
#         results = await search_data(keyword)
#         return results
#     except Exception as e:
#         logger.error(f"Error during search request for keyword: {keyword}. Error: {str(e)}")
#         raise HTTPException(status_code=500, detail="Internal Server Error")

# @router.get('/searchs')
# async def searchs(keyword: str, request: Request):
#     log_request_info(request, f"Searchs request for keyword: {keyword}")
#     try:
#         results = await search_data(keyword)
#         return results
#     except Exception as e:
#         logger.error(f"Error during searchs request for keyword: {keyword}. Error: {str(e)}")
#         raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post('/searchs')
async def searchs(request: Request, keyword: str = Body(..., embed=True)):
    log_request_info(request, f"Searchs request for keyword: {keyword}")
    try:
        results = await search_data(keyword)
        return results
    except Exception as e:
        logger.error(f"Error during searchs request for keyword: {keyword}. Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get('/order-goods-match')
async def get_data(request: Request, page: Optional[int] = 1, page_size: Optional[int] = 100):
    log_request_info(request, "Order-goods-match request")
    try:
        results = await get_data_index_order_goods_match(page, page_size)
        return results
    except Exception as e:
        logger.error(f"Error during order-goods-match request. Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

app = APIRouter()
app.include_router(router, prefix='/api', tags=["RPA Search"])
