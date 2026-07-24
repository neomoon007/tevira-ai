from src.app.schemas import ProgressNoteRead

# --- MEMORY STORAGE ---
# projects
projects_in_memory = {}
project_id_number = 0

# notes
progress_notes_in_memory: list[ProgressNoteRead] = []
progress_notes_id_number: int = 0
