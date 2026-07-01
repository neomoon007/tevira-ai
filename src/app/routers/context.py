from fastapi import Depends, APIRouter
from src.app.utils import (
    validate_progress_note,
    validate_project_id,
    get_project_tasks,
    get_important_task,
)
from src.app.state.memory import projects_in_memory, progress_notes_in_memory
from src.app.schemas import ContextRead
from operator import attrgetter

router = APIRouter(prefix="/context", tags=["Context"])


@router.get("/{project_id}")
def restore_context(project_id: str = Depends(validate_project_id)) -> ContextRead:
    # find project
    project = projects_in_memory[project_id]

    validate_progress_note(project_id)

    # find all notes that belong to that project_id
    matching_notes = [
        note for note in progress_notes_in_memory if note.project_id == project_id
    ]

    # find all tasks that belong to that project_id && status == "open"
    open_tasks = get_project_tasks(project_id)

    # output recommended next action (latest note next actions OR open tasks
    latest_note = max(matching_notes, key=attrgetter("updated_at"), default=None)

    next_actions = (
        latest_note.next_actions
        if latest_note and latest_note.next_actions
        else get_important_task(project_id)
    )

    return ContextRead(
        project=project,
        current_state=latest_note.current_state if latest_note else None,
        open_tasks=open_tasks,
        open_loops=latest_note.open_loops if latest_note else None,
        next_actions=next_actions,
        important_context=latest_note.important_context if latest_note else None,
    )
