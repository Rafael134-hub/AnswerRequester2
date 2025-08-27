from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from fastapi import Depends
from core.database import get_session

SessionDep = Annotated[AsyncSession, Depends(get_session)]