import gspread
import datetime
from google.oauth2.service_account import Credentials
from prettytable import PrettyTable

# SCOPE and credentials code from Code Institutes Love Sandwiches project

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

# Global variables
### Code Institute code ###
CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPEAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPEAD_CLIENT.open("to_do_list")
### Code institute code ends here ###
TO_DO_SHEET = SHEET.worksheet("To-do")

def get_to_do_list():
    """
    Retrieve the tasks and their respective deadlines from the to_do_list spreadsheet.
    Return them both as 2 seperate lists to allow looping through them sperately to print the table.
    """
    tasks = TO_DO_SHEET.col_values(1)
    deadlines = TO_DO_SHEET.col_values(2)
    return tasks, deadlines
    

def get_completed_list():
    """
    Fetch the data from all 3 columns in the completed sheet to allow for iteration
    and display to the user.
    """
    completed_sheet = SHEET.worksheet("Completed")
    tasks = completed_sheet.col_values(1)
    deadlines = completed_sheet.col_values(2)
    time_completed = completed_sheet.col_values(3)
    return tasks, deadlines, time_completed


def user_decision():
    """
    Ask the user what they wish to see from the spreadsheet.
    """
    print("Type: 'view' to show To-do List.\nType 'history' to show completed tasks.\n")
    user_input = input("Enter your command here:\n").lower()
    print("")
    display_decision(user_input)


def display_decision(user_input):
    """
    Display the choice the user made in user_decision() and provide
    new options based on what was chosen and dispalyed.
    If the input in user_decision() was faulty alert the user and allow a new attempt.
    """
    if user_input == "view":
        tasks, deadlines = get_to_do_list()
        table = PrettyTable(["Index", "Task", "Deadline"])

        index = 1
        for task, deadline in zip(tasks[1:], deadlines[1:]):
            table.add_row([index, task, deadline])
            index += 1
        print(table)
        edit_decision = input("Would you like to edit the list? y/n\n").lower()
        if edit_decision == "y":
            edit_list()

        else:
            user_decision()

    elif user_input == "history":
        tasks, deadlines, times = get_completed_list()
        table = PrettyTable(["Index", "Task", "Deadline", "Completed"])

        index = 1
        for task, deadline, time in zip(tasks[1:], deadlines[1:], times[1:]):
            table.add_row([index, task, deadline, time])
            index += 1
        print(table)
        user_decision()
    
    else:
        print(f"Invalid command.. You entered: '{user_input}'\nDid you type the command correctly?")
        input("Press enter to try again\n")
        user_decision()


def edit_list():
    """
    Grab input from user as to how they would like to edit the to do list.
    Call the function relevant to the choice.
    If the input does not match options alert user and allow another attempt.
    """
    edit_type = input("Type 'edit' to edit a list item\nType 'add' to add an item to the list\nType 'complete' to complete a task\nType 'remove' to remove an item from the list\nOr type 'none' to stop editing\n").lower()
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
        print(f"Did not recognize '{edit_type}'. Did you type that correctly?")
        input("Press enter to try again")
        edit_list()
    

def edit_task():
    """
    Ask the user which row in the list they would like to edit.
    Let the user provide new input to update the relevant cells.
    Raise ValueError if the index input is smaller than 1 or if it's not a number.
    """
    try:
        task_to_edit = int(input("Which task index would you like to edit?\n"))
        if task_to_edit < 1:
            raise ValueError
        task_to_edit + 1 # Add a value of 1 here since actual row 1 in the sheet has the headings
    except ValueError:
        print("That is not a valid number. Has to be a number, that is bigger than 0.")
        edit_task()

    cell_to_edit = input("Would you like to edit 'task', 'deadline', or 'both'?\n").lower()
    if cell_to_edit == "task":
        new_task = input("Update task to:\n")
        TO_DO_SHEET.update_cell(task_to_edit, 1, new_task)
        
    elif cell_to_edit == "deadline":
        new_deadline = input("Update deadline (yyyy-mm-dd) to:\n")
        TO_DO_SHEET.update_cell(task_to_edit, 2, new_deadline)

    elif cell_to_edit == "both":
        new_task = input("Update task to:\n")
        new_deadline = input("Update deadline (yyyy-mm-dd) to:\n")
        TO_DO_SHEET.update_cell(task_to_edit, 1, new_task)
        TO_DO_SHEET.update_cell(task_to_edit, 2, new_deadline)

    else:
        print(f"Did not recognize '{cell_to_edit}'. Did you type that correctly?")
        input("Press enter to try again")
        edit_task()
    
    print("Task updated successfully\n")
    edit_list()


def add_task():
    """
    Ask the user for a task description and task deadline to append
    the new task to the sheet.
    """
    task = input("Task to be added:\n")
    deadline = input("Task deadline in yyyy-mm-dd:\n")
    print("Adding task...")
    TO_DO_SHEET.append_row([task, deadline])
    print("Task added successfully\n")
    edit_list()

def complete_task():
    """
    Ask the user which task should be completed and append
    that task to the 'Completed' sheet with the date the
    task was completed added.
    Raise ValueError if the index input is smaller than 1 or if it's not a number.
    """
    try:
        index_to_complete = int(input("Which task (index) would you like to complete?\n"))
        if index_to_complete < 1:
            raise ValueError
    except ValueError:
        print("That is not a valid number. Has to be a number, that is bigger than 0.")
        complete_task()

    def confirm():
        confirm_complete = input(f"Are you sure you want to complete task {index_to_complete}? y/n\n").lower()
        if confirm_complete == "y":
            print(f"Completing task {index_to_complete}...")
            completed_sheet = SHEET.worksheet("Completed")
            today_date = datetime.datetime.now().date()
            to_completed_sheet = TO_DO_SHEET.row_values(index_to_complete + 1) # Add a value of 1 here since actual row 1 in the sheet has the headings
            
            to_completed_sheet.append(str(today_date)) # Add the date this function was carried out to the completed history sheet.
            completed_sheet.append_row(to_completed_sheet)
            TO_DO_SHEET.delete_rows(index_to_complete + 1) # Add a value of 1 here since actual row 1 in the sheet has the headings
            print("Task completed successfully\n")
            edit_list()

        elif confirm_complete == "n":
            edit_list()

        else:
            input(f"Did not recognize {confirm_complete}, did you type 'y' or 'n'?\nPress enter to try again\n")
            confirm()

    confirm() 


def remove_task():
    """
    Ask the user which task they would like to have removed and
    delete that row from the sheet.
    Raise ValueError if the index input is smaller than 1 or if it's not a number.
    """
    try:
        index_to_remove = int(input("Which task (index) would you like to remove?\n"))
        if index_to_remove < 1:
            raise ValueError
    except ValueError:
        print("That is not a valid number. Has to be a number, that is bigger than 0.")
        remove_task()

    def confirm():
        confirm_remove = input(f"Are you sure you want to remove task {index_to_remove}? y/n\n").lower()
        if confirm_remove == "y":
            print(f"Removing task {index_to_remove}...")
            TO_DO_SHEET.delete_rows(index_to_remove + 1) # Add a value of 1 here since actual row 1 in the sheet has the headings
            print("Task removed successfully\n")
            edit_list()

        elif confirm_remove == "n":
            edit_list()

        else:
            input(f"Did not recognize {confirm_remove}, did you type 'y' or 'n'?\nPress enter to try again\n")
            confirm()

    confirm()


print("Welcome back to your To-do List!\n")
user_decision()

