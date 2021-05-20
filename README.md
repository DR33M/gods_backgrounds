# Gods backgrounds
Gods backgrounds is a photo sharing web application.
The backend is written in Python, using the Django framework.
The frontend is written in Javascript.

## Features
* User Registration
* User Login & Logout
* User Profile
* User Change Password
* Create, Edit & Delete images
* Search
* Moderator-panel
## Installation Instructions
1. Clone the project:
```
  $ git clone https://github.com/DR33M/gods_backgrounds.git
```
2. Set up the Python development environment.
3. Install required dependencies:
```
  $ pip install -r requirements.txt
```
4. Create a PostgreSQL database:
```
  CREATE DATABASE gb;
  CREATE USER gbapp WITH PASSWORD :db_password;
  GRANT ALL PRIVILEGES ON DATABASE gb TO gbapp;
  ALTER ROLE gbapp SET client_encoding TO 'utf8';
  ALTER ROLE gbapp SET default_transaction_isolation TO 'read committed';
  ALTER ROLE gbapp SET timezone TO 'UTC';
  \q
```
5. Run redis.
6. Set up your environment variables ( See .env.example for more details. ):
   - `cd` into the project directory.
   - configure them in a .env file.
7. Apply migrations & Collect static:
```
  python manage.py makemigrations
  python manage.py migrate
  python manage.py collectstatic
```
8. Load fixtures:
```
  python manage.py loaddata color.json
```
9. Create a superuser that can log in to the admin panel:
```
  python manage.py createsuperuser
```
10. Run the local server:
```
  python manage.py runserver
```
And, enjoy it! 🎉
