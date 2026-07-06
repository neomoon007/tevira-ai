from src.app.schemas import (
    CaptureRead,
    CreateTaskProposal,
    CreateProgressNoteProposal,
    NonEmptyString,
    CreateTaskAction,
    CreateProgressNoteAction,
)
from src.app.parser import parse_note
from src.app.state.memory import projects_in_memory


def capture_from_text(raw_input: NonEmptyString) -> CaptureRead:
    parsed_input = parse_note(raw_input, projects_in_memory)

    return CaptureRead(
        raw_text=raw_input,
        parsed=parsed_input,
        proposed_actions=[
            CreateTaskAction(
                type="create_task",
                data=CreateTaskProposal(
                    title=parsed_input.title, due_date_hint=parsed_input.due_date_hint
                ),
            ),
            CreateProgressNoteAction(
                type="create_progress_note",
                data=CreateProgressNoteProposal(
                    next_action=parsed_input.next_action_hint
                ),
            ),
        ],
    )
