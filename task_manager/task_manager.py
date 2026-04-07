from datetime import datetime
from task_model import Task
from data_manager import DataManager


users = DataManager.load_users()
logged_in = False


while not logged_in:
    username = input("Enter username: ")
    password = input("Enter password: ")

    for user in users:
        if user.username == username and user.password == password:
            print("\nLogin successful!")
            logged_in = True
            break
    if not logged_in:
        print("Invalid credentials, try again.")


# ===== Functions =====
def view_all():
    tasks = DataManager.load_tasks()
    if not tasks:
        print("No tasks found.")
        return

    for task in tasks:
        print("\n" + "-"*35)
        print(task)
        print("-"*35)


def reg_user():
    users = DataManager.load_users()
    new_username = input("New Username: ")
    for u in users:
        if u.username == new_username:
            print("Username already exists. Try again.")
            return

    new_password = input("New Password: ")
    confirm_password = input("Confirm Password: ")

    if new_password == confirm_password:
        with open("user.txt", "a") as file:
            file.write(f"\n{new_username}, {new_password}")
        print("User registered successfully!")
    else:
        print("Passwords do not match.")


def add_task():
    """
    Collects task details from user, creates a Task object,
    and saves it using the DataManager.
    """
    assigned_user = input("Username of person task is assigned to: ")
    task_title = input("Task title: ")
    task_description = input("Task description: ")
    todays_date = input("Todays date: ")
    due_date = input("Due date: ")
    completed = "No"
    task_complete = input("Is the task complete? (yes/no): ").lower()

    if task_complete == "yes":
        completed = "Yes"

    new_task = Task(
        assigned_user,
        task_title,
        task_description,
        todays_date,
        due_date,
        completed
    )

    current_tasks = DataManager.load_tasks()
    current_tasks.append(new_task)
    DataManager.save_all_tasks(current_tasks)

    print(f"\nTask '{task_title}' added successfully!")


def view_mine(username):
    tasks = DataManager.load_tasks()
    user_task_indices = []

    # Filter tasks by username using the Task objects
    for i, task in enumerate(tasks):
        if task.username == username:
            print(f"\nTask number: {i}")
            print(task)  # This uses the __str__ method in your Task class
            user_task_indices.append(i)

    if not user_task_indices:
        print("You have no tasks assigned.")
        return

    try:
        task_select = int(input("Select task number (-1 to go back): "))
        if task_select == -1:
            return
        if task_select not in user_task_indices:
            print("Invalid task selection.")
            return

        selected_task = tasks[task_select]
        choice = input("Mark as complete (m) or Edit (e): ").lower()

        if choice == 'm':
            selected_task.completed = "Yes"
            DataManager.save_all_tasks(tasks)
            print("Task updated!")

        elif choice == 'e':
            if selected_task.completed == "No":
                sub_choice = input(
                    "Edit due date (d) or assignee (a)? "
                ).lower()
                if sub_choice == 'd':
                    selected_task.due_date = input("Enter new due date: ")
                elif sub_choice == 'a':
                    selected_task.username = input("Enter new assignee: ")
                DataManager.save_all_tasks(tasks)
                print("Task edited successfully!")
            else:
                print("Cannot edit a completed task.")

    except ValueError:
        print("Please enter a valid number.")


def view_completed():
    with open("tasks.txt", "r") as file:

        lines = file.readlines()
        for i, line in enumerate(lines):

            temp = line.strip().split(", ")
            if temp[-1] == "Yes":

                print(
                    f"""Task number: {i}
                    Assigned user: {temp[0]}
                    Task: {temp[1]}
                    Task Description: {temp[2]}
                    Date Assigned: {temp[3]}
                    Due Date: {temp[4]}
                    Task Completed?: {temp[5]}"""
                )


def delete_task():
    with open("tasks.txt", "r") as file:

        lines = file.readlines()
        for i, line in enumerate(lines):

            temp = line.strip().split(", ")
            if len(temp) == 6:

                print(
                    f"""
                    Task number: {i}
                    Assigned user: {temp[0]}
                    Task: {temp[1]}
                    Task Description: {temp[2]}
                    Date Assigned: {temp[3]}
                    Due Date: {temp[4]}
                    Task Completed?: {temp[5]}"""
                )
        task_delete = int(input("Enter task number you wish to delete: "))

        lines.pop(task_delete)
        with open("tasks.txt", "w") as file:

            file.writelines(lines)
            print(f"Task number {task_delete} was successfully deleted\n")


def generate_reports():
    tasks = []

    with open("tasks.txt", "r") as file:
        for line in file:

            tasks.append(line.strip())

    total_tasks = len(tasks)
    completed_tasks = 0
    incompleted_tasks = 0
    overdue_tasks = 0

    for task in tasks:

        temp = task.split(", ")
        if temp[-1] == "Yes":

            completed_tasks += 1
        elif temp[-1] == "No":

            incompleted_tasks += 1
            try:

                due_date = datetime.strptime(temp[4], "%d %b %Y")

                if due_date < datetime.today():
                    overdue_tasks += 1

            except ValueError:
                print(f"Invalid date format for task: {temp[1]}")

    incomplete_percentage = (
        (incompleted_tasks / total_tasks) * 100 if total_tasks else 0
    )
    overdue_percentage = (
        (overdue_tasks / total_tasks) * 100 if total_tasks else 0
    )

    report = (
        f"Number of tasks generated and tracked is {total_tasks}\n"
        f"Number of tasks completed is {completed_tasks}\n"
        f"Number of uncompleted tasks is {incompleted_tasks}\n"
        f"Number of overdue tasks is {overdue_tasks}\n"
        f"Total percentage of incomplete tasks: {incomplete_percentage:.2f}%\n"
        f"Total percentage of overdue tasks: {overdue_percentage:.2f}%\n"
    )

    with open("task_overview.txt", "w") as file1:
        file1.write(report)

    users = []
    with open("user.txt", "r") as file:
        for line in file:

            temp = line.strip().split(", ")
            users.append(temp[0])

    total_users = len(users)

    report2 = (
        f"Number of users registered is: {total_users}\n"
        f"Number of tasks generated and tracked is: {total_tasks}\n\n"
    )

    for user in users:

        user_tasks = 0
        user_completed_tasks = 0
        user_incompleted_tasks = 0
        user_overdue_tasks = 0

        for task in tasks:
            parts = task.split(", ")

            if parts[0].strip() == user.strip():
                user_tasks += 1

                if parts[-1] == "Yes":
                    user_completed_tasks += 1
                elif parts[-1] == "No":
                    user_incompleted_tasks += 1

                    try:
                        due_date = datetime.strptime(parts[4], "%d %b %Y")
                        if due_date < datetime.today():
                            user_overdue_tasks += 1
                    except ValueError:
                        print(f"Invalid date format for task: {parts[1]}")

        task_percentage = (
            (user_tasks / total_tasks) * 100
            if total_tasks else 0
        )

        completed_percentage = (
            (user_completed_tasks / user_tasks) * 100
            if user_tasks else 0
        )

        incompleted_percentage = (
            (user_incompleted_tasks / user_tasks) * 100
            if user_tasks else 0
        )

        overdue_task_percentage = (
            (user_overdue_tasks / user_tasks) * 100
            if user_tasks else 0
        )

        report2 += (
            f"{user} has {user_tasks} assigned tasks\n"
            f"{user} has {task_percentage:.2f}% of the total tasks assigned\n"
            f"{user} has completed {completed_percentage:.2f}% "
            f"of their tasks\n"
            f"{user} has not completed {incompleted_percentage:.2f}% "
            f"of their tasks\n"
            f"{user} has {overdue_task_percentage:.2f}% "
            f"of their tasks overdue\n\n"
            )

    with open("user_overview.txt", "w") as file2:
        file2.write(report2)


def display_statistics():
    try:
        with open("task_overview.txt", "r") as file:
            print("\nTask Overview:\n")
            print(file.read())

    except FileNotFoundError:
        generate_reports()
        with open("task_overview.txt", "r") as file:
            print("\nTask Overview:\n")
            print(file.read())

    try:
        with open("user_overview.txt", "r") as file:
            print("\nUser Overview:\n")
            print(file.read())

    except FileNotFoundError:
        generate_reports()
        with open("user_overview.txt", "r") as file:
            print("\nUser Overview:\n")
            print(file.read())


while True:
    if username == "admin":
        menu = input("""Select one of the following options:
    r - register a user
    a - add task
    va - view all tasks
    vm - view my tasks
    vc - view completed tasks
    del - delete tasks
    ds - display statistics
    gr - generate reports
    e - exit
    : """).lower()
    else:
        menu = input("""Select one of the following options:
        a - add task
        va - view all tasks
        vm - view my tasks
        e - exit
        : """).lower()

    if menu == "r":
        if username == "admin":
            reg_user()
        else:
            print("Access Denied")

    elif menu == "a":
        add_task()

    elif menu == "va":
        view_all()

    elif menu == "vm":
        view_mine(username)

    elif menu == "vc":
        if username == "admin":
            view_completed()
        else:
            print("Access Denied")

    elif menu == "del":
        if username == "admin":
            delete_task()
        else:
            print("Access Denied")

    elif menu == "ds":
        display_statistics()
    elif menu == "gr":
        generate_reports()
    elif menu == "e":
        print("Goodbye!!!")
        exit()

    else:
        print("You have entered an invalid input. Please try again")
