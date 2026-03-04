import sys  # For a safer exit() method

from actions import (
    add_task,
    delete_task,
    display_statistics,
    generate_report,
    login,
    register_user,
    view_all_tasks,
    view_completed_tasks,
    view_mine,
)
from constants import TASKS_FILE_PATH, TERMINAL_PRINT_WIDTH, USER_FILE_PATH
from managers import TaskManager, UserManager


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
