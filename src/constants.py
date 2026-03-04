from pathlib import Path

USER_FILE_PATH = Path(__file__).parent.parent / "data/user.txt"
TASKS_FILE_PATH = Path(__file__).parent.parent / "data/tasks.txt"
TASK_OVERVIEW_FILE_PATH = Path(__file__).parent.parent / "data/task_overview.txt"
USER_OVERVIEW_FILE_PATH = Path(__file__).parent.parent / "data/user_overview.txt"
EXPECTED_USER_FIELDS = 3  # The number of columns in the user.txt file
EXPECTED_TASKS_FIELDS = 7  # The number of columns in the tasks.txt file
TERMINAL_PRINT_WIDTH = 80  # This is for styling the output to the CLI
DATETIME_FORMAT = (
    "%d-%m-%Y"  # This is for the strftime method used in the datetime class
)
