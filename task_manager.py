# ===== Importing external modules ===========
import sys
from datetime import datetime
from pathlib import Path

# ==== Constants Section ====
USERS_FILE_PATH = Path(Path(__file__).parent / "users.txt")
TASKS_FILE_PATH = Path(Path(__file__).parent / "tasks.txt")


# ==== Class Section ====
class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.valid_commands = ["a", "va", "vm", "e"]

    def get_menu(self):
        return (
            "\nSelect one of the following options:\n"
            "\ta - add task\n"
            "\tva - view all tasks\n"
            "\tvm - view my tasks\n"
            "\te - exit\n"
            "Enter selection: "
        )

    def is_valid_command(self, user_input):
        return user_input in self.valid_commands


class Admin(User):
    def __init__(self, username: str, password: str):
        super().__init__(username, password)
        self.valid_commands = ["r", "a", "va", "vm", "e", "vc", "del", "ds", "gr"]

    def get_menu(self):
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
    def __init__(
        self,
        username: str,
        title: str,
        description: str,
        assigned_date: str,
        due_date: str,
    ):
        self.username = username
        self.title = title
        self.description = description
        self.assigned_date = assigned_date
        self.due_date = due_date
        self.is_completed = False

    def to_csv_string(self):
        task_status = "Yes" if self.is_completed else "No"
        return f"{self.username}, {self.title}, {self.description}, {self.assigned_date}, {self.due_date}, {task_status}"

    def complete_task(self):
        self.is_completed = True


class TaskManager:
    pass


# ==== Login Section ====
def login():
    pass


# ==== Main program loop Section ====
def main():
    current_user = Admin("testUser", "Password123")
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
