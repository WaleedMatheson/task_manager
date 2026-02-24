# ===== Importing external modules ===========
import sys
from datetime import datetime, timezone
from getpass import getpass
from pathlib import Path

# ==== Constants Section ====
USER_FILE_PATH = Path(Path(__file__).parent / "user.txt")
TASKS_FILE_PATH = Path(Path(__file__).parent / "tasks.txt")
EXPECTED_USER_FIELDS = 3


# ==== Class Section ====
# I decided to use Classes to manage most of this program because it will be easier to
# keep track of if the user is regular or an admin, and to know what they can do
class User:
    def __init__(self, username: str, password: str):
        """
        Initialise the User object.

        :param username: Users username
        :type username: str
        :param password: Users password
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
            "\nSelect one of the following options:\n"
            "\ta - add task\n"
            "\tva - view all tasks\n"
            "\tvm - view my tasks\n"
            "\te - exit\n"
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


class Admin(User):
    def __init__(self, username: str, password: str):
        """
        Initialise the Admin object.

        :param username: Admins username
        :type username: str
        :param password: Admins password
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
            "\nSelect one of the following options:\n"
            "\tr - register a user\n"
            "\ta - add task\n"
            "\tva - view all tasks\n"
            "\tvm - view my tasks\n"
            "\tvc - view completed tasks\n"
            "\tdel - delete a task\n"
            "\tds - display statistics\n"
            "\tgr - generate reports\n"
            "\te - exit\n"
            "Enter selection: "
        )


class Task:
    def __init__(  # noqa: PLR0913
        self,
        assigned_by: str,
        assigned_to: str,
        title: str,
        description: str,
        assigned_date: str,
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
        :param assigned_date: Date task was assigned
        :type assigned_date: str
        :param due_date: Date task is due
        :type due_date: str
        """
        self.assigned_by = assigned_by
        self.assigned_to = assigned_to
        self.title = title
        self.description = description
        self.assigned_date = assigned_date
        self.due_date = due_date
        self.is_completed = False

    def to_csv_string(self) -> str:
        """
        Convert and return the assigned value in the object to a CSV string format.

        Also changes the bool value of `is_completed` to "Yes" or "No".

        :return: A string of all the assigned values in the object
        :rtype: str
        """
        task_status = "Yes" if self.is_completed else "No"
        return f"{self.assigned_by}, {self.assigned_to}, {self.title}, {self.description}, {self.assigned_date}, {self.due_date}, {task_status}"

    def complete_task(self):
        """Set `is_completed` to True."""
        self.is_completed = True


class TaskManager:
    pass


# ==== Functions ====
def login() -> User | Admin:
    """
    Prompt the user for their username and password.

    Password is obfuscated using the `getpass` library.
    Check the username and password against the `user.txt` file and if incorrect allow the user to try again.
    If the username and password are valid, then check if it's a User or Admin.

    :return: The User or Admin object for the username and password entered
    :rtype: User | Admin
    """
    while True:
        input_username = input("Username: ")
        # Using getpass library to obfuscate the password when it's entered in the CLI
        input_password = getpass("Password: ")

        with Path.open(USER_FILE_PATH) as user_file:
            for line in user_file:
                parts = line.strip().split(", ")

                if len(parts) == EXPECTED_USER_FIELDS:
                    file_username = parts[0]
                    file_password = parts[1]
                    file_is_admin = parts[2]

                    if (
                        input_username == file_username
                        and input_password == file_password
                    ):
                        print("\nYou've successfully logged in!")
                        if file_is_admin == "Yes":
                            return Admin(input_username, input_password)
                        return User(input_username, input_password)

            # Printing that username or password is incorrect to not let unauthorised persons know
            # if they got a username correct.
            print("\nThe username or password you've entered is incorrect")
            retry = input("would you like to try again? (y/n): ")

            if retry != "y":
                print("Exiting program...")
                sys.exit()


def display_users() -> list:
    """
    Prints out a comma separated row of all existing users then returns a list of all users.

    :return: A list of all existing users
    :rtype: list
    """
    users = []
    with Path.open(USER_FILE_PATH) as user_file:
        for line in user_file:
            parts = line.strip().split(", ")

            if len(parts) == EXPECTED_USER_FIELDS:
                file_username = parts[0]
                users.append(file_username)

    users.sort()
    print(f"Existing list of users: {', '.join(users)}")
    return users


def add_task(current_user: User | Admin):
    """
    Take inputs from a user to add a task.

    Checks against existing users to validate that the user exists.
    Validates the due date inputted.

    :param current_user: The current user object of the user that is logged in
    :type current_user: User | Admin
    """
    print("Enter task details...")
    assigned_by = current_user.username

    # Logic to make sure the entered user exists
    existing_users = display_users()
    while True:
        input_assigned_to = input("\tAssign to: ")
        if input_assigned_to not in existing_users:
            print("\nUser does not exist, try again...\n")
            continue
        break

    while True:
        input_title = input("\tTitle: ")
        input_description = input("\tDescription: ")

        while True:
            input_due_date = input("\tDue Date (e.g. 24-04-2025): ")
            # Using a try/except statement along with the datetime library to
            # make sure the date entered by the user is in the correct format.
            # This could help later on when generating reports
            try:
                datetime.strptime(input_due_date, "%d-%m-%Y").replace(
                    tzinfo=timezone.utc,
                )
                break

            except ValueError:
                print("Date format incorrect, try again...")

        assigned_date = datetime.now(tz=timezone.utc).strftime("%d-%m-%Y")

        print("Details entered...")
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

    with Path.open(TASKS_FILE_PATH, "a") as tasks_file:
        tasks_file.write(task.to_csv_string() + "\n")

    print("Task added to file...")


def register_user():
    """Register a new user by taking inputs from an admin."""
    print("Enter new user details:")

    # Get existing users to make sure the new username isn't already in the user file
    existing_users = display_users()
    while True:
        input_username = input("\tUsername: ")
        if input_username not in existing_users:
            break
        print("User already exists, try username again...")

    while True:
        input_password = getpass("Password: ")
        repeat_password = getpass("Repeat password: ")
        if input_password == repeat_password:
            break
        print("Passwords don't match, try password again...")

    input_is_admin = input("Give this user admin privileges? (y/n) ").lower()
    is_admin = "Yes" if input_is_admin == "y" else "No"

    with Path.open(USER_FILE_PATH, "a") as user_file:
        user_file.write(f"{input_username}, {input_password}, {is_admin}\n")

    print("New user registered...")


# ==== Main program loop Section ====
def main():
    # Assigns the relevant User|Admin object to current_user
    # Also this way the menu inputs from the user is validated by the User|Admin object
    current_user = login()
    while True:
        menu = input(current_user.get_menu())
        if not current_user.is_valid_command(menu):
            print("This is an invalid command, try again...")
            continue
        break

    while True:
        if menu == "r":
            # TODO: Implement the following functionality
            """This code block will add a new user to the user.txt file
            - You can use the following steps:
                - Request input of a new username
                - Request input of a new password
                - Request input of password confirmation.
                - Check if the new password and confirmed password are the same
                - If they are the same, add them to the user.txt file,
                otherwise present a relevant message"""

        elif menu == "a":
            # TODO: Implement the following functionality
            """This code block will allow a user to add a new task to task.txt file
            - You can use these steps:
                - Prompt a user for the following:
                    - the username of the person whom the task is assigned to,
                    - the title of the task,
                    - the description of the task, and
                    - the due date of the task.
                - Then, get the current date.
                - Add the data to the file task.txt
                - Remember to include 'No' to indicate that the task is not
                complete.
            """

        elif menu == "va":
            # TODO: Implement the following functionality
            """This code block will read the task from task.txt file and
            print to the console in the format of Output 2 presented in the PDF
            You can do it in this way:
                - Read a line from the file.
                - Split that line where there is comma and space.
                - Then print the results in the format shown in the Output 2 in
                the PDF
                - It is much easier to read a file using a for loop."""

        elif menu == "vm":
            # TODO: Implement the following functionality
            """This code block will read the task from task.txt file and
            print to the console in the format of Output 2 presented in the PDF
            You can do it in this way:
                - Read a line from the file
                - Split the line where there is comma and space.
                - Check if the username of the person logged in is the same as the 
                username you have read from the file.
                - If they are the same you print the task in the format of Output 2
                shown in the PDF """

        elif menu == "vc":
            # TODO: Implement functionality
            pass

        elif menu == "del":
            # TODO: Implement functionality
            pass

        elif menu == "ds":
            # TODO: Implement functionality
            pass

        elif menu == "gr":
            # TODO: Implement functionality
            pass

        elif menu == "e":
            print("Goodbye!!!")
            sys.exit()

        else:
            print("You have entered an invalid input. Please try again")


if __name__ == "__main__":
    main()
