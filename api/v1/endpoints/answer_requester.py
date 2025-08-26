from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.requester_model import AnswerRequestModel
from schemas.requester_schema import ApiRequesterSchema, ApiRequesterCreateSchema
from core.deps import get_session
import httpx

router = APIRouter()

@router.post("/requests", status_code=status.HTTP_201_CREATED, response_model=ApiRequesterSchema)
async def post_request(answerRequest: ApiRequesterCreateSchema, db: AsyncSession = Depends(get_session)):
    async with httpx.AsyncClient() as client:
        try:
            token_response = await client.post("http://cap-ets.br.bosch.com:5678/v1/login/", json={"username": "ct67ca", "password": "ETSindustriaconectada@2"})
            token_response.raise_for_status()
            token_data = await token_response.json()
            token = token_data.get("access_token", str(token_data))
            headers = {
                "Authorization": f"Bearer {token}"
            }

            response = await client.post("http://cap-ets.br.bosch.com:5678/v1/rag/ask", headers=headers, json={"question": answerRequest.request, "file_type": answerRequest.file_type})
            response.raise_for_status()
            external_data = await response.json()

        except httpx.HTTPError as e:
            raise HTTPException(status_code=502, detail=f"Answer API call for authentication failed: {str(e)}")
        
    answer_text_response = external_data.get("answer", str(external_data))
    
    answer_request_data = AnswerRequestModel(
        request =  answerRequest.request,
        response = answer_text_response,
        file_type = answerRequest.file_type     
    )

    try:
        db.add(answer_request_data)
        await db.commit()
        await db.refresh(answer_request_data)
        return answer_request_data
    
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Database error occurred.")

@router.get('/requests', response_model=List[ApiRequesterSchema])
async def get_requests(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(AnswerRequestModel)
        result = await session.execute(query)
        requests: List[AnswerRequestModel] = result.scalars().all()
        return requests

@router.get("/requests/{request_id}", response_model=ApiRequesterSchema, status_code=status.HTTP_200_OK)
async def get_request(request_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(AnswerRequestModel).filter(AnswerRequestModel.request_id == request_id)
        result = await session.execute(query)
        request = result.scalar_one_or_none()

        if request:
            return request
        else:
            raise HTTPException(detail='Request não encontrado.', status_code=status.HTTP_404_NOT_FOUND)