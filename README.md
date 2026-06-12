# Tevira-AI ![License: MIT](https://img.shields.io/badge/license-MIT-brightgreen) ![Python Versions](https://img.shields.io/badge/python-3.10_%7C_3.11_%7C_3.12_%7C_3.13_%7C_3.14-brightgreen)
A python API that stores your tasks, notes, projects and restores context for each of your projects so you can switch back to where you left it off without ever feeling lost again.

## ⚠ Status
### What works so far
- Running the API locally in localhost,

- `"/health"` - Ping server to check that it is working.

- `"/tasks"` - Creates and lists all tasks through GET and POST methods. Currently stores tasks in memory.

- `"/projects"` - Creates and lists all projects through GET and POST methods. Currently stores them in memory.

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
```

If on Windows run this instead:
```powershell
python -m venv venv
source venv\Scripts\Activate.ps1
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
### Endpoints
### Schemas

## 🛣 Next Steps
I am actively developing Tevira-AI and in the near future it will have more capabilities, some of them may be found below:
- Real SQL database with persistent storage, not just in memory storage.
- Auth

## License
MIT License. See [LICENSE](LICENSE)
