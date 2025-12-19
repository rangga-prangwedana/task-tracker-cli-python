import os
import json
from datetime import datetime
from tracemalloc import start
from typing import List, Dict, Optional

FILENAME = "tasks.json"
VALID_STATUSES = ["todo", "in-progress", "done"]

def load_tasks() -> List(Dict):
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




def save_tasks(tasks):
    """
    Save task to json file.
    """

    try:
        with open(FILENAME, "w") as file:
            json.dump(tasks, file, indent = 4)
    except Exception as e:
        print(f"Error saving task: {e}")


def timestamp_now() -> str:
    """
    Return current timestamp as a string in ISO format.
    """
    return datetime.now().isoformat(timespec="seconds")


def get_next_id(tasks):
    """
    Generate unique incremental integer ID.
    """
    if not tasks:
        return 1
    return max(task["id"] for task in tasks) + 1


#
# Core functions
#

def add_task(tasks):
    """Add new task(s) with description and default status."""
    # TODO: prompt user for number of tasks and their descriptions
    # use get_next_id() and timestamp_now()
    pass

def show_tasks(tasks, filter_status=None):
    """Display tasks optionally filtered by status."""
    # TODO: if filter_status provided, show only tasks matching it
    # otherwise, show all
    pass

def update_task(tasks):
    """Update task description."""
    # TODO: ask for ID, find matching task, modify description
    # update 'updatedAt' timestamp
    pass

def delete_task(tasks):
    """Delete task by ID."""
    # TODO: ask for ID, confirm, remove from list if found
    pass

def mark_task(tasks, new_status):
    """Change status of a task (todo/in-progress/done)."""
    # TODO: similar to 'mark as done' but allow all status types
    # validate new_status input
    pass


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
            try:
                n_tasks = int(input("How many tasks do you want to add: "))
                for _ in range(n_tasks):
                    task = input("Enter task: ").strip()
                    if task:
                        tasks.append({"task": task, "done":False})
                        print("Task added!")
                    else:
                        print("Empty task ignored.")
                save_tasks(tasks)
            except ValueError:
                print("Invalid number. Please enter an integer.")

        elif choice == "2":
            show_tasks(tasks)

        elif choice == "3":
            show_tasks(tasks)
            try:
                task_index = int(input("\nEnter the task number to mark as done,"))
                if 0 <= task_index < len(tasks):
                    tasks[task_index]["done"] = True
                    print("Task marked as done!")
                    save_tasks(tasks)
                else:
                    print("Invalid task number.")
            except ValueError:
                print("Please enter a valid integer.")

        elif choice == "4":
            print("Exiting Task Tracker.")
            save_tasks(tasks)
            break

        else:
            print("Invalid choice. Please try again.")    

if __name__ == "__main__":
    main()
