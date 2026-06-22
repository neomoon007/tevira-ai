from src.app.schemas import TaskRead, ProgressNoteRead

# --- MEMORY STORAGE ---
tasks_in_memory: list[TaskRead] = []
projects_in_memory = {}
progress_notes: list[ProgressNoteRead] = []
