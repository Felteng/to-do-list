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


def list_decision():
    """Ask the user which list they wish to see."""
    print(
        "Type: 'tasks' to show to-do List.\n"
        "Type 'history' to show completed tasks.\n"
    )
    user_input = input("Enter your command here:\n").lower()
    print("")
    if user_input == "tasks":
        display_to_do_list()

    elif user_input == "history":
        display_completed_list()

    else:
        print(f"Invalid command.. You entered: '{user_input}'.")
        list_decision()

    edit_list_decision(user_input)


def edit_list_decision(chosen_list):
    """Ask the user if they would like to edit the list they chose to see."""
    while True:
        edit_decision = input(
            "Do you want to edit the list? y/n\n"
        ).lower()
        print("")

        if edit_decision == "y":
            if chosen_list == "tasks":
                edit_to_do_list()

            elif chosen_list == "history":
                edit_completed_list()

        elif edit_decision == "n":
            list_decision()

        else:
            print(f"Did not recognize '{edit_decision}'.")


def display_to_do_list():
    """
    If 'tasks' was chosen in list_decision() then display a table of
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
    If 'history' was chosen in list_decision() then display a table of
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


def edit_to_do_list():
    """Grab input from user as to how they would like to edit the to do list.

    Call the function relevant to the choice.

    If the input does not match options alert user and allow another attempt.
    """
    print("Press enter at any point while editing to go back here.")
    edit_type = input(
                "Type 'edit' to edit a list task\n"
                "Type 'add' to add a task to the list\n"
                "Type 'complete' to complete a task\n"
                "Type 'remove' to remove a task from the list\n"
                "Or type 'none' to stop editing\n"
                ).lower()
    print("")

    if edit_type == "edit":
        edit_task()

    elif edit_type == "add":
        add_task()

    elif edit_type == "complete":
        complete_task()

    elif edit_type == "remove":
        remove_task("To-do")

    elif edit_type == "none":
        list_decision()

    else:
        print(f"Did not recognize '{edit_type}'.")
        edit_to_do_list()


def edit_completed_list():
    """Choices for editing the 'history' list.
    Mainly to undo a task that was accidentally completed.
    """
    print("Press enter at any point while editing to go back here.")
    edit_type = input(
                "Type 'remove' if a task was accidentally completed\n"
                "Or type 'none' to stop editing\n"
                ).lower()
    print("")

    if edit_type == "remove":
        remove_task("Completed")

    elif edit_type == "none":
        list_decision()

    else:
        print(f"Did not recognize '{edit_type}'.")
        edit_completed_list()


def edit_task():
    """Ask the user which row in the list they would like to edit.

    Add 1 to task_index since row 1 in the sheet has the headings.

    Let the user provide new input to update the relevant cells.
    """
    task_index = validate_index_input("edit")
    task_index += 1

    while True:
        cell_to_edit = input("Edit 'task', 'deadline', or 'both'?\n").lower()
        if cell_to_edit == "task":
            new_task = validate_task_input()
            TO_DO_SHEET.update_cell(task_index, 1, new_task)
            print("Task updated successfully\n")
            break

        elif cell_to_edit == "deadline":
            new_deadline = validate_date_input()
            TO_DO_SHEET.update_cell(task_index, 2, new_deadline)
            print("Deadline updated successfully\n")
            break

        elif cell_to_edit == "both":
            new_task = validate_task_input()
            new_deadline = validate_date_input()
            TO_DO_SHEET.update_cell(task_index, 1, new_task)
            TO_DO_SHEET.update_cell(task_index, 2, new_deadline)
            print("Task and deadline updated successfully\n")
            break

        elif cell_to_edit == "":
            edit_to_do_list()

        else:
            print(f"Did not recognize '{cell_to_edit}'.")

    back_to_edit()


def add_task():
    """Ask the user for a task description and task deadline to append
    the new task to the sheet.
    """
    task = validate_task_input()
    deadline = validate_date_input()
    print("Adding task...")
    TO_DO_SHEET.append_row([task, deadline])
    print("Task added successfully\n")
    back_to_edit()


def complete_task():
    """Ask the user which index they would like to complete.

    Get confirmation if the index is correct, if user is not sure,
    return to edit_to_do_list(), if user is sure, proceed with completion.

    Add a value of 1 to task_index when changing a sheet
    since row 1 in the sheet has the headings.

    Add the date this function was carried out to the completed history sheet.

    As for all editing inputs enter an empty string will take the user back.
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

    elif confirm == "n":
        back_to_edit()

    back_to_edit()


def remove_task(worksheet_name):
    """Ask the user which index they would like to remove.

    Target the right worksheet with worksheet_name.

    Get confirmation if the index is correct, if user is sure,
    proceed with removal, if user is not sure return to edit_to_do_list().

    Add a value of 1 to task_index when changing the sheet
    since row 1 in the sheet has the headings.

    As for all editing inputs enter an empty string will take the user back.
    """
    task_index = validate_index_input("remove", worksheet_name)
    confirm = confirm_action("remove", task_index)
    if confirm == "y":
        target_sheet = SHEET.worksheet(worksheet_name)
        print(f"Removing task {task_index}...")
        target_sheet.delete_rows(task_index + 1)
        print("Task removed successfully\n")

    elif confirm == "n":
        back_to_edit(worksheet_name)

    back_to_edit(worksheet_name)


def back_to_edit(*origin_worksheet):
    """Call if user presses enter with no input or with 'n' while editing"""
    print("Going back to edit choices...")
    if origin_worksheet[0] == "Completed":
        display_completed_list()
        edit_completed_list()

    else:
        display_to_do_list()
        edit_to_do_list()


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


def validate_index_input(action, *origin_worksheet):
    """Call this function for any action
    that needs the user to select an index to access.

    Raise ValueError if the index input is smaller than 1
    or if it's not a number.

    As for all editing inputs enter an empty string will take the user back.
    """
    while True:
        try:
            index = input(f"Which index would you like to {action}?\n")

            print("")
            if index == "":
                back_to_edit(origin_worksheet[0])
            elif int(index) < 1:
                raise ValueError

            if origin_worksheet[0] == "Completed":
                index_has_content = (
                    validate_content_presence(int(index), "Completed")
                    )
            else:
                index_has_content = (
                    validate_content_presence(int(index), "To-do")
                    )

            if index_has_content is True:
                return int(index)

        except ValueError:
            print(
                f"'{index}' is not a valid number. "
                "Has to be a number, that is bigger than 0."
            )


def validate_date_input():
    """Call this function whenever user is expected to provide a deadline.
    Checks if the date is in the correct format for consistency.
    Checks if the date is valid in the sense that it has not already passed.

    Parse deadline string into datetime object to compare and test format.
    Get current date and convert it to a string, then parse it back
    into a datetime object with strptime to compare against date_input.

    As for all editing inputs enter an empty string will take the user back.
    """
    while True:
        try:
            deadline = input("Task deadline (yyyy-mm-dd):\n")
            if deadline == "":
                back_to_edit()

            print("")
            date_input = datetime.strptime(deadline, "%Y-%m-%d")
            date_now = str(datetime.now().date())

            if date_input < datetime.strptime(date_now, "%Y-%m-%d"):
                print("That date has already passed")
            else:
                return deadline

        except ValueError:
            print(f"{deadline} does not match format: yyyy-mm-dd")


def validate_task_input():
    """Call this function whenever an input for a task is needed.

    Valdidates the length of the task string to avoid bugs in the table
    and assures ANY input is provided.

    As for all editing inputs enter an empty string will take the user back.
    """
    while True:
        print(
            "If description is longer than 50 characters it will be cut to 50."
        )
        task = input("Task description:\n")
        if task == "":
            back_to_edit()

        if len(task) > 50:
            task = task[:50]
            print("Task description cut down.")
            break
        else:
            break

    print("")
    return task


def validate_content_presence(index, origin_worksheet):
    """Whenever user provides an index this function checks if the index
    has any content. Returns True if yes it does, alert user if it does not.

    Add 1 to index to account for sheet headings.

    Since the user HAS to provide a task and deadline to a task the content
    will be valid if the row is NOT empty.
    """
    target_sheet = SHEET.worksheet(origin_worksheet)
    row_values = target_sheet.row_values(index + 1)
    if row_values == []:
        print(f"Index {index} has no data.\n")

    else:
        return True


def confirm_action(action, task_index):
    """Call this function when confirmation of choice is relevant.

    Asks the user if they're sure about the action on the selected index
    and returns the choice made.
    """
    while True:
        confirm = input(
            f"Are you sure you want to {action} task {task_index}? y/n\n"
        ).lower()
        print("")

        if confirm == "y" or confirm == "yes":
            return "y"

        elif confirm == "n" or confirm == "no" or confirm == "":
            return "n"

        else:
            print(f"Did not recognize '{confirm}'.")


# Thanks to my mentor Rohit Sharma for suggesting this piece of code.
if __name__ == "__main__":
    print("\nWelcome to your To-do List!\n")
    list_decision()
