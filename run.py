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
    # Everything below this is subject to get moved into a seperate function
    if user_input == "view":
        to_do_list, deadlines = get_to_do_list()
        table = PrettyTable(["Task", "Deadline"])

        for item, deadline in zip(to_do_list[1:], deadlines[1:]):
            table.add_row([item, deadline])
        print(table)

    elif user_input == "history":
        print("history")
    
    else:
        print(f"Invalid command.. You entered: '{user_input}'\nDid you type the command correctly?")
        input("Press enter to try again\n")
    user_decision()


print("Welcome back to your To-do List!\n")
user_decision()