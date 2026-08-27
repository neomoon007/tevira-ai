from uuid import UUID

from sqlalchemy import delete, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.tevira_ai.db.models import ProgressNote
from src.tevira_ai.exceptions import ResourceInUseError


class ProgressNoteRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, note: ProgressNote) -> ProgressNote:
        self.session.add(note)
        await self.session.commit()
        await self.session.refresh(note)

        return note

    async def get_all(self, owner_id: UUID) -> list[ProgressNote]:
        tasks_list = await self.session.scalars(
            select(ProgressNote).where(ProgressNote.owner_id == owner_id)
        )

        return list(tasks_list.all())

    async def get_by_project(
        self, owner_id: UUID, project_id: UUID
    ) -> list[ProgressNote]:
        notes_list = await self.session.scalars(
            select(ProgressNote).where(
                ProgressNote.owner_id == owner_id,
                ProgressNote.project_id == project_id,
            )
        )

        return list(notes_list.all())

    async def get_by_id(self, owner_id: UUID, note_id: UUID) -> ProgressNote | None:
        note_result = await self.session.scalar(
            select(ProgressNote).where(
                ProgressNote.owner_id == owner_id, ProgressNote.id == note_id
            )
        )

        return note_result

    async def update(
        self, owner_id: UUID, note_id: UUID, note_obj: dict
    ) -> ProgressNote | None:
        updated_note = await self.session.scalar(
            update(ProgressNote)
            .where(ProgressNote.owner_id == owner_id, ProgressNote.id == note_id)
            .values(**note_obj)
            .returning(ProgressNote)
        )

        await self.session.commit()
        return updated_note

    async def delete(self, owner_id: UUID, note_id: UUID):
        try:
            await self.session.execute(
                delete(ProgressNote).where(
                    ProgressNote.owner_id == owner_id, ProgressNote.id == note_id
                )
            )
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()

            raise ResourceInUseError(resource_type="Note", resource_id=str(note_id))


# TODO: missing except statement for NoResultFound exception, also there is no error handling on the service layer yet!!!
