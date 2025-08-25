from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator
from core.database import get_session

SessionDep = AsyncGenerator[AsyncSession, None]
