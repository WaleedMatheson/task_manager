import textwrap

from constants import TERMINAL_PRINT_WIDTH


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
