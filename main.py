from fastapi import FastAPI 
from core.configs import settings
from api.v1.api import api_router
import os
import uvicorn

app = FastAPI(title='Answer Requests API - FastAPI SQL Alchemy')
app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == '__main__':
    

    port = int(os.environ.get("PORT", 8001))  # Pega a porta do Render ou usa 8000 localmente
    # uvicorn.run("main:app", host="0.0.0.1", port=port, log_level='info', reload=True)
    
    uvicorn.run("main:app", host="127.0.0.1", port=port, log_level='info', reload=True)

