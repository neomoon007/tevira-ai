from src.app.parser import parse_note


def test_parse_note_accepts_valid_input(temp_projects):
    messy_note = (
        "Need to finish the README for SAT before Friday. Next, add setup commands"
    )
    response = parse_note(messy_note, temp_projects)

    assert response.title == "Need to finish the README for SAT"
    assert response.project_hint == "SAT"
    assert response.due_date_hint == "Friday."
    assert response.next_action_hint == "add setup commands"
