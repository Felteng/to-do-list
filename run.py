import gspread
from datetime import datetime
from google.oauth2.service_account import Credentials
from prettytable import PrettyTable


# Global variables

# SCOPE and credentials code from Code Institutes Love Sandwiches project
# Code Institute code
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPEAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPEAD_CLIENT.open("to_do_list")
# Code institute code ends here
TO_DO_SHEET = SHEET.worksheet("To-do")
COMPLETED_SHEET = SHEET.worksheet("Completed")


def get_to_do_list():
    """Retrieve the tasks and their respective deadlines
    from the to_do_list spreadsheet.

    Return them both as 2 separate lists to allow
    looping through them to print the table.
    """
    tasks = TO_DO_SHEET.col_values(1)
    deadlines = TO_DO_SHEET.col_values(2)
    return tasks, deadlines


def get_completed_list():
    """Retrieve the data from all 3 columns in the completed sheet
    to allow for iteration and display to the user.

    Return the 3 as 3 separate lists to allow
    looping through them to print the table.
    """
    tasks = COMPLETED_SHEET.col_values(1)
    deadlines = COMPLETED_SHEET.col_values(2)
    time_completed = COMPLETED_SHEET.col_values(3)
    return tasks, deadlines, time_completed


def validate_index_input(action):
    """Call this function for any action
    that needs the user to select an index to access.

    Raise ValueError if the index input is smaller than 1
    or if it's not a number.
    """
    while True:
        try:
            task_index = int(input(f"Which task index would you like to {action}?\n"))
            if task_index < 1:
                raise ValueError

            return task_index

        except ValueError:
            print("That is not a valid number. Has to be a number, that is bigger than 0.")


def validate_date_input(action):
    """Call this function whenever user is expected to provide a deadline.

    Checks if the date is in the correct format for consistency.

    Checks if the date is valid in the sense that it has not already passed.
    """
    while True:
        try:
            if action == "update":
                deadline = input("Update deadline (yyyy-mm-dd) to:\n")

            elif action == "add":
                deadline = input("Task deadline (yyyy-mm-dd):\n")
            """Parse deadline string into datetime object
            for comparing and format testing.
            """
            date_input = datetime.strptime(deadline, "%Y-%m-%d")

            """Get current date and parse it to a string with the right format
            using strftime(), then parse it back into an object
            with strptime to compare against date_input.
            """
            date_now = datetime.strptime(datetime.now().strftime("%Y-%m-%d"), "%Y-%m-%d")

            if date_input < date_now:
                print("That date has already passed")
            else:
                return deadline

        except ValueError:
            print(f"{deadline} does not match format: yyyy-mm-dd")


def confirm_action(action, task_index):
    while True:
        confirm = input(f"Are you sure you want to {action} task {task_index}? y/n\n").lower()
        if confirm == "y" or confirm == "yes":
            return "y"

        elif confirm == "n" or confirm == "no":
            return "n"

        else:
            print(f"Did not recognize '{confirm}'.")


def user_decision():
    """Ask the user what they wish to see from the spreadsheet.

    If the input in user_input was faulty,
    alert the user and allow a new attempt.

    If user wants to see the to-do list provide a follow-up question
    of whether they would like to edit it as well.
    """
    print("Type: 'view' to show To-do List.\nType 'history' to show completed tasks.\n")
    user_input = input("Enter your command here:\n").lower()
    if user_input == "view":
        display_to_do_list()

        while True:
            edit_decision = input("Would you like to edit the list? y/n\n").lower()
            if edit_decision == "y":
                edit_list()

            elif edit_decision == "n":
                user_decision()

            else:
                print(f"Did not recognize '{edit_decision}'.")

    elif user_input == "history":
        display_completed_list()
        user_decision()

    else:
        print(f"Invalid command.. You entered: '{user_input}'.")
        user_decision()


def display_to_do_list():
    """
    If 'view' was chosen in user_decision() then display a table of
    all the tasks that are yet to be completed in the 'To-do' worksheet.
    """
    tasks, deadlines = get_to_do_list()
    table = PrettyTable(["Index", "Task", "Deadline"])

    index = 1
    """Start from 2nd index in list to avoid the spreadsheet headings."""
    for task, deadline in zip(tasks[1:], deadlines[1:]):
        table.add_row([index, task, deadline])
        index += 1
    print(table)


def display_completed_list():
    """
    If 'history' was chosen in user_decision() then display a table of
    all the tasks in the 'Completed' worksheet.
    """
    tasks, deadlines, times = get_completed_list()
    table = PrettyTable(["Index", "Task", "Deadline", "Completed"])

    index = 1
    """Start from 2nd index in list to avoid the spreadsheet headings."""
    for task, deadline, time in zip(tasks[1:], deadlines[1:], times[1:]):
        table.add_row([index, task, deadline, time])
        index += 1
    print(table)
    user_decision()


def edit_list():
    """Grab input from user as to how they would like to edit the to do list.

    Call the function relevant to the choice.

    If the input does not match options alert user and allow another attempt.
    """
    edit_type = input("""
Type 'edit' to edit a list item
Type 'add' to add an item to the list
Type 'complete' to complete a task
Type 'remove' to remove an item from the list
Or type 'none' to stop editing
""").lower()

    print("")
    if edit_type == "edit":
        edit_task()

    elif edit_type == "add":
        add_task()

    elif edit_type == "complete":
        complete_task()

    elif edit_type == "remove":
        remove_task()

    elif edit_type == "none":
        user_decision()

    else:
        print(f"Did not recognize '{edit_type}'.")
        edit_list()


def edit_task():
    """Ask the user which row in the list they would like to edit.

    Add 1 to task_index since row 1 in the sheet has the headings.

    Let the user provide new input to update the relevant cells.
    """
    task_index = validate_index_input("edit")
    task_index += 1

    while True:
        cell_to_edit = input("Would you like to edit 'task', 'deadline', or 'both'?\n").lower()
        if cell_to_edit == "task":
            new_task = input("Update task to:\n")
            TO_DO_SHEET.update_cell(task_index, 1, new_task)
            print("Task updated successfully\n")
            break

        elif cell_to_edit == "deadline":
            new_deadline = validate_date_input("update")
            TO_DO_SHEET.update_cell(task_index, 2, new_deadline)
            print("Deadline updated successfully\n")
            break

        elif cell_to_edit == "both":
            new_task = input("Update task to:\n")
            new_deadline = validate_date_input("update")
            TO_DO_SHEET.update_cell(task_index, 1, new_task)
            TO_DO_SHEET.update_cell(task_index, 2, new_deadline)
            print("Task and deadline updated successfully\n")
            break

        else:
            print(f"Did not recognize '{cell_to_edit}'.")

    display_to_do_list()
    edit_list()


def add_task():
    """Ask the user for a task description and task deadline to append
    the new task to the sheet.
    """
    task = input("Task to be added:\n")
    deadline = validate_date_input("add")
    print("Adding task...")
    TO_DO_SHEET.append_row([task, deadline])
    print("Task added successfully\n")
    display_to_do_list()
    edit_list()


def complete_task():
    """Ask the user which task index they would like to complete.

    Get confirmation if the index is correct, if user is not sure,
    return to edit_list(), if user is sure, proceed with completion.

    Add a value of 1 to task_index when changing a sheet
    since row 1 in the sheet has the headings.

    Add the date this function was carried out to the completed history sheet.
    """
    task_index = validate_index_input("complete")
    confirm = confirm_action("complete", task_index)
    if confirm == "y":
        print(f"Completing task {task_index}...")
        today_date = datetime.now().date()
        to_completed_sheet = TO_DO_SHEET.row_values(task_index + 1)

        to_completed_sheet.append(str(today_date))
        COMPLETED_SHEET.append_row(to_completed_sheet)
        TO_DO_SHEET.delete_rows(task_index + 1)

        print("Task completed successfully\n")

    display_to_do_list()
    edit_list()


def remove_task():
    """Ask the user which task index they would like to remove.

    Get confirmation if the index is correct, if user is sure,
    proceed with removal, if user is not sure return to edit_list().

    Add a value of 1 to task_index when changing the sheet
    since row 1 in the sheet has the headings.
    """
    task_index = validate_index_input("remove")
    confirm = confirm_action("remove", task_index)
    if confirm == "y":
        print(f"Removing task {task_index}...")
        TO_DO_SHEET.delete_rows(task_index + 1)
        print("Task removed successfully\n")

    display_to_do_list()
    edit_list()


print("Welcome back to your To-do List!\n")
user_decision()
