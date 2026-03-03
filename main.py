# ===== Importing external modules ===========
import sys  # For a safer exit() method
import textwrap  # For styling when printing to the terminal
from datetime import datetime, timezone  # For date validation and formatting
from getpass import getpass  # To obfuscate the password input in the terminal
from pathlib import Path  # The recommended approach to filepath management

# ==== Constants Section ====
USER_FILE_PATH = Path(__file__).parent / "user.txt"
TASKS_FILE_PATH = Path(__file__).parent / "tasks.txt"
TASK_OVERVIEW_FILE_PATH = Path(__file__).parent / "task_overview.txt"
USER_OVERVIEW_FILE_PATH = Path(__file__).parent / "user_overview.txt"
EXPECTED_USER_FIELDS = 3  # The number of columns in the user.txt file
EXPECTED_TASKS_FIELDS = 7  # The number of columns in the tasks.txt file
TERMINAL_PRINT_WIDTH = 80  # This is for styling the output to the CLI
DATETIME_FORMAT = (
    "%d-%m-%Y"  # This is for the strftime method used in the datetime class
)


# ==== Class Section ====
# I decided to use Classes to manage most of this program because it will be easier to
# keep track of if the user is regular or an admin, and to know what they can do
class User:
    def __init__(self, username: str, password: str):
        """
        Initialise the User object.

        :param username: User's username
        :type username: str
        :param password: User's password
        :type password: str
        """
        self.username = username
        self.password = password
        self.valid_commands = ["a", "va", "vm", "e"]

    def get_menu(self) -> str:
        """
        Get the menu string for the user that's logged in.

        :return: A string with a list of menu items
        :rtype: str
        """
        return (
            "\nMAIN MENU\n"
            "\nSelect one of the following options:\n"
            "\ta  - add task\n"
            "\tva - view all tasks\n"
            "\tvm - view my tasks\n"
            "\te  - exit\n\n"
            "Enter selection: "
        )

    def is_valid_command(self, user_input: str) -> bool:
        """
        Checks the input from a user against a list of valid commands.

        :param user_input: Command input from the user
        :type user_input: str
        :return: A bool if command entered is valid
        :rtype: bool
        """
        return user_input in self.valid_commands

    def to_csv_string(self) -> str:
        """
        Generates and returns a CSV ready string with all the values in the user object.

        :return: A formatted string with all the assigned values in the object
        :rtype: str
        """
        return f"{self.username}, {self.password}, No"


class Admin(User):
    def __init__(self, username: str, password: str):
        """
        Initialise the Admin object.

        :param username: Admin's username
        :type username: str
        :param password: Admin's password
        :type password: str
        """
        super().__init__(username, password)
        self.valid_commands = ["r", "a", "va", "vm", "e", "vc", "del", "ds", "gr"]

    def get_menu(self) -> str:
        """
        Get the menu string for the admin that's logged in.

        :return: A string with a list of menu items
        :rtype: str
        """
        return (
            "\nMAIN MENU\n"
            "\nSelect one of the following options:\n"
            "\tr   - register a user\n"
            "\ta   - add task\n"
            "\tva  - view all tasks\n"
            "\tvm  - view my tasks\n"
            "\tvc  - view completed tasks\n"
            "\tdel - delete a task\n"
            "\tds  - display statistics\n"
            "\tgr  - generate reports\n"
            "\te   - exit\n\n"
            "Enter selection: "
        )

    def to_csv_string(self):
        """
        Generates and returns a CSV ready string with all the values in the user object.

        :return: A formatted string with all the assigned values in the object
        :rtype: str
        """
        return f"{self.username}, {self.password}, Yes"


class UserManager:
    def __init__(self, file_path: Path):
        """
        Initialise UserManager object.

        :param file_path: File path to the user file
        :type file_path: Path
        """
        self.file_path = file_path
        self.users: list[User] = []
        self.load_users()

    def load_users(self):
        """Load all users from the user source into a `users` list within this object."""
        if not self.file_path.exists():
            print(
                "\t***** User file does not exist, please add it and run this program again *****",
            )
            sys.exit()

        with self.file_path.open(encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split(", ")

                if len(parts) != EXPECTED_USER_FIELDS:
                    continue

                username, password, is_admin = parts

                if is_admin == "Yes":
                    self.users.append(Admin(username, password))
                else:
                    self.users.append(User(username, password))

    def get_users(self):
        """Return a sorted list of all existing users."""
        return sorted([user.username for user in self.users])

    def save_users(self):
        """Save current users to file."""
        with self.file_path.open("w", encoding="utf-8") as file:
            for user in self.users:
                file.write(user.to_csv_string() + "\n")


class Task:
    def __init__(  # noqa: PLR0913
        self,
        assigned_by: str,
        assigned_to: str,
        title: str,
        description: str,
        date_assigned: str,
        due_date: str,
    ):
        """
        Initialise the Task object.

        :param assigned_by: The username the task is assigned by
        :type assigned_by: str
        :param assigned_to: The username the task is assigned to
        :type assigned_to: str
        :param title: Task title
        :type title: str
        :param description: Task description
        :type description: str
        :param date_assigned: Date task was assigned
        :type date_assigned: str
        :param due_date: Date task is due
        :type due_date: str
        """
        self.assigned_by = assigned_by
        self.assigned_to = assigned_to
        self.title = title
        self.description = description
        self.date_assigned = date_assigned
        self.due_date = due_date
        self.is_complete = False

    def to_csv_string(self) -> str:
        """
        Convert and return the assigned values in the object to a CSV string format.

        Also changes the bool value of `self.is_complete` to "Yes" or "No".

        :return: A string of all the assigned values in the object
        :rtype: str
        """
        task_status = "Yes" if self.is_complete else "No"
        return f"{self.assigned_by}, {self.assigned_to}, {self.title}, {self.description}, {self.date_assigned}, {self.due_date}, {task_status}"

    def complete_task(self):
        """Set `is_complete` attribute to True."""
        self.is_complete = True

    def display(self, task_number=None):
        """
        Prints a formatted version of the task to the terminal.

        `textwrap` library is used to make the longer strings look neater.

        :param task_number: If a task number is given it will be displayed
        :type task_number: int | None
        """
        print()
        if task_number:
            print(f"Task number:\t{task_number}")

        print(
            f"Task:\t\t{textwrap.fill(self.title, TERMINAL_PRINT_WIDTH, subsequent_indent='\t\t')}",
        )
        print(f"Assigned to:\t{self.assigned_to}")
        print(f"Assigned by:\t{self.assigned_by}")
        print(f"Date assigned:\t{self.date_assigned}")
        print(f"Due date:\t{self.due_date}")
        print(f"Task complete?\t{'Yes' if self.is_complete else 'No'}")
        print(
            f"Task description:\n    {textwrap.fill(self.description, TERMINAL_PRINT_WIDTH, subsequent_indent='    ')}",
        )
        print("_" * TERMINAL_PRINT_WIDTH)


class TaskManager:
    def __init__(self, file_path: Path):
        """
        Initialise TaskManager object.

        :param file_path: File path to the tasks file
        :type file_path: Path
        """
        self.file_path = file_path
        self.tasks: list[Task] = []
        self.load_tasks()

    def load_tasks(self):
        """Load all tasks from the tasks source into a `tasks` list in this object."""
        if not self.file_path.exists():
            print(
                "\t***** Tasks file does not exist, creating a blank new tasks file *****",
            )
            TASKS_FILE_PATH.touch()

        with self.file_path.open(encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split(", ")

                if len(parts) != EXPECTED_TASKS_FIELDS:
                    continue

                (
                    assigned_by,
                    assigned_to,
                    title,
                    description,
                    date_assigned,
                    due_date,
                    is_complete,
                ) = parts

                task = Task(
                    assigned_by,
                    assigned_to,
                    title,
                    description,
                    date_assigned,
                    due_date,
                )

                if is_complete == "Yes":
                    task.complete_task()

                self.tasks.append(task)

    def get_user_tasks(self, username: str) -> list[Task]:
        """
        Return a list of Task objects for the currently logged in user.

        :param username: Current user
        :type username: str
        :return: List of Task objects
        :rtype: list[Task]
        """
        return [task for task in self.tasks if task.assigned_to == username]

    def save_tasks(self):
        """Save current tasks to file."""
        with self.file_path.open("w", encoding="utf-8") as file:
            for task in self.tasks:
                file.write(task.to_csv_string() + "\n")


# ==== Functions ====
def login(user_manager: UserManager) -> User:
    """
    Prompt the user for their username and password.

    Password is obfuscated using the `getpass` library.
    Check the username and password against the users list in the UserManager object
    and if incorrect allow the user to try again.

    :param user_manager: UserManager object that contains the users list
    :type user_manager: UserManager
    :return: The User object for the username and password entered
    :rtype: User
    """
    while True:
        input_username = input("Username: ")
        input_password = getpass("Password: ")

        for user in user_manager.users:
            if input_username == user.username and input_password == user.password:
                print("\nYou've successfully logged in!")
                return user

        # Printing that username or password is incorrect to not let unauthorised persons know
        # if they got a username correct.
        print("\nThe username and/or password you've entered are incorrect")
        retry = input("\nWould you like to try again? (y/n): ")

        if retry != "y":
            print("_" * TERMINAL_PRINT_WIDTH)
            print("\n\t***** Exiting Program, Goodbye *****")
            print("_" * TERMINAL_PRINT_WIDTH)
            sys.exit()


def display_existing_users(user_manager: UserManager):
    """
    Prints out a comma-separated row of all existing users sorted in alphabetical order.

    :param user_manager: UserManager object that contains the users list
    :type user_manager: UserManager
    """
    print(
        "\nExisting list of users:"
        f"\n\t{textwrap.fill(', '.join(user_manager.get_users()), TERMINAL_PRINT_WIDTH)}",
    )


def add_task(current_user: User, task_manager: TaskManager, user_manager: UserManager):
    """
    Take inputs from a user to add a task.

    Checks against existing users to validate that the user exists.
    Validates the due date input.

    :param current_user: The current user object of the user that is logged in
    :type current_user: User
    :param task_manager: The TaskManager object that manages current tasks
    :type task_manager: TaskManager
    :param user_manager: UserManager object that contains the users list
    :type user_manager: UserManager
    """
    print("_" * TERMINAL_PRINT_WIDTH)
    print("\nADD TASK\n")
    print("\nEnter task details...")
    assigned_by = current_user.username

    while True:
        # Logic to make sure the entered user exists
        input_assigned_to = get_valid_user(user_manager)

        # Ensure the tasks.txt file doesn't break by replacing commas if the user uses them
        input_title = input("\tTitle: ").replace(",", ";")
        input_description = input("\tDescription: ").replace(",", ";")

        input_due_date = get_valid_date("\tDue Date (e.g. 24-04-2025): ")

        assigned_date = datetime.now(tz=timezone.utc).strftime(DATETIME_FORMAT)

        print("\nDetails entered...")
        print(f"\tAssigned to: {input_assigned_to}")
        print(f"\tTitle: {input_title}")
        print(f"\tDescription: {input_description}")
        print(f"\tDate Due: {input_due_date}")

        retry = input("\nAre these details correct? (y/n): ")

        if retry == "y":
            break
        print("Please enter task details again...")

    task = Task(
        assigned_by,
        input_assigned_to,
        input_title,
        input_description,
        assigned_date,
        input_due_date,
    )

    # Append task to memory and immediately synchronise with the text file.
    task_manager.tasks.append(task)
    task_manager.save_tasks()

    print("\n\t***** Task Added to File *****")


def register_user(user_manager: UserManager):
    """
    Register a new user via terminal input.

    Password inputs are obfuscated using the `getpass` library.

    :param user_manager: UserManager object that contains the users list
    :type user_manager: UserManager
    """
    minimum_password_length = 8

    print("_" * TERMINAL_PRINT_WIDTH)
    print("\nREGISTER NEW USER\n")
    print("\nEnter new user details...\n")
    print("Usernames must contain only letters and numbers")
    print(
        f"Passwords must be at least {minimum_password_length} characters long and cannot contain commas (,)",
    )

    # Get validated inputs via helper functions
    new_username = get_new_username(user_manager)
    new_password = get_new_password(min_length=minimum_password_length)

    # Admin Assignment Loop
    while True:
        input_is_admin = input("Give this user admin privileges? (y/n): ").lower()

        if input_is_admin == "y":
            user_manager.users.append(Admin(new_username, new_password))
            break

        if input_is_admin == "n":
            user_manager.users.append(User(new_username, new_password))
            break

        print("Invalid input, please try again...\n")

    user_manager.save_users()

    print("\n\t***** New User Registered *****")


def view_all_tasks(task_manager: TaskManager):
    """
    Print all tasks to the command line in a neatly formatted manner.

    :param task_manager: The TaskManager object that manages current tasks
    :type task_manager: TaskManager
    """
    # This is used for styling the width of the output to the CLI
    print("_" * TERMINAL_PRINT_WIDTH)
    print("\nVIEW ALL TASKS")

    if len(task_manager.tasks) == 0:
        print("\nThere are no tasks...")
        return

    print("_" * TERMINAL_PRINT_WIDTH)

    for task in task_manager.tasks:
        task.display()

    print(f"\nThere are a total of {len(task_manager.tasks)} tasks.")


def view_mine(current_user: User, task_manager: TaskManager, user_manager: UserManager):
    """
    Display the current user's tasks in a neatly formatted manner and provide an interactive menu to edit task details.

    :param current_user: The current user object of the user that is logged in
    :type current_user: User
    :param task_manager: The TaskManager object that manages current tasks
    :type task_manager: TaskManager
    :param user_manager: UserManager object that contains the users list
    :type user_manager: UserManager
    """
    my_tasks: list[Task] = task_manager.get_user_tasks(current_user.username)

    print("_" * TERMINAL_PRINT_WIDTH)
    print("\nVIEW MY TASKS")

    if not my_tasks:
        print("You have no tasks assigned to you...")
        return

    print(f"\nNumber of tasks assigned to you: {len(my_tasks)}")
    print("_" * TERMINAL_PRINT_WIDTH)

    # starting from 1 for aesthetics, later on there is logic to handle correct index use
    for task_number, task in enumerate(my_tasks, start=1):
        task.display(task_number=task_number)

    print(f"\nNumber of tasks assigned to you: {len(my_tasks)}")
    print("\n\tTo edit a task,")
    # Logic to edit tasks for current user
    input_task_number = get_valid_task_number(my_tasks)
    if not input_task_number:
        return

    task_to_edit = my_tasks[input_task_number - 1]
    changes_made = handle_task_edit(task_to_edit, user_manager)

    if changes_made:
        task_manager.save_tasks()
        print("\t***** Updated Task Saved to File *****")


def view_completed_tasks(task_manager: TaskManager):
    """
    View all completed tasks.

    :param task_manager: The TaskManager object that manages current tasks
    :type task_manager: TaskManager
    """
    completed_tasks = [task for task in task_manager.tasks if task.is_complete]

    print("_" * TERMINAL_PRINT_WIDTH)
    print("\nVIEW MY TASKS")
    print(f"\nNumber of completed tasks: {len(completed_tasks)}")

    if not completed_tasks:
        print("There are no completed tasks yet...\n")
        return

    print("_" * TERMINAL_PRINT_WIDTH)
    for task in completed_tasks:
        task.display()

    print(f"\nNumber of completed tasks: {len(completed_tasks)}")


def delete_task(task_manager: TaskManager):
    """
    Delete a task.

    :param task_manager: The TaskManager object that manages current tasks
    :type task_manager: TaskManager
    :return: Returns early (None) if the user chooses to exit the selection
    :rtype: None
    """
    print("_" * TERMINAL_PRINT_WIDTH)
    print("\nDELETE TASK")

    # starting from 1 for aesthetics, later on there is logic to handle correct index use
    for task_number, task in enumerate(task_manager.tasks, start=1):
        task.display(task_number=task_number)

    while True:
        print("\n\tTo delete a task,")
        input_index = get_valid_task_number(task_manager.tasks, allow_completed=True)
        if not input_index:
            return

        corrected_index = input_index - 1
        confirm_delete = input(
            f'\nAre you sure you want to delete task number {input_index}: "{task_manager.tasks[corrected_index].title}"? (y/n) ',
        )
        if confirm_delete != "y":
            continue
        break

    task_manager.tasks.pop(corrected_index)
    task_manager.save_tasks()

    print("\t***** Task Deleted *****")


def handle_task_edit(task: Task, user_manager: UserManager) -> bool:
    """
    Provides a sub-menu to edit a specific task's user, due date, or status.

    :param task: The task to be edited
    :type task: Task
    :param user_manager: UserManager object that contains the users list
    :type user_manager: UserManager
    :return: A True if a change is made, else False
    :rtype: bool
    """
    print(
        f"\nEditing Task: '{task.title}'\n"
        "\tu - change assigned user\n"
        "\td - change due date\n"
        "\tc - mark task as complete\n"
        "\te - return to main menu\n",
    )

    while True:
        selection = input("Enter selection: ").lower()

        if selection == "u":
            task.assigned_to = get_valid_user(user_manager)
            print(f"\nTask reassigned to: {task.assigned_to}")
            return True  # Signal that a change was made

        if selection == "d":
            task.due_date = get_valid_date("\tNew Due Date (e.g. 24-04-2025): ")
            print(f"\nDue date updated to: {task.due_date}")
            return True

        if selection == "c":
            task.complete_task()
            print(f"\nTask '{task.title}' marked as completed.")
            return True

        if selection == "e":
            return False  # No changes made/exited

        print("Invalid input, please try again...")


def get_valid_task_number(
    tasks: list[Task],
    *,
    allow_completed: bool = False,
) -> int | None:
    """
    A recursive function to check if the task number entered is valid.

    :param tasks: A list of tasks for the current user
    :type tasks: list[Task]
    :param allow_completed: Flag to determine if completed tasks can be selected
    :type allow_completed: bool
    :return: Returns the valid task number, or None if the user exits
    :rtype: int | None
    """
    if len(tasks) == 0:
        return None

    try:
        user_input = int(
            input("\tEnter task number, or -1 to return to main menu: "),
        )
    except ValueError:
        print("\nInvalid input, please try again...")
        return get_valid_task_number(tasks, allow_completed=allow_completed)
    else:
        if user_input == -1:
            return None

    if user_input < -1 or user_input > len(tasks) or user_input == 0:
        print("\nInvalid input, please try again...")
        return get_valid_task_number(tasks, allow_completed=allow_completed)

    # Check if completed tasks should be blocked
    if not allow_completed and tasks[user_input - 1].is_complete:
        print(
            "\nThis task is complete and cannot be edited, please try again...",
        )
        return get_valid_task_number(tasks, allow_completed=allow_completed)

    return user_input


def get_valid_date(prompt: str) -> str:
    """
    Repeatedly prompts the user for a date until a valid format is entered.

    :param prompt: The text to display to the user
    :return: A validated date string in DATETIME_FORMAT
    """
    while True:
        user_input = input(prompt)
        try:
            # We parse it just to validate, then return the string
            datetime.strptime(user_input, DATETIME_FORMAT).replace(tzinfo=timezone.utc)
        except ValueError:
            print(f"Invalid format. Please use {DATETIME_FORMAT} (e.g. 24-03-2026)...")
        else:
            return user_input


def get_valid_user(user_manager: UserManager) -> str:
    """
    Prompt for and validate an existing user.

    :param user_manager: UserManager object that contains the users list
    :type user_manager: UserManager
    """
    display_existing_users(user_manager)
    existing_users = user_manager.get_users()

    while True:
        input_username = input("\n\tAssign to: ")
        if input_username in existing_users:
            return input_username
        print("User doesn't exist, try again...")


def get_new_username(user_manager: UserManager) -> str:
    """
    Helper to prompt for and validate a unique, alphanumeric username.

    :param user_manager: UserManager object that contains the users list
    :type user_manager: UserManager
    :return: The validated username
    :rtype: str
    """
    # Fetch existing users to prevent duplicate usernames.
    display_existing_users(user_manager)
    existing_users = user_manager.get_users()
    while True:
        username = input("\n\tNew Username: ").strip()
        if not username:
            print("Username cannot be empty, try again...")
            continue
        if not username.isalnum():
            print("Username must be alphanumeric (no spaces/symbols), try again...")
            continue
        if username in existing_users:
            print("User already exists, try again...")
            continue
        return username


def get_new_password(min_length: int = 8) -> str:
    """
    Helper to prompt for and validate a secure password.

    :param min_length: Minimum password length, defaults to 8
    :type min_length: int, optional
    :return: The validated password
    :rtype: str
    """
    while True:
        password = getpass("\tPassword: ")
        if len(password) < min_length:
            print(f"\nPassword must be at least {min_length} characters, try again...")
            continue
        if "," in password:
            print("Password cannot contain commas, try again...")
            continue

        repeat = getpass("\tRepeat password: ")
        if password != repeat:
            print("\nPasswords do not match, try again...")
            continue
        return password


def generate_report(task_manager: TaskManager, user_manager: UserManager):
    """
    Takes all the data from the TaskManager and UserManager objects to generate a report.

    Outputs the reports to files.

    :param task_manager: The TaskManager object that manages current tasks
    :type task_manager: TaskManager
    :param user_manager: UserManager object that contains the users list
    :type user_manager: UserManager
    """
    print("_" * TERMINAL_PRINT_WIDTH)
    print("\nGENERATING REPORT...")
    date_report_generated = datetime.now(tz=timezone.utc).strftime(
        f"{DATETIME_FORMAT} %H:%M",
    )

    ### Tasks reporting
    total_tasks = len(task_manager.tasks)  # Also used for users reporting
    total_completed_tasks = len(
        [task for task in task_manager.tasks if task.is_complete],
    )
    total_incomplete_tasks = total_tasks - total_completed_tasks

    # An overdue task is strictly defined as incomplete and having a due date in the past
    total_overdue_tasks = len(
        [
            task
            for task in task_manager.tasks
            if not task.is_complete
            and datetime.strptime(task.due_date, DATETIME_FORMAT).replace(
                tzinfo=timezone.utc,
            )
            < datetime.now(tz=timezone.utc)
        ],
    )

    # Using a ternary operator to prevent division by zero if the system has no tasks for all percentage calculations
    percentage_incomplete_tasks: float = (
        round((total_incomplete_tasks / total_tasks) * 100, 2)
        if total_tasks != 0
        else 0
    )

    percentage_overdue_tasks: float = (
        round((total_overdue_tasks / total_tasks) * 100, 2) if total_tasks != 0 else 0
    )

    # Write tasks report to the task overview file
    with TASK_OVERVIEW_FILE_PATH.open("w", encoding="utf-8") as file:
        file.write(
            f"{date_report_generated}, {total_tasks}, {total_completed_tasks}, {total_incomplete_tasks}, {total_overdue_tasks}, {percentage_incomplete_tasks}, {percentage_overdue_tasks}\n",
        )

    ### Users reporting
    total_users = len(user_manager.users)
    user_report = {}

    for user in user_manager.users:
        total_user_tasks = len(
            [task for task in task_manager.tasks if task.assigned_to == user.username],
        )
        total_user_completed_tasks = len(
            [
                task
                for task in task_manager.tasks
                if task.assigned_to == user.username and task.is_complete
            ],
        )
        total_user_incomplete_tasks = total_user_tasks - total_user_completed_tasks
        total_user_overdue_tasks = len(
            [
                task
                for task in task_manager.tasks
                if not task.is_complete
                and datetime.strptime(task.due_date, DATETIME_FORMAT).replace(
                    tzinfo=timezone.utc,
                )
                < datetime.now(tz=timezone.utc)
                and task.assigned_to == user.username
            ],
        )

        # Using a ternary operator to prevent division by zero if the system has no tasks for all percentage calculations
        percentage_user_total_tasks: float = (
            round((total_user_tasks / total_tasks) * 100, 2) if total_tasks != 0 else 0
        )
        percentage_user_total_completed_tasks: float = (
            round((total_user_completed_tasks / total_user_tasks) * 100, 2)
            if total_user_tasks != 0
            else 0
        )
        percentage_user_total_incomplete_tasks: float = (
            round((total_user_incomplete_tasks / total_user_tasks) * 100, 2)
            if total_user_tasks != 0
            else 0
        )
        percentage_user_overdue_tasks: float = (
            round((total_user_overdue_tasks / total_user_tasks) * 100, 2)
            if total_user_tasks != 0
            else 0
        )

        user_report[user.username] = {
            "total_tasks": total_user_tasks,
            "%_total_tasks": percentage_user_total_tasks,
            "%_complete_tasks": percentage_user_total_completed_tasks,
            "%_incomplete_tasks": percentage_user_total_incomplete_tasks,
            "%_overdue_tasks": percentage_user_overdue_tasks,
        }

    # Write users report to the user overview file
    with USER_OVERVIEW_FILE_PATH.open("w", encoding="utf-8") as file:
        file.write(f"{total_users}, {total_tasks}\n")
        for username, stats in user_report.items():
            file.write(
                f"{username}, {stats['total_tasks']}, {stats['%_total_tasks']}, {stats['%_complete_tasks']}, {stats['%_incomplete_tasks']}, {stats['%_overdue_tasks']}\n",
            )

    print("\n\t***** Tasks/Users Report Generated *****")


def display_statistics(task_manager: TaskManager, user_manager: UserManager):
    """
    Display statistics from files about tasks and users.

    :param task_manager: The TaskManager object that manages current tasks
    :type task_manager: TaskManager
    :param user_manager: UserManager object that contains the users list
    :type user_manager: UserManager
    """
    print("_" * TERMINAL_PRINT_WIDTH)
    print("\nDISPLAY STATISTICS")

    lw = 19  # Label width for text alignment when printing to the CLI
    # Ensure report files exist and actually have data before reading
    if (
        not TASK_OVERVIEW_FILE_PATH.exists()
        or TASK_OVERVIEW_FILE_PATH.stat().st_size == 0
        or not USER_OVERVIEW_FILE_PATH.exists()
        or USER_OVERVIEW_FILE_PATH.stat().st_size == 0
    ):
        generate_report(task_manager, user_manager)

    ### Tasks
    print("\nTasks Statistics...")
    with TASK_OVERVIEW_FILE_PATH.open(encoding="utf-8") as file:
        (
            date_report_generated,
            total_tasks,
            total_completed_tasks,
            total_incomplete_tasks,
            total_overdue_tasks,
            percentage_incomplete_tasks,
            percentage_overdue_tasks,
        ) = file.readline().strip().split(", ")

    print(f"\t{'Report Date & Time:':<{lw}} {date_report_generated}")
    print(f"\t{'Total Tasks:':<{lw}} {total_tasks}")
    print(f"\t{'Completed Tasks:':<{lw}} {total_completed_tasks}")
    print(
        f"\t{'Incomplete Tasks:':<{lw}} {total_incomplete_tasks} ({float(percentage_incomplete_tasks):.2f}%)",
    )
    print(
        f"\t{'Overdue Tasks:':<{lw}} {total_overdue_tasks} ({float(percentage_overdue_tasks):.2f}%)",
    )

    ### Users
    header = "| Username | Total | Total (%) | Completed (%) | Incomplete (%) | Overdue (%) |"
    table_width = len(header)

    print()
    print("\nUser Statistics...")
    with USER_OVERVIEW_FILE_PATH.open(encoding="utf-8") as file:
        total_users, total_tasks = file.readline().strip().split(", ")
        print(f"\tTotal Users: {total_users}")
        print(f"\tTotal Tasks: {total_tasks}")
        print()
        print("Users Tasks:")
        print("_" * table_width)
        print(header)
        print("-" * table_width)
        for line in file:
            (
                username,
                total_user_tasks,
                percentage_user_total_tasks,
                percentage_user_total_completed_tasks,
                percentage_user_total_incomplete_tasks,
                percentage_user_overdue_tasks,
            ) = line.strip().split(", ")

            # Print each user's stats, aligning strings to the left and floats to the right to match the header widths
            print(
                f"| {username:<8} | {int(total_user_tasks):<5} | {float(percentage_user_total_tasks):>9.2f} | {float(percentage_user_total_completed_tasks):>13.2f} | {float(percentage_user_total_incomplete_tasks):>14.2f} | {float(percentage_user_overdue_tasks):>11.2f} |",
            )
        print("-" * table_width)
        print()


# ==== Main Program Loop Section ====
def main():
    """
    The main execution loop for the task management program.

    Initialises data managers, handles user authentication, and
    routes menu selections to the appropriate functions.
    """
    task_manager = TaskManager(TASKS_FILE_PATH)
    user_manager = UserManager(USER_FILE_PATH)

    print("_" * TERMINAL_PRINT_WIDTH)
    print("\n\tWelcome to Your Task Manager, Please Login\n")

    # Assigns the relevant User|Admin object to current_user
    # Also this way the menu inputs from the user are validated by the User|Admin object
    current_user = login(user_manager)

    # Mapping menu inputs to actions to reduce complexity.
    # The lambda keyword creates an anonymous function, delaying execution
    # until the user actually selects the corresponding menu option.
    menu_actions = {
        "r": lambda: register_user(user_manager),
        "a": lambda: add_task(current_user, task_manager, user_manager),
        "va": lambda: view_all_tasks(task_manager),
        "vm": lambda: view_mine(current_user, task_manager, user_manager),
        "vc": lambda: view_completed_tasks(task_manager),
        "del": lambda: delete_task(task_manager),
        "ds": lambda: display_statistics(task_manager, user_manager),
        "gr": lambda: generate_report(task_manager, user_manager),
        # For the exit, using a tuple allows the lambda to run multiple functions
        "e": lambda: (
            print("_" * TERMINAL_PRINT_WIDTH),
            print("\n\t***** Exiting Program, Goodbye *****"),
            print("_" * TERMINAL_PRINT_WIDTH),
            sys.exit(),
        ),
    }

    while True:
        print("_" * TERMINAL_PRINT_WIDTH)
        while True:
            menu = input(current_user.get_menu())
            if not current_user.is_valid_command(menu):
                print("Invalid input, please try again...")
                continue
            break

        # Execute the matched function from the dictionary
        menu_actions[menu]()


if __name__ == "__main__":
    main()
