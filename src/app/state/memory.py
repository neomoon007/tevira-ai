from src.app.schemas import TaskRead, ProgressNoteRead

# --- MEMORY STORAGE ---
# tasks
tasks_in_memory: list[TaskRead] = []
task_id_number: int = 0

# projects
projects_in_memory = {}
project_id_number = 0

# notes
progress_notes_in_memory: list[ProgressNoteRead] = []
progress_notes_id_number: int = 0
