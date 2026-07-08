import pytest
import src.app.state.memory as memory
from src.app.schemas import ProjectRead, ProgressNoteRead, TaskRead
from datetime import date, timezone, datetime
from fastapi.testclient import TestClient
from src.app.main import app


@pytest.fixture(autouse=True)
def reset_state():
    memory.progress_notes_id_number = 0
    memory.progress_notes_in_memory.clear()
    memory.project_id_number = 0
    memory.projects_in_memory.clear()
    memory.task_id_number = 0
    memory.tasks_in_memory.clear()

    memory.progress_notes_in_memory.extend(
        [
            ProgressNoteRead(
                project_id="project_1",
                current_state="Week 08 got to finish soon",
                last_session="Week 08 halfway through",
                open_loops=["not finished", "WIP", "TBA"],
                next_actions="Finish week 08",
                important_context="One step at a time",
                blockers=["No blockers"],
                id="note_1",
                updated_at=datetime.now(timezone.utc),
            ),
            ProgressNoteRead(
                project_id="project_2",
                current_state="SAT",
                last_session="SAT",
                open_loops=["not finished", "WIP", "TBA"],
                next_actions="SAT",
                important_context="One step at a time",
                blockers=["No blockers"],
                id="note_2",
                updated_at=datetime.now(timezone.utc),
            ),
            ProgressNoteRead(
                project_id="project_3",
                current_state="Tevira-AI",
                last_session="Tevira-AI",
                open_loops=["not finished", "WIP", "TBA"],
                next_actions="Tevira-AI",
                important_context="One step at a time",
                blockers=["No blockers"],
                id="note_3",
                updated_at=datetime.now(timezone.utc),
            ),
            ProgressNoteRead(
                project_id="project_4",
                current_state="Tech",
                last_session="Tech",
                open_loops=["not finished", "WIP", "TBA"],
                next_actions="Tech",
                important_context="One step at a time",
                blockers=["No blockers"],
                id="note_4",
                updated_at=datetime.now(timezone.utc),
            ),
            ProgressNoteRead(
                project_id="project_5",
                current_state="Home",
                last_session="Home",
                open_loops=["not finished", "WIP", "TBA"],
                next_actions=None,
                important_context="One step at a time",
                blockers=["No blockers"],
                id="note_5",
                updated_at=datetime.now(timezone.utc),
            ),
        ]
    )

    memory.projects_in_memory["project_1"] = ProjectRead(name="SAT", id="project_1")
    memory.projects_in_memory["project_2"] = ProjectRead(
        name="Tevira-AI", id="project_2"
    )
    memory.projects_in_memory["project_3"] = ProjectRead(name="Tech", id="project_3")
    memory.projects_in_memory["project_4"] = ProjectRead(name="foo", id="project_4")
    memory.projects_in_memory["project_5"] = ProjectRead(name="Home", id="project_5")

    memory.tasks_in_memory.extend(
        [
            TaskRead(
                title="Hello World!",
                priority="high",
                due_date=date.today(),
                project_id="project_1",
                id="task_1",
                status="open",
            ),
            TaskRead(
                title="SAT",
                priority="medium",
                due_date=date.today(),
                project_id="project_1",
                id="task_2",
                status="open",
            ),
            TaskRead(
                title="Tevira-AI",
                priority="low",
                due_date=date.today(),
                project_id="project_2",
                id="task_3",
                status="open",
            ),
            TaskRead(
                title="bro",
                priority="high",
                due_date=date.today(),
                project_id="project_2",
                id="task_4",
                status="done",
            ),
            TaskRead(
                title="This is the way",
                priority="high",
                due_date=date.today(),
                project_id="project_5",
                id="task_5",
                status="open",
            ),
        ]
    )
    yield


@pytest.fixture(scope="session")
def client():
    return TestClient(app)
