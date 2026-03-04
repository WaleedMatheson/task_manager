# CLI Task Manager Program

A robust, Object-Oriented command-line application built in Python for managing users and tasks.

This program was developed with a strong focus on **Defensive Programming**, **Data Integrity**, and **Clean Code Architecture**, strictly adhering to modern Python standards and Ruff linter compliance.

## Key Technical Highlights for Reviewers

* **Defensive Programming & Validation:** Comprehensive input sanitisation and validation. Handles edge cases such as delimiter collisions (preventing CSV corruption from rogue commas), enforces alphanumeric-only usernames, and validates strict date formats using `try-except-else` control flows.
* **Object-Oriented Design (OOP):** Deeply modular architecture separating concerns into distinct classes (`User`, `Admin`, `Task`) and data managers (`UserManager`, `TaskManager`) to encapsulate logic and state.
* **Modular Refactoring:** Transitioned from a monolithic script to a professional multi-module architecture, improving maintainability and testability.
* **Linter & Standard Compliance:** The codebase passes strict Ruff linting, specifically engineered to maintain low McCabe Cyclomatic Complexity (C901), avoid Boolean Traps (FBT), and implement clean early-return/break logic (RET).
* **Safe File I/O:** Utilises Python's modern `pathlib` for cross-platform compatibility and explicitly enforces `utf-8` encoding to prevent character crashes across different operating systems.
* **Secure CLI Experience:** Integrates the `getpass` module to obfuscate passwords in the terminal and uses dynamic string formatting (`f-strings` with alignment padding and `textwrap`) to generate pixel-perfect, responsive statistics tables.

## Architecture Overview

The program is split into specialised modules to ensure a **Separation of Concerns**:

* **`main.py`**: The entry point. Uses a lightweight execution loop and dictionary-based dispatching for menu actions to keep the code flat and readable.
* **`models.py`**: Contains core data structures (`User`, `Admin`, `Task`). Utilises inheritance to manage different user permission levels.
* **`managers.py`**: Orchestrates data persistence. Handles the lifecycle of loading, instantiating, and saving objects to the data source.
* **`actions.py`**: The business logic layer. Contains the high-level functions for registering users, managing tasks, and generating reports.
* **`utils.py`**: A dedicated toolbox for reusable helper functions, specifically focused on recursive validation and CLI formatting.
* **`constants.py`**: Centralised configuration for file paths, date formats, and UI styling.

## Future Roadmap & Improvements

While the current version is a robust CLI tool, the following architectural enhancements are planned to improve scalability and performance:

### 1. Database Integration (SQLite)

* **Current State:** Data is stored in comma-separated `.txt` files.
* **The Goal:** Transition to a Relational Database Management System (RDBMS) using SQLite.
* **Why:** * **Data Integrity:** Enforce strict relationships between Users and Tasks using Foreign Keys.
  * **Concurrency:** Better handling of simultaneous read/write operations.
  * **Performance:** Replace O(n) file parsing with indexed SQL queries for faster data retrieval as the task count grows.

### 2. Password Hashing

* **Current State:** Passwords are stored in plain text.
* **The Goal:** Implement the `hashlib` or `bcrypt` library to store salted SHA-256 hashes.
* **Why:** To ensure industry-standard security practices and protect user credentials in the event of a data breach.

### 3. Unit Testing

* **The Goal:** Implement a comprehensive test suite using `pytest`.
* **Why:** To ensure that new features or refactors (like the SQLite transition) do not introduce regressions into the core business logic.

## How to Run the Program

**Prerequisites:** Python 3.x installed on your machine.

1. **Clone this repository:**

    ```bash
    git clone https://github.com/WaleedMatheson/task_manager.git
    ```

2. **Navigate to the project directory:**

    ```bash
    cd task_manager
    ```

3. **Run the program:**

    ```bash
    python src/main.py
    ```

*Note: The program requires a `data/user.txt` file with at least one admin user to function. It will automatically generate `data/tasks.txt` upon first run if missing.*

## Tech Stack

* **Language:** Python 3
* **Libraries:** `pathlib`, `datetime`, `getpass`, `textwrap`, `sys`
* **Code Quality:** Ruff (Linter)
