# tevira-ai
Tevira AI helps you organize your messy mind into actionable items. Dump your mind, it takes care of it for you.

## How to run locally

Start development server:
```bash
uvicorn app.main:app --reload
```

Initial health-check endpoint:
```bash
curl http://127.0.0.1:8000/health
```