from fastapi import APIRouter
from src.app.schemas import NonEmptyString, CaptureRead, ProposedAction
from src.app.parser import parse_note
from src.app.state.memory import projects_in_memory

router = APIRouter(prefix="/capture", tags=["Capture"])


@router.post("/text")
def capture_mess(input: NonEmptyString):
    parsed_input = parse_note(input, projects_in_memory)

    # TODO: WIP - change from dummy values on proposed_actions to a variable called proposed_actions
    # proposed_actions = get_proposed_actions()
    # create a function that returns a list of ProposedAction objects with the real proposed actions

    return CaptureRead(
        raw_text=input,
        parsed=parsed_input,
        proposed_actions=[
            ProposedAction(type="create_task", title="WIP"),
            ProposedAction(type="create_progress_note", title="WIP"),
        ],
    )
