DEFAULT_PROJECT_FALLBACK = "Tevira-AI"

# --- INPUT STRUCTURE ---
# "Need to X before Y. Next, Z"
# Where X is the title, Y is the due_date and Z is the the next_action

# It checks the existing projects to match the project hint
# If it doesn't find any, it is currently hardcoded to return "Tevira-AI" as default


def find_project(projects: dict, input: str):
    project_list = [project_loop.name for project_loop in projects.values()]
    input_list = input.split(" ")

    hint = list(set(project_list) & set(input_list))

    return hint[0] if hint[0] != "" else DEFAULT_PROJECT_FALLBACK


def parse_note(mind_dump_note: str, projects: dict):
    next_action_marker = " Next, "
    due_date_marker = " before "

    raw_title, next_action = mind_dump_note.split(next_action_marker)
    title, due_date = raw_title.split(due_date_marker)

    project_hint = find_project(projects, title)

    return {
        "title": title,
        "project_hint": project_hint,
        "due_date_hint": due_date,
        "next_action_hint": next_action,
    }
