from gettext import find
import os
import json
from datetime import datetime
#from tracemalloc import start
from typing import _ReturnT_nd_co, List, Dict, Optional

FILENAME = "tasks.json"
VALID_STATUSES = ["todo", "in-progress", "done"]

def load_tasks() -> List[Dict]:
    """
    Load tasks from local JSON file. Return empty list if file not found or invalid.
    If old format detected, migrate it.
    """

    if not os.path.exists(FILENAME):
        return []

    try:
        with open(FILENAME, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"WARNING! Failed to read {FILENAME}: {e}. Starting with an empty list.")
        return []
    
    # Validate list data
    if not isinstance(data, list): 
        print(f"{FILENAME} format unrecognized. Starting with an empty list.")
        return []

    
    # Detect old format files and migrate
    migrated = False
    new_list = []
    for item in data:
        if isinstance(item, dict) and "task" in item and "done" in item:
            status = "done" if item.get("done") else "todo"
            now = timestamp_now()
            new_item = {
                "id": None, # Only temporary, assign ID after loop
                "description": item.get("task", "").strip(),
                "status": status,
                "createdAt": item.get("createdAt", now),
                "updatedAt": item.get("updatedAt", now),
            }
            new_list.append(new_item)
            migrated = True
        elif isinstance(item, dict) and "id" in item and "description" in item:
            new_list.append(item)
        else:
            continue

    if migrated:
        for idx, itm in enumerate(new_list, start=1):
            itm["id"] = idx
        save_tasks(new_list)
        print("Migrated tasks from old format to the new format.")

    return new_list




def save_tasks(tasks: List[Dict]) -> None:
    """
    Save task to json file.
    Overwrite existing file.
    """

    try:
        with open(FILENAME, "w", encoding="utf-8") as file:
            json.dump(tasks, file, indent = 4, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving task: {e}")


def timestamp_now() -> str:
    """
    Return current timestamp as a string in ISO format.
    """
    return datetime.now().isoformat(timespec="seconds")


def get_next_id(tasks: List[Dict]) -> int:
    """
    Generate unique incremental integer ID.
    """
    if not tasks:
        return 1
    try:
        max_id = max(task.get("id",0) for task in tasks)
        return max_id + 1
    except Exception:
        return 1

def find_task_by_id(tasks: List[Dict], task_id: int) -> Optional[Dict]:
        """
        Return task dict with given id or None if not found.
        """
        for t in tasks:
            if t.get("id") == task_id:
                return t 
        return None

def print_task(task: Dict) -> None:
    """
    Print single tasks.
    """
    print(
        f"[{task['id']}] {task['description']}"
            f"({task['status']}) created: {task['createdAt']} updated: {task['updatedAt']}"
    )

#
# Core functions
#

def add_task(tasks: List[Dict]) -> None:
    """
    Add new task(s) with description and default status.
    Assign id(s) and timestamps.
    """
    try:
        raw = input("How many tasks do you want to add? (enter a number): ").strip()
        n = int(raw)
        if n <= 0:
            print("Number must be positive.")
            return
    except ValueError:
        print("Invalid number. Aborting operation.")
        return

    # Loop for adding task(s)
    for _ in range(n):
        desc = input("Enter task description: ").strip()
        if not desc:
            print("Empty description. Skipping description.")
            continue
        new_id = get_next_id(tasks)
        now = timestamp_now()
        task = {
            "id": new_id,
            "description": desc,
            "status": "todo", 
            "createdAt": now,
            "updatedAt": now,
        }
        tasks.append(task)
        print(f"Added task id: {new_id}.")


def show_tasks(tasks, filter_status=None):
    """Display tasks optionally filtered by status."""
    if filter_status:
        filter_status = filter_status.strip().lower()
        if filter_status not in VALID_STATUSES:
            print(f"'{filter_status}' is invalid status filter. Valid: {', '.join(VALID_STATUSES)}")
            return
        filtered = {t for t in tasks if t.get("status") == filter_status}
        print(f"\n=== Tasks (status: {filter_status}) ===")
    else:
        filtered = tasks
        print(f"\n=== All tasks ===")

    if not filtered:
        print("No task to show.")
        return

def update_task(tasks: List[Dict]) -> None:
    """Update task description by id."""
    try:
        raw = input("Enter task id to update: ").strip()
        task_id = int(raw)
    except ValueError:
        print("Invalid id.")
        return
    
    task = find_task_by_id(tasks, task_id)
    if not task:
        print(f"No task found with id {task_id}.")
        return

    print("Current task: ")
    print_task(task)
    new_desc = input("Enter new description for task (leave empty to cancel): ").strip()
    if not new_desc:
        print("Update cancelled.")
        return

    task["description"] = new_desc
    task["updatedAt"] = timestamp_now()
    print(f"Task with id {task_id} updated succesfully.")

def delete_task(tasks: List[Dict]) -> None:
    """Delete task by ID."""
    try:
        raw = input("Enter task id to delete: ").strip()
        task_id = int(raw)
    except ValueError:
        print("Invalid id.")
        return

    task = find_task_by_id(tasks, task_id)
    if not task:
        print(f"Task with id {task_id} no found.")
        return


    print("Task to delete: ")
    print_task(task)
    confirm = input("Are you sure want to DELETE this task? (y/N):").strip().lower()
    if confirm in {"y", "yes"}:
        tasks.remove(task)
        print(f"Task {task_id} deleted.")
    else:
        print("Delete cancelled.")


def mark_task(tasks: List[Dict], status: Optional[str] = None) -> None:
    """
    Mark status for tasks.
    If the status is None, prompt for status.
    """
    try:
        raw = input("Enter task id to change status: ").strip()
        task_id = int(raw)
    except ValueError:
        print("Invalid id.")
        return

    task = find_task_by_id(tasks, task_id)
    if not task:
        print(f"No task found with id {task_id}.")
        return

    if status is None:
        status = input(f"Enter new status ({'/'.join(VALID_STATUSES)}): ").strip().lower()

    if status not in VALID_STATUSES:
        print(f"{status} is an invalid status. Valid status options: {'/'.join(VALID_STATUSES)}")
        return

    old = task["status"]
    task["status"] = status
    task["updatedAt"] = timestamp_now()
    print(f"Task {task_id} status changed: {old} --> {status}")

'''
def show_tasks(tasks):
    """
    Display all tasks with their status.
    """

    if not tasks:
        print("\nNo tasks found.")
        return

    print("\nTasks:")

    for index, task in enumerate(tasks):
        status = "Done" if task["done"] else "Not Done"
        print(f"{index + 1}. {tasks[task]} - {status}")
  '''   
    
def main():
    tasks = load_tasks()

    try:
        while True:
            print("\n=====TASK TRACKER=====")
            print("1. Add Task")
            print("2. Show Tasks")
            print("3. Show by Status (todo / in-progress / done)")
            print("4. Update Task")
            print("5. Mark Task as Done")
            print("6. Delete Task")
            print("7. Exit")

            choice = input("Enter your choice:")

            if choice == "1":
                add_task(tasks)
                save_tasks(tasks)
            elif choice == "2":
                show_tasks(tasks)
            elif choice == "3":
                filt = input("Enter status to filter (todo/in-progress/done): ").strip().lower()
                show_tasks(tasks, filt)
            elif choice == "4":
                update_task(tasks)
                save_tasks(tasks)
            elif choice == "5":
                mark_task(tasks)
                save_tasks(tasks)
            elif choice == "6":
                delete_task(tasks)
                save_tasks(tasks)
            elif choice == "7":
                print("Closing application....")
                save_tasks(tasks)
                break
            else:
                print("Invalid choice. Please try again.")    

    except KeyboardInterrupt:
        print("\nKeyboard interrupt detected. Saving tasks ...")
        save_tasks(tasks)




if __name__ == "__main__":
    main()
