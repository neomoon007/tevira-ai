from sqlalchemy import Integer, cast, delete, desc, func, select, update
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session

from src.tevira_ai.db.models import ProgressNote


class ProgressNoteRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, note: ProgressNote) -> ProgressNote:
        self.session.add(note)
        self.session.commit()
        self.session.refresh(note)

        return note

    def get_all(self, owner_id: str) -> list[ProgressNote]:
        tasks_list = list(
            self.session.scalars(
                select(ProgressNote).where(ProgressNote.owner_id == owner_id)
            ).all()
        )

        return tasks_list

    def get_highest_id(self, owner_id: str) -> int:
        clean_number = func.regexp_replace(ProgressNote.id, r"\D", "", "g")
        num_only_from_id = cast(clean_number, Integer)
        query = (
            select(num_only_from_id)
            .where(ProgressNote.owner_id == owner_id)
            .order_by(desc(num_only_from_id))
            .limit(1)
        )

        highest_task_id = self.session.scalars(query).first()

        return highest_task_id if highest_task_id is not None else 0

    def get_by_project(self, owner_id: str, project_id: str) -> list[ProgressNote]:
        notes_list = list(
            self.session.scalars(
                select(ProgressNote).where(
                    ProgressNote.owner_id == owner_id,
                    ProgressNote.project_id == project_id,
                )
            ).all()
        )

        return notes_list

    def get_by_id(self, owner_id: str, note_id: str) -> ProgressNote | None:
        note_result = self.session.scalars(
            select(ProgressNote).where(
                ProgressNote.owner_id == owner_id, ProgressNote.id == note_id
            )
        ).first()

        return note_result

    def update(self, owner_id: str, note_id: str, note_obj: dict) -> ProgressNote:
        try:
            updated_note = self.session.execute(
                update(ProgressNote)
                .where(ProgressNote.owner_id == owner_id, ProgressNote.id == note_id)
                .values(**note_obj)
                .returning(ProgressNote)
            ).scalar_one()

            self.session.commit()
            return updated_note
        except NoResultFound:
            self.session.rollback()
            raise

    def delete(self, owner_id: str, note_id: str):
        try:
            self.session.execute(
                delete(ProgressNote).where(
                    ProgressNote.owner_id == owner_id, ProgressNote.id == note_id
                )
            )
            self.session.commit()
        except IntegrityError:
            self.session.rollback()

            raise


# TODO: missing except statement for NoResultFound exception, also there is no error handling on the service layer yet!!!
