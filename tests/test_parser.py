from src.app.parser import parse_note
import src.app.state.memory as memory


def test_parse_note_accepts_valid_input():
    messy_note = (
        "Need to finish the README for SAT before Friday. Next, add setup commands"
    )
    response = parse_note(messy_note, memory.projects_in_memory)

    assert response.title == "finish the README for SAT"
    assert response.project_id_hint == "project_1"
    assert response.due_date_hint == "Friday."
    assert response.next_action_hint == "add setup commands"
