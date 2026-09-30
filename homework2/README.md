# Homework #2: Introduction to Django
Student: Fabian A. Perez Muñoz
Course: CS4300/5300 002

## Installing Python and Virtual Environment (venv)
```bash
python3 -m venv hw2_venv
source hw2_venv/bin/activate
```

## Required Packages
Install the Django packages required for this assignment.
```bash
python3 -m pip install django djangorestframework
```

## Running the Django Development Server
From the `homework2` directory:
```bash
cd movie_theater_booking
python3 manage.py runserver
```
Then open http://127.0.0.1:8000/ in a browser. 

## Booking App
The `bookings` application created inside the `movie_theater_booking` project is ran by:
```bash
python manage.py startapp bookings
```
In this section, the command populates files and then `models.py` is defining information on database for movies, seats, and bookings. Instead of copying a movie, Django contains foreign keys and Bookings uses it.

### Creation of Database Tables
```bash
python manage.py makemigrations bookings
python manage.py migrate
python manage.py check
```

## AI Usage Log
Codex GPT-5.6 Terra was utilized to analyze Django content, learn about how Django works a bit beyond the tutorial provided in the course assignment file. As I had trouble with running Django's porting, I moved to local VSCode usage.

Other usage:
- Elaborate understanding on how certain Django functions work for the `bookings` application and file organization for that specific task.