# Booking API

A Django REST API for managing fitness classes, user registration, bookings, and booking history.

# Project Structure

1. UserRegisterApi: Register users (Instructor) with profile info and image.
2. UserListApi: List all registered users (admin view).
3. FitnessClassApi: Create, update, and fetch fitness classes with validation and date filters.
4. BookingApi: Book slots in a fitness class, handling slot availability and waitlisting.
5. BookingHistoryApi: Retrieve user-specific booking history with pagination support.

# Installation

1. Clone the repository:
   git clone https://github.com/Nageswaran18/booking_api.git
   cd booking_api

2. Create and activate a virtual environment:
   python -m venv venv

3. Install dependencies:
    pip install -r requirements.txt

4. Apply migrations:
    python manage.py makemigrations
    python manage.py migrate

5. Create a superuser (admin):
    python manage.py createsuperuser

6. Run the development server:
    python manage.py runserver
