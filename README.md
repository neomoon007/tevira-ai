# Tevira-AI

![Coverage](https://img.shields.io/badge/Coverage-93%25-brightgreen.svg)
![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3670A0?style=flat&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)
![PostgreSQL 18](https://img.shields.io/badge/PostgreSQL-18-4169E1?style=flat&logo=postgresql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/sqlalchemy-D71F00?style=flat&logo=sqlalchemy&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-blue.svg)

A python API that stores your tasks, notes, projects and restores context for each of your projects so you can switch back to where you left it off without ever feeling lost again.

<video src="https://github.com/user-attachments/assets/8fe6e6c0-2a4d-4d97-80dc-1860a5f800fe" controls="controls" width="100%">
</video>

## 📃 Documentation
You can check the endpoints and schemas by clicking on the badge below:

[![Swagger UI](https://img.shields.io/badge/-Swagger-%23Clojure?style=for-the-badge&logo=swagger&logoColor=white)](https://editor.swagger.io/?url=https://raw.githubusercontent.com/neomoon007/tevira-ai/refs/heads/main/docs/openai.json)

## 🎯 Core Feature
Context Restauration: The main feature of Tevira-AI is the ability to restore context from previous sessions. It gathers all of your relevant tasks and notes for your project at the press of a button.

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
- Running the API locally in localhost.

- Data persistency layer with the stack: Postgres (database), SQLAlchemy (object-relational mapper) and Alembic (migrations).

- `"/health"` - Ping server to check that it is working.

- `"/tasks"` - Full CRUD for tasks working.

- `"/projects"` - Full CRUD for projects working.

- `"/progress-notes"` - Full CRUD for progress-notes working.

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
> Make sure you have Python 3.10+ installed and Docker Desktop (With WSL integration if using WSL).
> Development is currently supported on Linux/WSL only. The app does not currently support Windows environment.

### 1 - Clone the repo:
```bash
git clone https://github.com/neomoon007/tevira-ai
cd tevira-ai
```

### 2 - Setup environment:

#### 2.1a - Through setup script (does all the manual steps below at once)
```bash
source setup.sh
```

Or if you wanna do it manually... Follow the steps below.

#### 2.1b - Create and activate python's virtual environment
```bash
python3 -m venv .venv 
source .venv/bin/activate
```

#### 2.2 - Setup the .env file
```bash
cp .env.example .env
```
The app is setup to work even if you don't change the placeholder values in `.env.example`, but it's recommended that you change the variables before running the app.

#### 2.3 - Install python dependencies
```bash
pip install -r requirements.txt
```

### 3. Start the API locally:
> Before starting the application make sure that Docker engine is running. If you are using WSL enable WSL integration through Docker Desktop>Settings>Resources>WSL Integration and check the box for "Enable integration with my default WSL distro".

#### 3.1a - Run the script below to start the application
```bash
./run.sh
```

Again, if you wanna do it manually anyways... Follow the steps below.

#### 3.1b - Initialize the docker containers
```bash
docker compose up -d
```

#### 3.2 - Check that PostgreSQL is ready
```bash
docker exec your-container pg_isready -U your_username -d your_database
```
Do not move to the next step until PostgreSQL is ready.

#### 3.3 - Run Alembic migrations
```bash
alembic upgrade head
```

#### 3.4 - Start Uvicorn server
```bash
uvicorn src.app.main:app --reload
```

### 4. Test the application:
Open `/docs` on your browser. FastAPI uses Swagger UI so you can test the endpoints manually.
```bash
http://127.0.0.1:8000/docs
```

### 5. Stop the application
On your terminal inside the repo directory run
```
<Ctrl+C> # This stops the uvicorn application
docker compose down
```

## 🛣 Next Steps
I am actively developing Tevira-AI and in the near future it will have more capabilities, some of them may be found below:
- **Deployment** I plan on deploying my project soon using a docker image in a VPS (Virtual Private Server).
- **Security and Login:** I plan to use OAuth in the future for login and security.
- **Authentication** I will create a authentication layer to separate each users' data.

## License
MIT License. See [LICENSE](LICENSE)
