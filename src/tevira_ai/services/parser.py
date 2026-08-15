# --- INPUT STRUCTURE ---
# "Need to X before Y. Next, Z"
# Where X is the title, Y is the due_date and Z is the the next_action

# It checks the existing projects to match the project hint
# If it doesn't find any, it is currently hardcoded to return "Tevira-AI" as default

import os
import uuid

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession

from src.tevira_ai.schemas import ParseNoteRead
from src.tevira_ai.services.projects import list_projects

load_dotenv()

default_project = uuid.UUID(os.getenv("DEFAULT_PROJECT"))


# Currently only supports projects that don't have spaces inside of its name, meaning it supports one word names and names separated by -
async def find_project_id_by_name(db: AsyncSession, input: str) -> uuid.UUID:
    projects = await list_projects(db)
    input_list = input.split(" ")

    for input_item in input_list:
        project_id = next(
            (
                project_obj.id
                for project_obj in projects
                if project_obj.title == input_item
            ),
            None,
        )

        if project_id is not None:
            return project_id

    return default_project


async def parse_note(db: AsyncSession, mind_dump_note: str) -> ParseNoteRead:
    next_action_marker = " Next, "
    due_date_marker = " before "

    raw_title, next_action = mind_dump_note.split(next_action_marker)
    title, due_date = raw_title.split(due_date_marker)

    title = title[8:]  # extrart the "Need to" placeholder

    project_hint = await find_project_id_by_name(db, title)

    return ParseNoteRead(
        title=title,
        project_id_hint=project_hint,
        due_date_hint=due_date,
        next_action_hint=next_action,
    )
