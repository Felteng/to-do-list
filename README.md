# To-do List
This program functions as a to-do list which the user may manipulate as they see fit. It's stored in an external google sheet so it is mostly limited to personal use as of now.

[Live link](https://felteng-to-do-list-fc4edcc70d21.herokuapp.com/) to the application.

## Table of contents

## The goal

### Goal of the developer
- ***Create a user-friendly experience through simplicity.***
    - Utilize simplicity to provide an easy to understand application despite the users experience level.

- ***Develop functionalities essential to a to-do list.***
    - Identify core functions necessary to manipulate a to-do list, such as adding new tasks and deadlines, updating a task and or deadline, removing redundant tasks, marking tasks as complete, and of course displaying the tasks.

- ***Provide a bug-free user experience.***
    - Implement functions to validate any input the user is expected to make to avoid bugs when displaying the table of tasks. It also helps the user avoid trying to manipulate a task that does not exist. Any wrongful input will also provide feedback to the user.

- ***Make data provided persist through sessions.***
    - Integrate google drive and google sheets through the use of an API to provide a source for the data to be stored, so that the user can maintain the to-do list across different sessions and even devices.

- ***Personal development and application of new skills.***
    - Take advantage of this project as means to learn more about Python, programming libraries, the use of APIs, common programming practices, as well as improving my problem solving skills.

### Goal of the user
- ***Manage and track everyday tasks.***
    - Get a scope of important day to day tasks all in one place to avoid stressful situations where a task or deadline gets lost track of.

- ***Look back through time.***
    - Have the ability to look back in history to see what adn when tasks have been accomplished.

- ***Relish a convenient experience.***
    - Avoid being plagued by bugs and technical difficulties while using the application, and get meaningful feedback when necessary.

## User experience

### User stories

## Features and planning



### Logic planning
![Logic Flowchart](readme-assets/to-do-list-flowchart.png)

### Features

## Technologies used

### Languages
- Python

### Frameworks and libraries
- Google Cloud - Setting up API connections.

- GSpread - Manipulation of the spreadsheet holding the task information.

- PrettyTable - Printing a comprehenisive table to the terminal.

- OAuth2 - Authenticating credentials for API.

- Flake8 - In IDE linter.

- CI Python Linter - External linter for live adjustments.

### Development
- Git - Version control system.

- GitHub - Hosting and storing Git repository.

- Gitpod - IDE for writing all the code.

## Testing

## Deployment
The project was deployed to [Heroku](https://felteng-to-do-list-fc4edcc70d21.herokuapp.com/).

After creating my account at Heroku I took the following steps to ensure successful deployment:

1. At the start page/dashboard click 'New' in the top right part of the page to open a small dropdown.

2. In the dropdown select 'Create new app'.

3. Give the application a unique name and choose a region for deployment. I went with Europe since that's the closest for this applications purposes.

4. Click 'Create app'.

5. Back on the dashboard, select the newly created app.

6. On the app page click 'Settings'.

7. We want to set some Config Vars. Since the application utilizes an API to connect with the google spreadsheet, Heroku needs the credentials from the creds.json file.

8. Create a config var with key 'CREDS' and for the value, paste ALL of the content in the creds.json.

9. The second config var we need to set is key 'PORT' with value '8000'.

10. Now to add 2 neccessary buildpacks, IN THE ORDER SPECIFIED, click add buildpack and choose heroku/python. Then to do the same but choose heroku/nodejs.

Now to prepare the project itself for deployment on Heroku we need to make sure Heroku knows what dependencies to install to run the project.

11. Make sure there's a file called 'requirements.txt' in the root directory.

12. Type 'pip freeze > requirements. txt' in the terminal and you should see some information added to the requirements.txt file.

Make sure to push these changes to your repository before deploying.

13. Back on the app page on Heroku select 'Deploy', choose GitHub as deployment method and connect your account.

14. Search upp the name of the repository for the app to select it.

15. Deploy manually by choosing a branch to deploy from and click 'Deploy Branch'.

16. I also enabled automatic deploys for whenever a push is made to 'main' branch. This is however optional.

## Credits