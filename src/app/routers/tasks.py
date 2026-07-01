from src.app.state.memory import tasks_in_memory, task_id_number
from src.app.validator import validate_project_id, get_project_tasks, get_task_by_id
from fastapi import APIRouter
from src.app.schemas import TaskCreate, TaskRead, TaskUpdate, NonEmptyString

router = APIRouter(prefix="/tasks", tags=["Tasks"])


# -- "/tasks" --
@router.post("", status_code=201)
def create_task(task: TaskCreate) -> TaskRead:
    global task_id_number
    task_id_number += 1

    task_id = f"task_{task_id_number}"

    new_task = TaskRead(
        **task.model_dump(),  # Dumps all `task` fields here, no need to type them manually.
        id=task_id,
        status="open",
    )

    tasks_in_memory.append(new_task)

    return new_task


@router.get("")
def show_tasks(project_id: str = None, task_id: str = None) -> list[TaskRead]:  # type: ignore
    if project_id is None and task_id is None:
        return tasks_in_memory

    if project_id is not None and task_id is None:
        validate_project_id(project_id)
        return get_project_tasks(project_id)

    if project_id is None and task_id is not None:
        return [get_task_by_id(task_id)]

    if project_id is not None and task_id is not None:
        validate_project_id(project_id)
        project_tasks = get_project_tasks(project_id)
        return [get_task_by_id(task_id, project_tasks)]


@router.patch("/{task_id}")
def update_task(task_id: NonEmptyString, updated_task: TaskUpdate) -> TaskRead:
    matching_task = get_task_by_id(task_id)
    merged_task = {
        **matching_task.model_dump(),
        **updated_task.model_dump(exclude_none=True),
    }

    task_index = tasks_in_memory.index(matching_task)
    tasks_in_memory[task_index] = TaskRead(**merged_task)

    return TaskRead(**merged_task)


@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: str):
    # TODO: change the parameter from str type to a validation (similar to Depends(validate_project_id(project_id) or NonEmptyString at least)
    matching_task = get_task_by_id(task_id)
    task_index = tasks_in_memory.index(matching_task)
    del tasks_in_memory[task_index]

    return
