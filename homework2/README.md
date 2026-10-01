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
python manage.py runserver 0.0.0.0:3000
```
For DevEdu, it is required to use Port 3000, otherwise it will show a Bad Gateway 502 Error.

## Booking App
The `bookings` application created inside the `movie_theater_booking` project is ran by:
```bash
python manage.py startapp bookings
```
In this section, the command populates files and then `models.py` is defining information on database for movies, seats, and bookings. Instead of copying a movie, Django contains foreign keys and Bookings uses it.

### Creation of Database Tables
Any new changes to bookings, run these commands from the `movie_theater_booking` folder.

```bash
python manage.py makemigrations bookings
python manage.py migrate
python manage.py check
```

## Unit and Integration Testing
https://docs.djangoproject.com/en/6.1/topics/testing/overview/
https://docs.djangoproject.com/en/6.1/intro/tutorial05/

This homework is taking advantage of Django's `TestCase` for unit and integration testing. Within `homework2/movie_theater_booking`:
1. Open an Integrated Terminal.
2. Ensure that `manage.py` file is within this folder.
3. Run Unit/Integration Tests:
   > As an example: 
   `python3 manage.py test bookings.tests.MovieModelTests -v 2`
   > Would run all the unit tests from the Movie Model for the Bookings App. The verbose helps with showing docstrings in the testing for better organization.

### Available Unit Tests
```bash
python3 manage.py test bookings.tests.MovieModelTests -v 2 # Test Count: 6
python3 manage.py test bookings.tests.SeatModelTests -v 2 # Test Count: 5
python3 manage.py test bookings.tests.BookingModelTests -v 2 # Test Count: 5
```

## AI Usage Log
Codex GPT-5.6 Terra was utilized to analyze Django content, learn about how Django works a bit beyond the tutorial provided in the course assignment file. As I had trouble with running Django's porting, I moved to local VSCode usage.

Other usage:
- Elaborate understanding on how certain Django functions work for the `bookings` application and file organization for that specific task.
- Learn how to remove certain Django warning messages regarding BigAutoField.

Gemini 3.1 Pro was utilized to better understand Django's native `TestCase` to create better unit and integration testing from the first commits. Rather than waiting till the end, the idea is taking more time to ensure good test-driven development is practiced in this homework to help with the course project later on.