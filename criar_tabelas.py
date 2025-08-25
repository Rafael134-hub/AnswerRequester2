# criar_tabelas.py
import asyncio
from core.database import engine, Base 
from models import requester_model

async def create_tables() -> None: 
    print("Criando as tabelas no banco de dados")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    print('Tabelas criadas com sucesso')

if __name__ == '__main__':    
    asyncio.run(create_tables())
