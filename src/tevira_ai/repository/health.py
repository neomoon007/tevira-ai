from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession


class HealthRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def check(self) -> str:
        query_result = await self.session.scalar(select(func.version()))
        if isinstance(query_result, str):
            return query_result
        raise TypeError
