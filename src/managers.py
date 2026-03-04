import sys
from pathlib import Path

from constants import EXPECTED_TASKS_FIELDS, EXPECTED_USER_FIELDS
from models import Admin, Task, User


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
            self.file_path.touch()

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
