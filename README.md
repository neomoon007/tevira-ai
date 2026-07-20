# Tevira-AI ![License: MIT](https://img.shields.io/badge/license-MIT-brightgreen) ![Python Versions](https://img.shields.io/badge/python-3.10_%7C_3.11_%7C_3.12_%7C_3.13_%7C_3.14-brightgreen)
A python API that stores your tasks, notes, projects and restores context for each of your projects so you can switch back to where you left it off without ever feeling lost again.

## 🎯 Core Feature
Context Restauration: The main feature of Tevira-AI is the ability to restore context from previous sessions. It gathers all of your relevant tasks and notes for your project at the press of a button.

Currently using in-memory storage for faster MVP development, PostgreSQL will be used in the future for production.

Example of context restauration through `"/context/{project_id}"` endpoint:
```
{
  "project": {
    "name": "Study for finals",
    "id": "project_2"
  },
  "current_state": "Already reviewed math and physics. One week away from finals",
  "open_tasks": [
    {
      "title": "Study for English test",
      "priority": "high",
      "due_date": "2026-06-08",
      "project_id": "project_2",
      "id": "task_2",
      "status": "open"
    },
    {
      "title": "Finish homework assignment for math class",
      "priority": "medium",
      "due_date": "2026-06-10",
      "project_id": "project_2",
      "id": "task_3",
      "status": "open"
    }
  ],
  "open_loops": [
    "Need to review all subjects before finals (besides math and physics)"
  ],
  "next_actions": {
    "title": "Study for English test",
    "priority": "high",
    "due_date": "2026-06-08",
    "project_id": "project_2",
    "id": "task_2",
    "status": "open"
  },
  "important_context": "Late assignments will receive 50% less grade"
}
```

## ⚠ Status
### What works so far
- Running the API locally in localhost,

- `"/health"` - Ping server to check that it is working.

- `"/tasks"` - Full CRUD for tasks working. Currently stores tasks in memory for MVP purposes.

- `"/projects"` - Full CRUD for projects working. Currently stores projects in memory for MVP purposes.

- `"/progress-notes"` - Full CRUD for progress-notes working. Currently stores notes in memory for MVP purposes.

- `"/context/{project_id}"` - Restores context for the given project. It gathers info from notes and tasks regarding the project and returns them in a structured way. See Schemas for more info.

- `"/capture/text"` - Parses input from user and suggests actions based on the input. 

    > Current valid input: `Need to X before Y. Next, Z` Where X is the task, Y is the due date - has natural language support for dates - and Z is the next action. 
    
    **Example input:** "Need to finish tests for Tevira-AI before friday. Next, deploy app"

    **Example output:**
    ```
    {
    "raw_text": "Need to finish tests for Tevira-AI before friday. Next, deploy app",
    "parsed": {
        "title": "finish tests for Tevira-AI",
        "project_id_hint": "project_1",
        "due_date_hint": "friday.",
        "next_action_hint": "deploy app"
    },
    "proposed_actions": [
        {
        "type": "create_task",
        "data": {
            "title": "finish tests for Tevira-AI",
            "due_date_hint": "friday.",
            "project_hint": "project_1"
        }
        },
        {
        "type": "create_progress_note",
        "data": {
            "next_action": "deploy app"
        }
        }
    ]
    }
    ```
    It suggests a project for the task if it finds a project name inside your task title, if it doesn't find a project it defaults to Inbox, `project_1` is Inbox.

- `"/actions/apply"` - This endpoint creates tasks and progress-notes using the suggestions given in `/capture/text`.
    
    **Example input :**
    ```
    {
      "type": "create_task",
      "data": {
        "title": "finish tests for Tevira-AI",
        "due_date_hint": "friday.",
        "project_hint": "project_1"
      }
    }
    ```
    **Example output:**

    Obs: date was 2026-07-09 so next friday would be 2026-07-10
    ```
    {
    "status": "applied",
    "action": {
        "type": "create_task",
        "data": {
        "title": "finish tests for Tevira-AI",
        "due_date_hint": "friday.",
        "project_hint": "project_1"
        }
    },
    "result": {
        "title": "finish tests for Tevira-AI",
        "priority": "medium",
        "due_date": "2026-07-10",
        "project_id": "project_1",
        "id": "task_1",
        "status": "open"
    }
    }
    ```

## 🚀 Getting started
### 1. Clone the repo:
```bash
git clone https://github.com/neomoon007/tevira-ai
cd tevira-ai
```

### 2. Setup environment:
Make sure you have Python 3.10+ installed and Docker Desktop (With WSL integration if using WSL).
> Development is currently supported on Linux/WSL only. The app hasn't been tested on natively on Windows yet.

On Linux run:
```bash
python3 -m venv .venv
source .venv/bin/activate
cp .env.example .env
```

### 3. Install dependencies:
```bash
pip3 install -r requirements.txt
```

### 4. Start the API locally:
```bash
docker compose up -d
uvicorn src.app.main:app --reload
```

### 5. Test the application:
Open `/docs` on your browser. FastAPI uses Swagger UI so you can test the endpoints manually.
```bash
http://127.0.0.1:8000/docs
```

### 6. Stop the application
On your terminal inside the repo directory run
```
<Ctrl+C> # This stops the uvicorn application
docker compose down
```

## 📃 Documentation
You can also check the endpoints and schemas by clicking on the badge below:

[![Swagger UI](https://img.shields.io/badge/-Swagger-%23Clojure?style=for-the-badge&logo=swagger&logoColor=white)](https://editor.swagger.io/?url=https://raw.githubusercontent.com/neomoon007/tevira-ai/refs/heads/main/docs/openai.json)

## 🛣 Next Steps
I am actively developing Tevira-AI and in the near future it will have more capabilities, some of them may be found below:
- **Real SQL database with persistent storage (PostgreSQL):** Currently using In-Memory storage to develop the core logic faster without having to deal with a real database just yet. This is what I'll be working on the next few days it's going to be the next feature added.
- **Security and Login:** I plan to use OAuth in the future for login and security.

## License
MIT License. See [LICENSE](LICENSE)
