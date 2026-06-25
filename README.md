# Tevira-AI ![License: MIT](https://img.shields.io/badge/license-MIT-brightgreen) ![Python Versions](https://img.shields.io/badge/python-3.10_%7C_3.11_%7C_3.12_%7C_3.13_%7C_3.14-brightgreen)
A python API that stores your tasks, notes, projects and restores context for each of your projects so you can switch back to where you left it off without ever feeling lost again.

## 🎯 Core Feature
Context Restauration: The main feature of Tevira-AI is the ability to restore context from previous sessions. It gathers all of your relevant tasks and notes for your project at the press of a button.

Currently using in-memory storage for faster MVP development, PostgreSQL will be used in the future for production ready app.

Example of context restauration through `"/context/{project_id}"` endpoint:
```
Project: Study for finals
Current stage: Already reviewed math and physics. One week away from finals
Open tasks:
    1. Title: Study for english test
    Priority: High
    Due date: 2026-06-08
    Status: open

    2. Title: Finish homework assignment for math class
    Priority: medium
    Due date: 2026-06-10
    Status: open

Open loops: Need to review all subjects before finals (besides math and physics)
Next actions: Study for english test
Important context: Late assignments will receive 50% less grade
```

## ⚠ Status
### What works so far
- Running the API locally in localhost,

- `"/health"` - Ping server to check that it is working.

- `"/tasks"` - Full CRUD for tasks working. Currently stores tasks in memory for MVP purposes.

- `"/projects"` - Full CRUD for projects working. Currently stores tasks in memory for MVP purposes.

- `"/progress-notes"` - Creates and lists all notes through GET and POST methods. Currently stores notes in memory.

- `"/context/{project_id}"` - Restores context for the given project. It gathers info from notes and tasks regarding the project and returns them in a structured way. See Schemas for more info.

## 🚀 Getting started
### 1. Clone the repo:
```bash
git clone https://github.com/neomoon007/tevira-ai
cd tevira-ai
```

### 2. Setup environment:
Make sure you have Python 3.10+ installed.

On Linux run:
```bash
python -m venv venv
source venv/bin/activate
cp .env.example .env
```

If on Windows run this instead:
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
Copy-Item .env.example .env
```

### 3. Install dependencies:
```bash
pip install -r requirements.txt
```

### 4. Start the API locally:
```bash
uvicorn src.app.main:app --reload
```

### 5. Test the application:
Open `/docs` on your browser. FastAPI uses Swagger UI so you can test the endpoints manually.
```bash
http://127.0.0.1:8000/docs
```

## 📃 Documentation
You can also check the endpoints and schemas by clicking on the badge below:

[![Swagger UI](https://img.shields.io/badge/-Swagger-%23Clojure?style=for-the-badge&logo=swagger&logoColor=white)](https://editor.swagger.io/?url=https://raw.githubusercontent.com/neomoon007/tevira-ai/refs/heads/main/docs/openai.json)

## 🛣 Next Steps
I am actively developing Tevira-AI and in the near future it will have more capabilities, some of them may be found below:
- **Real SQL database with persistent storage (PostgreSQL):** Currently using In-Memory storage to develop the core logic faster without having to deal with a real database just yet.
- **Security and Login:** I plan to use OAuth in the future for login and security.

## License
MIT License. See [LICENSE](LICENSE)
