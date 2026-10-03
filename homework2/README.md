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
python3 -m pip install -r requirements.txt
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
python3 manage.py test bookings.tests.MovieModelTests -v 2 # Test Count: 4
python3 manage.py test bookings.tests.SeatModelTests -v 2 # Test Count: 4
python3 manage.py test bookings.tests.BookingModelTests -v 2 # Test Count: 7
python3 manage.py test bookings.tests.SeatAvailabilityViewTests -v 2 # Test Count: 2
python3 manage.py test bookings.tests.SeatAPITests -v 2 # Test Count: 4
python3 manage.py test bookings.tests.BookingViewSetTests -v 2 # Test Count: 4

python3 manage.py test bookings -v 2 # Run all bookings app tests
python3 manage.py test -v 2 # Run all project tests
```

### Coverage and Behave Tests
Run these from `homework2/movie_theater_booking` after installing the packages in `homework2/requirements.txt`:

```bash
python3 -m coverage run manage.py test bookings
python3 -m coverage report -m
python3 manage.py behave --simple
```

The coverage report counts the `bookings` app code and leaves out tests and migrations. The Behave scenario checks that a signed-in customer can book a seat and see it in booking history. `--simple` uses Django's test client, so no browser is needed.

## Seat Availability API

GET /api/seats/?movie_id=<movie ID> returns each seat's status for one movie. The is_booked value is calculated from bookings for that movie, so a seat can be booked for one movie and available for another. A missing or invalid movie ID returns 400; an unknown movie returns 404. This endpoint is read-only. Booking creation is a separate implementation step.

## Booking API
The booking API is available at `/api/bookings/` while the development server is running. Sign in through `/accounts/login/` first. Requests from visitors who are not signed in return 403 Forbidden.

- `GET /api/bookings/` lists only the signed-in user's bookings.
- `GET /api/bookings/<id>/` shows one of their bookings; another user's booking returns 404.
- `POST /api/bookings/` creates a booking from movie and seat IDs. For example, send {"movie": 1, "seat": 2} using IDs that exist in your database. The server sets the user and booking date. A seat already booked for that movie is rejected.

To check it visually, run the server on port 3000, sign in on the site, then open `/api/bookings/` in the browser. Django REST Framework shows the GET response and a POST form. An account with no bookings sees an empty list.

## AI Usage Log
Codex GPT-5.6 Terra was utilized to analyze Django content, learn about how Django works a bit beyond the tutorial provided in the course assignment file. As I had trouble with running Django's porting, I moved to local VSCode usage.

Other usage:
- Elaborate understanding on how certain Django functions work for the `bookings` application and file organization for that specific task.
- Learn how to remove certain Django warning messages regarding BigAutoField.
- Helped understand serializers as items that can translate big object database information into things like JSON files to better apply towards DRF. A topic I need to improve on a bit more.

Gemini 3.1 Pro was utilized to better understand Django's native `TestCase` to create better unit and integration testing from the first commits. Rather than waiting till the end, the idea is taking more time to ensure good test-driven development is practiced in this homework to help with the course project later on.

Codex GPT-6.0 Sol helped with improving HTML file conventions to make the site look more visually appealing. Most HTML was made using primarily AI. However, it did help me practice HTML workflows and complexities. Additionally, assisted with the movie-specific seat availability API, removal of the conflicting stored seat status, migration, integration tests, and repository-root key ignore rules. Also helped with understanding for booking serializer, streamlining some testing (although verification is needed for edge cases).

DevEdu Code was used to verify POST handling and seat booking functionality. DevEdu Code was also used to improve test coverage by identifying uncovered lines in `services.py` and `serializers.py`, implementing tests for edge cases including IntegrityError propagation and SeatUnavailable exception handling, and adding Behave acceptance criteria for the "seat already taken" scenario. Feedback was provided on test naming conventions and proper assertion patterns for Django REST Framework serializers.