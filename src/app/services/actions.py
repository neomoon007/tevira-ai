from src.app.schemas import (
    ProposedAction,
    ApplyActionResponse,
    CreateTaskProposal,
    TaskRead,
)


def apply_action(action: ProposedAction) -> ApplyActionResponse:
    return ApplyActionResponse(
        status="applied",
        action=ProposedAction(
            type="create_task",
            data=CreateTaskProposal(
                title="My first task",
                due_date_hint="Friday",
            ),
        ),
        result=TaskRead(id="task_1", title="My first task"),
    )
