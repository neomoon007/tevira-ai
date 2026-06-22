from src.app.schemas import TaskRead, ProgressNoteRead

# --- MEMORY STORAGE ---
tasks_in_memory: list[TaskRead] = []
projects_in_memory = {}
progress_notes_in_memory: list[ProgressNoteRead] = []
