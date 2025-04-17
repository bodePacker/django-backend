# django-backend

https://www.digitalocean.com/github-students For hosting db later

## Getting started

### Docker Setup (Recommended)

```sh
# Step 1: Clone the repository using the project's Git URL
git clone <YOUR_GIT_URL>

# Step 2: Navigate to the project directory
cd django-backend

# Step 3: Build and start the Docker containers
docker-compose up -d

# Step 4: The application will be available at
http://localhost:8000

# Step 5: Access the admin panel at
http://localhost:8000/admin

# Additional commands:
# View logs
docker-compose logs -f

# Stop the containers
docker-compose down

# Create a superuser (if needed)
docker-compose exec web python manage.py createsuperuser
```

### Local Development Setup (Alternative)

```sh
# Step 1: Clone the repository using the project's Git URL
git clone <YOUR_GIT_URL>

# Step 2: Navigate to the project directory
cd django-backend

# Step 3: Create a virtual environment
# Windows
python -m venv venv
# Mac
python3 -m venv venv

# Step 3.5 Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Step 4: Install all the dependencies
pip install -r requirements.txt # or pip3

# Step 5: On initial setup you must create the db locally
# Follow the steps below to setup postgres locally
psql postgres

# Step 5.5: After setting up postgres make a migration to add the django tables to the new Postgres db
python manage.py migrate

# Step 6: Make a superUser to view and login to the admin panel
python manage.py createsuperuser

# Step 7: Make a copy of the test data (optional)
psql -U django_user clickrDatabase < backup.sql

# Step 8: Run the django server
python manage.py runserver

# Step 9: Open the admin panel at
http://127.0.0.1:8000/admin
```

## Database Configuration

When using Docker, PostgreSQL is automatically configured with:

- Database name: clickrDatabase
- Username: django_user
- Password: mypassword

The database is available:

- Inside Docker at hostname `db` port `5432`
- On your host machine at `localhost:5432`
