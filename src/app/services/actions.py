from sqlalchemy.orm import Session

from src.app.schemas import (
    ApplyActionResponse,
    CreateProgressNoteAction,
    CreateProgressNoteProposal,
    CreateTaskAction,
    CreateTaskProposal,
    ProgressNoteCreate,
    ProposedAction,
    TaskCreate,
)
from src.app.services.date_parser import parse_date
from src.app.services.progress_notes import create_progress_note
from src.app.services.tasks import create_task


def apply_action(db: Session, action: ProposedAction) -> ApplyActionResponse:
    if action.type == "create_task":
        due_date = parse_date(action.data.due_date_hint)
        project_id = action.data.project_hint

        task = create_task(
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
        project_id = "project_1"  # Project 1 should always be the Inbox
        note = create_progress_note(
            db,
            ProgressNoteCreate(
                project_id=project_id, next_actions=action.data.next_action
            ),
        )

        return ApplyActionResponse(
            status="applied",
            action=CreateProgressNoteAction(
                type="create_progress_note",
                data=CreateProgressNoteProposal(next_action=note.next_actions),
            ),
            result=note,
        )
