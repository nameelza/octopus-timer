# OCTOPUS THE TIMER

The project is a timer and to-do list web application, using Javascript, Python, and SQL.

## DEMO PREVIEW
![project demo gif](octopus.gif)

#### VIDEO DEMO:  <https://youtu.be/dGmvlbXrNbQ>

## SETUP
Run these commands to start the project
```
$ ../cd octopus-the-timer-app
$ . venv/bin/activate
$ export FLASK_APP=application.py
$ flask run
```
The app will be available at `http://127.0.0.1:5000/`

## FEATURES

- progress circle timer with the option to pause it and add a heading
- tracking of the finished sessions' duration and name in the account history
- todo list with "complete" and "delete" options

## TECHNOLOGIES USED

- Flask
- SQLite 3

## HOW THE APP WORKS

The idea and design implementation are simple.
I wanted to create an app with a clear design, yet including the most important features like timer, todo table, and history.

As a user with no created account, you can use the web page as a timer for a certain task you can put in the input field above the timer and set the time for a certain duration. The "take a break" and "continue" buttons allow you to pause and resume your timer as well as the progress circle of the timer.

To use more other features like todo table and timer sessions tracker, the user needs to create an account.

As a registered user, you have your timer sessions' name and duration saved in the account history along with the date of the session as soon as you finish your session. There is also an option to create, complete and delete todo tasks on the left sidebar, that can be closed and opened back.

#### Database

SQLite 3 database is used in this application. Database stores all users' info like username and hash password, their to-do list, and timer sessions. The sessions and to-do list tables both use foreign keys to relate users to finished sessions and their tasks in todo table bar.
