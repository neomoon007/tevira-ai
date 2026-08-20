import json

from src.tevira_ai.main import app

with open("docs/openai.json", "w") as docs_file:
    json.dump(app.openapi(), docs_file, indent=2)
