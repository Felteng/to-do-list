# To-do List
This program functions as a to-do list which the user may manipulate as they see fit. It's stored in an external google sheet so it is mostly limited to personal use as of now.

[Live link](https://felteng-to-do-list-fc4edcc70d21.herokuapp.com/) to the application.

## Table of contents

## User experience

### User stories

## Features and planning

### The goal
The goal with this project is largely to allow more learning by coding and creating a terminal based application, which can be of use for myself. Furthermore it also provides some grounds to familiarize myself with working with APIs. The source code is also there for anyone who would want to build upon it for their own to-do list application, although I don't suspect there's much appeal to that aspect.

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