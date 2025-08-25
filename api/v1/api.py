from fastapi import APIRouter
from api.v1.endpoints import answer_requester

api_router = APIRouter()
api_router.include_router(answer_requester.router, prefix='/answer_requester', tags=["answer_requester"])