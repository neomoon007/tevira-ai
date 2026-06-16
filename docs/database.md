# Database Schemas for Tevira-AI

## `projects` table
| Column | Type | Required? | Key? | Notes |
|---|---|---:|---|---|
| `id` | uuid | yes | primary key | project ID for notes and tasks to find it|
| `name` | text | yes | none | name of the project given by the user |

## `tasks` table
| Column | Type | Required? | Key? | Notes |
|---|---|---:|---|---|
| `id` | uuid | yes | primary key | task ID |
| `title` | text | yes | none | name of the task given by the user |
| `status` | text | yes | none | either `open` or `done` |
| `priority` | text | yes | none | possible values are: `low`, `medium` and `high` |
| `due_date` | text | no | none | stores the due_date for that task using `yyyy-MM-dd` format |
| `project_id` | uuid | no | foreign key | references back to `projects.id` |

## `progress_notes` table
| Column | Type | Required? | Key? | Notes |
|---|---|---:|---|---|
| `id` | uuid | yes | primary key | progress-note ID |
| `current_state` | text | yes | none | broader view of current project state |
| `last_session` | text | yes | none | what happened last session |
| `open_loops` | text[] | yes | none | text array of open loops, like a broad TODO list |
| `next_actions` | text[] | no | none | text array of exact next steps, narrower than open_loops | 
| `important_context` | text | no | none | things you need to remember about this project |
| `blockers` | text | no | none | dependencies that need follow up with other people |
| `project_id` | uuid | yes | foreign key | references back to `projects.id`, if no project is given, it defaults to `inbox` project |
| `confidence` | text | no | none | possible values are: `low`, `medium` or `high`. It is the confidence level of the AI model regarding the summary it produces |