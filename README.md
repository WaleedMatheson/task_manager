# CLI Task Manager Program

A robust, Object-Oriented command-line application built in Python for managing users and tasks.

This program was developed with a strong focus on **Defensive Programming**, **Data Integrity**, and **Clean Code Architecture**, strictly adhering to modern Python standards and Ruff linter compliance.

## Key Technical Highlights for Reviewers

* **Defensive Programming & Validation:** Comprehensive input sanitisation and validation. Handles edge cases such as delimiter collisions (preventing CSV corruption from rogue commas), enforces alphanumeric-only usernames, and validates strict date formats using `try-except-else` control flows.
* **Object-Oriented Design (OOP):** Deeply modular architecture separating concerns into distinct classes (`User`, `Admin`, `Task`) and data managers (`UserManager`, `TaskManager`) to encapsulate logic and state.
* **Linter & Standard Compliance:** The codebase passes strict Ruff linting, specifically engineered to maintain low McCabe Cyclomatic Complexity (C901), avoid Boolean Traps (FBT), and implement clean early-return/break logic (RET).
* **Safe File I/O:** Utilises Python's modern `pathlib` for cross-platform compatibility and explicitly enforces `utf-8` encoding to prevent character crashes across different operating systems.
* **Secure CLI Experience:** Integrates the `getpass` module to obfuscate passwords in the terminal and uses dynamic string formatting (`f-strings` with alignment padding and `textwrap`) to generate pixel-perfect, responsive statistics tables.

## Architecture Overview

The program uses inheritance and specific manager classes to keep the execution loop clean and flat.

* **Models:** `User` (base class) and `Admin` (inherits from User, unlocking expanded menu actions). `Task` handles its own data formatting and CLI rendering.
* **Managers:** `UserManager` and `TaskManager` handle all file reading, instantiation of objects, and saving state back to the text files.
* **Helpers:** Isolated helper functions manage complex `while True` validation loops to keep the main logic highly readable and flat.

## How to Run the Program

**Prerequisites:** Python 3.x installed on your machine.

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/WaleedMatheson/task_manager.git
2. Navigate to the project directory:

   ```bash
   cd task_manager
   ```

3. Run the program:

   ```bash
   python main.py
   ```

*Note: The program will automatically generate the required `tasks.txt` data file upon initialisation if it does not already exist.*

*Note: There must be a `user.txt` file with at least one admin user for this program to work*

## Tech Stack

* **Language:** Python 3
* **Libraries:** `pathlib`, `datetime`, `getpass`, `textwrap`, `sys`
* **Code Quality:** Ruff (Linter)
