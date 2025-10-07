import os
import json

FILENAME = "tasks.json"

def load_tasks():
    """
    Load tasks from local JSON file. Return empty list if file not found or invalid.
    """

    if not os.path.exists(FILENAME):
        return []

    try:
        with open(FILENAME, "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        print("WARNING! Failed to read tasks.json. Starting with an empty list.")
        return []


def save_tasks(tasks):
    """
    Save task to json file.
    """

    try:
        with open(FILENAME, "w") as file:
            json.dump(tasks, file, indent = 4)
    except Exception as e:
        print(f"Error saving task: {e}")

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
    
    
def main():
    tasks = load_tasks()

    while True:
        print("\n=====TASK TRACKER=====")
        print("1. Add Task")
        print("2. Show Tasks")
        print("3. Mark Task as Done")
        print("4. Exit")

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
