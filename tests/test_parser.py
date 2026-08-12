from src.tevira_ai.services.parser import parse_note


def test_parse_note_accepts_valid_input(db_session):
    messy_note = (
        "Need to finish the README for SAT before Friday. Next, add setup commands."
    )

    response = parse_note(db_session, messy_note)

    assert response.title == "finish the README for SAT"
    assert response.project_id_hint == "project_1"
    assert response.due_date_hint == "Friday."
    assert response.next_action_hint == "add setup commands."
