# Virtual Internship and Volunteer Platform (VIVP)

## Overview
The Virtual Internship and Volunteer Platform (VIVP) is designed to connect interns and volunteers with opportunities globally. It enables organizations to post internships and volunteer work, while students and other applicants can apply and submit tasks online. The platform facilitates the assignment of university supervisors to students, allowing for performance tracking and feedback.

## Features
- **Internship/Volunteer Posting**: Organizations can post opportunities with detailed tasks.
- **Application System**: Applicants can apply and, once accepted, submit their tasks.
- **Performance Evaluation**: System coordinators and organizations can evaluate interns' performance.
- **Certificate Generation**: System coordinators can generate certificates for successful interns.
- **User Management**: Admins have full control over users and posts.
- **University Integration**: University coordinators can approve students and assign supervisors.

## Technologies
- **Backend**: Django REST Framework
- **Database**: [sqlite, Postgres]

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites
What things you need to install the software and how to install them:
Python 3.6 or higher

### Installing
A step by step series of examples that tell you how to get a development environment running:

- Clone this repository: `git clone https://github.com/Dawit-y/vivp.git`
- Create a virtual environment: `python -m venv venv`
- Activate the virtual environment: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
- Install the requirements: `pip install -r requirements.txt`
- Run the migrations: `python manage.py migrate`
- Create a superuser: `python manage.py createsuperuser`
- Run the server: `python manage.py runserver`

