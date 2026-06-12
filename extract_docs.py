import json
from src.app.main import app

with open("openai.json", "w") as docs_file:
    json.dump(app.openapi(), docs_file, indent=2)
