# --- INPUT STRUCTURE ---
# "Need to X before Y. Next, Z"
# Where X is the title, Y is the due_date and Z is the the next_action

# It checks the existing projects to match the project hint
# If it doesn't find any, it is currently hardcoded to return "Tevira-AI" as default

from src.app.schemas import ParseNoteRead
from dotenv import load_dotenv
import os

load_dotenv()

default_project = os.getenv("DEFAULT_PROJECT", "Inbox")
default_project_id = "project_1"  # TODO: Change from hardcoded default project to .env file based project config


def find_project(projects: dict, input: str) -> str:
    project_list = [project_loop.name for project_loop in projects.values()]
    input_list = input.split(" ")

    hint = list(set(project_list) & set(input_list))

    return hint[0] if hint and hint[0] != "" else default_project


# Currently only supports projects that don't have spaces inside of its name, meaning it supports one word names and names separated by -
def find_project_id_by_name(projects: dict, input: str) -> str:
    input_list = input.split(" ")

    for input_item in input_list:
        project_id = next(
            (project.id for project in projects.values() if project.name == input_item),
            None,
        )

        if project_id is not None:
            return project_id

    return default_project_id


def parse_note(mind_dump_note: str, projects: dict) -> ParseNoteRead:
    next_action_marker = " Next, "
    due_date_marker = " before "

    raw_title, next_action = mind_dump_note.split(next_action_marker)
    title, due_date = raw_title.split(due_date_marker)

    title = title[8:]  # extrart the "Need to" placeholder

    project_hint = find_project_id_by_name(projects, title)

    return ParseNoteRead(
        title=title,
        project_hint=project_hint,
        due_date_hint=due_date,
        next_action_hint=next_action,
    )
