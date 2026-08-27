from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.tevira_ai.schemas import (
    CaptureRead,
    CreateProgressNoteAction,
    CreateProgressNoteProposal,
    CreateTaskAction,
    CreateTaskProposal,
    NonEmptyString,
)
from src.tevira_ai.services.parser import parse_note


async def capture_from_text(
    owner_id: UUID, db: AsyncSession, raw_input: NonEmptyString
) -> CaptureRead:
    parsed_input = await parse_note(owner_id, db, raw_input)

    return CaptureRead(
        raw_text=raw_input,
        parsed=parsed_input,
        proposed_actions=[
            CreateTaskAction(
                type="create_task",
                data=CreateTaskProposal(
                    title=parsed_input.title,
                    due_date_hint=parsed_input.due_date_hint,
                    project_hint=parsed_input.project_id_hint,
                ),
            ),
            CreateProgressNoteAction(
                type="create_progress_note",
                data=CreateProgressNoteProposal(
                    next_action=parsed_input.next_action_hint,
                    project_hint=parsed_input.project_id_hint,
                ),
            ),
        ],
    )
