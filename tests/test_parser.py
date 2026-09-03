from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.tevira_ai.db.models import Project
from src.tevira_ai.services.parser import parse_note


async def test_parse_note_accepts_valid_input(
    db_session: AsyncSession, test_project: list[Project], test_owner_id: UUID
):
    title = "finish the README for tevira-ai"
    project_id_hint = test_project[0].id
    due_date_hint = "friday."
    next_action_hint = "add setup commands."
    messy_note = f"{title} before {due_date_hint} Next, {next_action_hint}"

    response = await parse_note(
        owner_id=test_owner_id, db=db_session, mind_dump_note=messy_note
    )

    assert response.title == title
    assert response.project_id_hint == project_id_hint
    assert response.due_date_hint == due_date_hint
    assert response.next_action_hint == next_action_hint
