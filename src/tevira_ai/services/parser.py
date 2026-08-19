# --- INPUT STRUCTURE ---
# "X before Y. Next, Z"
# Where X is the title, Y is the due_date and Z is the the next_action

# It checks the existing projects to match the project hint
# If it doesn't find any, it is currently hardcoded to return "Tevira-AI" as default

from sqlalchemy.ext.asyncio import AsyncSession

from src.tevira_ai.exceptions import DomainException
from src.tevira_ai.repository.projects import ProjectRepository
from src.tevira_ai.schemas import ParseNoteRead

OWNER_ID = "local_user"


async def parse_note(db: AsyncSession, mind_dump_note: str) -> ParseNoteRead:
    next_action_marker = " Next, "
    due_date_marker = " before "
    try:
        raw_title, next_action = mind_dump_note.split(next_action_marker, maxsplit=1)
        title, due_date = raw_title.split(due_date_marker, maxsplit=1)
    except ValueError:
        raise DomainException(
            status_code=400,
            error_code="INVALID_NOTE_FORMAT",
            message=f"Note must contain '{next_action_marker}' and '{due_date_marker}'.",
        )

    raw_title_list = mind_dump_note.split(" ")
    repository = ProjectRepository(db)
    project_id_hint = await repository.get_project_id_by_title(
        owner_id=OWNER_ID, title_list=raw_title_list
    )

    return ParseNoteRead(
        title=title,
        project_id_hint=project_id_hint,
        due_date_hint=due_date,
        next_action_hint=next_action,
    )
