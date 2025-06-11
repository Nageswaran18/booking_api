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


# API's

# login:

METHOD : [POST]

url : http://127.0.0.1:8000/api/login/

example payload :
{
    "username":"admin",
    "password":"admin"
}

-----------------------------------------------------------------------
# Instructor Register:

METHOD : [POST]

url : http://127.0.0.1:8000/api/register/

example payload (use form data to support profile pic (not manditory)):

{
    "username": "sample",
    "first_name": "sample",
    "last_name": "sample",
    "email": "sample@gmail.com",
    "password": "123",
    "role": "Instructor",
    "date_of_birth": "2003-06-30",
    "phone_number":8786675665,
    "gender":"Female",
    "profile_picture": null,
    "address_line1":"sample",
    "address_line2": "sample" 
}

----------------------------------------------------------------------------------------

# Instructor List

METHOD : [GET]

url : http://127.0.0.1:8000/api/user-list/  - (Authenticated)

----------------------------------------------------------------------------------------

# Fitness Class:

METHOD : [post]

url : http://127.0.0.1:8000/api/fitness-classes/

example payload :

{
  "name": "Zumba",
  "description": "A relaxing yoga session to start your day",
  "start_time": "2025-06-11T06:00:00+05:30",
  "end_time": "2025-06-11T07:00:00+05:30",
  "instructor_id": (user_id),
  "max_capacity": 5,
  "available_slot": 5
}   

-------------------------------------------------------------------------------------------------------------

METHOD : [GET]

url : http://127.0.0.1:8000/api/fitness-classes/?start_date=2025-06-11&end_date=2025-06-11

----------------------------------------------------------------------------------------------------------------

Method : [PUT]

url : http://127.0.0.1:8000/api/fitness-classes/?fitness_id=1

example payload :
{
    "name": "Morning Yoga",
    "start_time": "2025-06-11T08:00:00+05:30",
    "end_time": "2025-06-11T09:00:00+05:30",
}

---------------------------------------------------------------------------------------------------------------

# Booking 

METHOD : [POST]

url : http://127.0.0.1:8000/api/booking/

example payload :
{
    "fitness_class":1,
    "client_name":"sample",
    "client_email":"sample@gmail.com",
    "number_of_slots":2
}

-----------------------------------------------------------------------------------------------------------------

# Booking History

METHOD : [GET]

url : http://127.0.0.1:8000/api/booking-history/?email=sample@gmail.com


----------------------------------------------------------------------------------------------------------------




