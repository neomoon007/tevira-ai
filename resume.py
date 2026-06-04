from operator import attrgetter
from fastapi import Depends
from src.app.main import validate_project_id, tasks, progress_notes, projects

# define function restore_context that takes project_id as parameter, that parameter has to be valid, use validate_project_id function for that.
def restore_context(project_id: str = Depends(validate_project_id)):
    # find project name
    project = projects[project_id]

    # find all notes that belong to that project_id
    matching_notes = [note for note in progress_notes if note.project_id == project_id]

    # find all tasks that belong to that project_id && status == "open"
    open_tasks = [task for task in tasks if task.project_id == project_id and task.status == "open"]

    # output recommended next action (latest note next actions OR open tasks
    latest_note = max(matching_notes, key=attrgetter("updated_at"), default=None)

    return {
        "project": project,
        "current_state": latest_note.current_state if latest_note else None,
        "open_tasks": open_tasks,
        "next_actions": latest_note.next_actions if latest_note else None,
    }