# taskcenter
TaskCenter is a task management system where users can create, assign, and track tasks with priority and status.

## Features

- Create Task
- Edit Task
- Assign Task to User
- Role-based access (Assigner/Assignee)
- Status & Priority tracking

## Setup Instructions

1. Clone the repository
git clone <repo-link>

2. Go to project folder
cd taskmanager

3. Create virtual environment
pip install virtualvenv
virtualenv venv

4. Activate environment
.\Scripts\activate

5. Install dependencies
pip install -r requirements.txt

6. Run migrations
python manage.py makemigrations
python manage.py migrate

7. Run server
python manage.py runserver

## Tech Stack

- Backend: Django
- Frontend: HTML, CSS, Bootstrap
- Database: SQLite
- Language: Python

## Sample User Credentials

User 1:
Email: aman@gmail.com
Password: 123

User 2:
Email: mohan@gmail.com
Password: 123


