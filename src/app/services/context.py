from operator import attrgetter

from sqlalchemy.orm import Session

from src.app.schemas import ContextRead, NonEmptyString
from src.app.services.progress_notes import get_notes_by_project
from src.app.services.projects import get_project
from src.app.services.tasks import get_important_task, get_tasks_by_project


def restore_context(db: Session, project_id: NonEmptyString) -> ContextRead:
    # find project
    project = get_project(db, project_id)

    # find all notes that belong in that project
    matching_notes = get_notes_by_project(db, project_id)

    # find all tasks that belong to that project_id && status == "open"
    open_tasks = get_tasks_by_project(db, project_id)

    # output recommended next action (latest note next actions OR open tasks)
    latest_note = max(matching_notes, key=attrgetter("updated_at"), default=None)

    next_actions = (
        latest_note.next_actions
        if latest_note and latest_note.next_actions
        else get_important_task(db, project_id)
    )

    return ContextRead(
        project=project,
        current_state=latest_note.current_state if latest_note else None,
        open_tasks=open_tasks,
        open_loops=latest_note.open_loops if latest_note else None,
        next_actions=next_actions,
        important_context=latest_note.important_context if latest_note else None,
    )
