from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.tevira_ai.schemas import (
    ApplyActionResponse,
    CreateProgressNoteAction,
    CreateProgressNoteProposal,
    CreateTaskAction,
    CreateTaskProposal,
    ProgressNoteCreate,
    ProposedAction,
    TaskCreate,
)
from src.tevira_ai.services.date_parser import parse_date
from src.tevira_ai.services.progress_notes import create_progress_note
from src.tevira_ai.services.tasks import create_task


async def apply_action(
    owner_id: UUID, db: AsyncSession, action: ProposedAction
) -> ApplyActionResponse:
    if action.type == "create_task":
        due_date = parse_date(action.data.due_date_hint)
        project_id = action.data.project_hint

        task = await create_task(
            owner_id,
            db,
            TaskCreate(
                title=action.data.title, due_date=due_date, project_id=project_id
            ),
        )

        return ApplyActionResponse(
            status="applied",
            action=CreateTaskAction(
                type="create_task",
                data=CreateTaskProposal(
                    title=task.title,
                    due_date_hint=action.data.due_date_hint,
                    project_hint=project_id,
                ),
            ),
            result=task,
        )

    elif action.type == "create_progress_note":
        note = await create_progress_note(
            owner_id,
            db,
            ProgressNoteCreate(
                project_id=action.data.project_hint,
                next_actions=action.data.next_action,
            ),
        )

        return ApplyActionResponse(
            status="applied",
            action=CreateProgressNoteAction(
                type="create_progress_note",
                data=CreateProgressNoteProposal(
                    next_action=note.next_actions, project_hint=action.data.project_hint
                ),
            ),
            result=note,
        )
