from typing import List
import json
import requests
from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.requester_model import AnswerRequestModel
from schemas.requester_schema import ApiRequesterSchema, ApiRequesterCreateSchema
from core.deps import get_session
import httpx
import mistune
import re

router = APIRouter()

def converter_markdown(texto_markdown):
    markdown  = mistune.create_markdown(renderer=mistune.Renderer())
    texto_convertido = markdown(texto_markdown)
    texto_final_formatado = re.sub(r'[^\w\s,;.!?]', '', texto_convertido)
    return texto_final_formatado

@router.post("/requests", status_code=status.HTTP_201_CREATED, response_model=ApiRequesterSchema)

async def post_request(answerRequest: ApiRequesterCreateSchema, db: AsyncSession = Depends(get_session)):
    async with httpx.AsyncClient() as client:
        try:
            form_data = {
                "username": "ct67ca@bosch.com",
                "password": "ETSindustriaconectada@1"
            }
            headersLogin = {"Content-Type": "application/x-www-form-urlencoded"}
            token_response = await client.post("http://cap-ets.br.bosch.com:5678/v1/auth/token", data=form_data, headers=headersLogin)
            token_response.raise_for_status()
            token_data = token_response.json()
            token = token_data.get("access_token", str(token_data))
            rag_headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }

            answer_payload = {"question": answerRequest.request, "file_type": answerRequest.file_type}
            
            answer_payload = json.dumps(answer_payload)
            response = requests.post("http://cap-ets.br.bosch.com:5678/v1/rag/ask", data=answer_payload, headers=rag_headers)
            external_data = response.json()

        except Exception as e:
            print(f"EXCEPTION : {e}")
            raise HTTPException(status_code=502, detail=f"Answer API call for authentication failed: {str(e)}")
        
    answer_text_response = converter_markdown(external_data.get("answer", str(external_data)))
    
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