import textwrap  # For styling when printing to the terminal
from datetime import datetime, timezone  # For date validation and formatting
from getpass import getpass  # To obfuscate the password input in the terminal

from constants import DATETIME_FORMAT, TERMINAL_PRINT_WIDTH
from managers import UserManager
from models import Task


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
