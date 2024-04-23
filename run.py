import gspread
from google.oauth2.service_account import Credentials
from prettytable import PrettyTable
from pprint import pprint

# Scope and credentials code from Code Institutes Love Sandwiches project

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPEAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPEAD_CLIENT.open("to_do_list")


def get_to_do_list():
    """
    Retrieve the tasks and their respective deadlines from the to_do_list spreadsheet.
    Return them both as 2 seperate lists to allow looping through them sperately to print the table.
    """
    to_do_sheet = SHEET.worksheet("To-do")
    to_do_list = to_do_sheet.col_values(1)
    deadlines = to_do_sheet.col_values(2)
    return to_do_list, deadlines
    

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
        to_do_list, deadlines = get_to_do_list()
        table = PrettyTable(["Item", "Task", "Deadline"])

        index = 1
        for item, deadline in zip(to_do_list[1:], deadlines[1:]):
            table.add_row([index, item, deadline])
            index += 1
        print(table)
        edit_decision = input("Would you like to edit the list? Y/N\n").lower()
        if edit_decision == "y":
            edit_list()
        else:
            user_decision()

    elif user_input == "history":
        print("history")
    
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
    edit_type = input("Type 'edit' to edit a list item\nType 'add' to add an item to the list\nType 'complete' to complete a task\nType 'remove' to remove an item from the list\n").lower()
    if edit_type == "edit":
        edit_task()
    elif edit_type == "add":
        add_task()
    elif edit_type == "complete":
        complete_task()
    elif edit_type == "remove":
        remove_task()
    else:
        print(f"Did not recognize '{edit_type}'. Did you type that correctly?")
        input("Press enter to try again")
        edit_list()


def edit_task():
    """
    Ask the user which row in the list they would like to edit.
    Let the user provide new input to update the relevant cells.
    """
    print("edit")


def add_task():
    """
    Ask the user for a task description and task deadline to append
    the new task to the sheet.
    """
    task = input("Task to be added:\n")
    deadline = input("Task deadline in yyyy-mm-dd:\n")
    to_do_sheet = SHEET.worksheet("To-do")
    to_do_sheet.append_row([task, deadline])
    print("Task added successfully\n")
    edit_list()

def remove_task():
    """
    Ask the user which task they would like to have removed and
    delete that row from the sheet.
    """
    print("remove")


def complete_task():
    """
    Ask the user which task should be completed and append
    that task to the 'Completed' sheet.
    """
    print("complete")


print("Welcome back to your To-do List!\n")
user_decision()
