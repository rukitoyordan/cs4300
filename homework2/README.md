# Homework #2: Introduction to Django
**Student:** Fabian A. Perez Muñoz  
**Course:** CS4300/5300 002  

---

## Project Structure
```text
homework2/
├── README.md
├── requirements.txt
└── movie_theater_booking/
    ├── manage.py
    ├── bookings/               # Main app containing models, serializers, views, templates, and tests
    ├── features/               # Behave BDD feature files and step definitions
    └── movie_theater_booking/  # Core Django project settings and routing configuration
```

## Local Setup and Execution
From the homework2 directory, create and activate a virtual environment, install the required packages, and start the server:
```bash
python3 -m venv hw2_venv
source hw2_venv/bin/activate
python3 -m pip install -r requirements.txt
cd movie_theater_booking
python manage.py migrate
python manage.py seed_demo
python manage.py runserver 0.0.0.0:3000
```
> Note: For DevEdu environments, port 3000 must be used to prevent a Bad Gateway 502 Error.

## Admin Access:
To test the Django admin panel locally, run python manage.py createsuperuser in your terminal to create your own master credentials, then log in at /admin/.

## Design Decisions
Seat Availability (Spec 3.2): A Seat represents a physical seat in the theater. Therefore, its booking status is determined dynamically by querying the Booking junction table for a specific movie, rather than storing a boolean status directly on the Seat model. This relational design ensures the exact same physical seat (e.g., A1) can be booked independently across different movies without data collisions.

## API Endpoints
### Seat Availability API
> `GET /api/seats/?movie_id=<movie ID>`: Returns each seat's status for a specific movie. The is_booked value is calculated dynamically from active bookings for that movie. A missing or invalid movie ID returns 400 Bad Request; an unknown movie returns 404 Not Found.

### Booking API
The booking API is strictly available to authenticated users. Requests from visitors who are not signed in return `403 Forbidden`. Sign in through `/accounts/login/` first.

> `GET /api/bookings/`: Lists only the signed-in user's bookings.

> `GET /api/bookings/<id>/`: Shows the details of one specific booking. Attempting to view another user's booking returns `404 Not Found`.

> `POST /api/seats/book/` *(or `POST /api/bookings/`)*: Creates a booking from a movie and seat ID. For example, send `{"movie": 1, "seat": 2}`. The server sets the user and booking date. A seat already booked for that movie is rejected.

## Testing (Unit, Integration, and Behave)
This project utilizes Django's native TestCase alongside behave-django for BDD.
Run the automated test suites from the movie_theater_booking directory:
```bash
python manage.py test -v 2          # Run all project unit and integration tests
python -m coverage run manage.py test bookings
python -m coverage report -m        # Generate a test coverage report
python manage.py behave --simple    # Run headless BDD acceptance scenarios
```
> The Behave scenarios verify that a signed-in customer can successfully book a seat, see it in their booking history, and are correctly blocked from booking an already-taken seat.

## Render Deployment
Live URL: https://movie-theater-booking-pytz.onrender.com/

The repository-root `render.yaml` defines a free Python web service and a free PostgreSQL database. Render supplies DATABASE_URL, generates SECRET_KEY, sets DEBUG=False, and uses Python 3.13.5. Startup applies migrations, cleanly updates the demo catalog without destroying subsequent user data, and starts Gunicorn.

## Movie Posters
The sample catalog features classic films like The Matrix, Dune: Part Two, and Interstellar. Poster images load reliably from TMDB at 780-pixel width, with attribution on the movie page. The poster_url field can be edited in the Django admin panel. If a URL is broken or missing, the UI gracefully defaults to an illustrated placeholder using a javascript fallback.

## AI Usage Log
- Codex GPT-5.6 Terra was utilized to analyze Django content, learn about how Django works a bit beyond the tutorial provided in the course assignment file. As I had trouble with running Django's porting, I moved to local VSCode usage.

Other usage:

> Elaborate understanding on how certain Django functions work for the bookings application and file organization for that specific task.

> Learn how to remove certain Django warning messages regarding BigAutoField.

> Helped understand serializers as items that can translate big object database information into things like JSON files to better apply towards DRF. A topic I need to improve on a bit more.

- Gemini 3.1 Pro was utilized to better understand Django's native TestCase to create better unit and integration testing from the first commits. Rather than waiting till the end, the idea is taking more time to ensure good test-driven development is practiced in this homework to help with the course project later on.

- Codex GPT-6.0 Sol helped with improving HTML file conventions to make the site look more visually appealing. Most HTML was made using primarily AI. However, it did help me practice HTML workflows and complexities. Additionally, assisted with the movie-specific seat availability API, removal of the conflicting stored seat status, migration, integration tests, and repository-root key ignore rules. Also helped with understanding for booking serializer, streamlining some testing (although verification is needed for edge cases).

- DevEdu Code was used to verify POST handling and seat booking functionality. DevEdu Code was also used to improve test coverage by identifying uncovered lines in services.py and serializers.py, implementing tests for edge cases including IntegrityError propagation and SeatUnavailable exception handling, and adding Behave acceptance criteria for the "seat already taken" scenario. Feedback was provided on test naming conventions and proper assertion patterns for Django REST Framework serializers.

- Codex GPT-5.6 Terra High was used to review the Render configuration and Homework 2 requirements, draft the environment-based Django settings and root render.yaml, add the demo-data command and admin registration, and update tests for the sign-in redirects. I reviewed the changes and verified them with Django checks, static-file collection, unit tests, Behave scenarios, and Render's Blueprint preview. Codex also helped select the sample films, add poster support and layout, and verify the migration, seed command, and tests.

Final deployment and polishing assistance included:
> Resolving a HOOK-ERROR collision by allowing behave-django to handle test database setups automatically instead of relying on manual setup in features/environment.py.

> Adjusting seed_demo.py to be non-destructive (removing .delete()) so Render's free-tier server restarts wouldn't wipe user data and trigger cascading booking deletions.

> Implementing a Javascript onerror UI fallback to serve a local placeholder (beach-night.png) if a TMDB poster URL breaks, and fixing a TemplateSyntaxError quote collision in the HTML.

> Disabling DRF's default UniqueTogetherValidator to allow custom validation messages to display on duplicate bookings and hit full test coverage.

> Fixing STORAGES dictionary indentation in settings.py.