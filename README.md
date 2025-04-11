# django-backend

## Getting started

```sh
# Step 1: Clone the repository using the project's Git URL.
git clone <YOUR_GIT_URL>

# Step 2: Navigate to the project directory.
cd django-backend

# Step 3: Create a virtual environment
# Windows
python -m venv venv
# Mac
python3 -m venv venv

# Step 3.5 Active the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Step 4: Install all the listed dependencies within your python env
pip install -r requirements.txt # or pip3

# Step 5: On inital setup you must create the db locally ro when you make changes to the schema
python manage.py migrate

#Step 6: Run the django server
python manage.py runserver

# Step 7: Open the admin panel if there are any users you would like to view and validate any changes you may make at
http://127.0.0.1:8000/admin

# Step 8: To view things in this admin pannel you will likely need to create a SuperUser and follow the steps
python manage.py createsuperuser
```

## Setting up the PostgreSQL database

### Mac

```sh
brew install postgresql@17
brew services start postgresql@17
# If the psql command doesnt show up, run this
echo 'export PATH="/opt/homebrew/opt/postgresql@17/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

#THIS IS TEMP FOR WHILE WE STILL HAVE A DB LOCALLY
# Connect to PostgreSQL as the default postgres user
psql postgres

# Create the database
CREATE DATABASE "clickrDatabase";

# Create the user with password
CREATE USER myuser WITH PASSWORD 'mypassword';

# Grant privileges to the user
GRANT ALL PRIVILEGES ON DATABASE "clickrDatabase" TO myuser;

# Connect to the database
\c clickrDatabase

# Grant schema privileges to the user
GRANT ALL ON SCHEMA public TO myuser;
```

### Windows

1. Go to [Postgres]{https://www.postgresql.org/download/windows/} and download 17.x
2. If an option click "Add PostgreSQL to the PATH" as this makes life much better
3. Follow the above steps to create and connect to the database.

### Linux

According to chatGPT this is a solution for linux but I cant validate it (Ubuntu/Debian).
The rest of the setup steps should be the same as mac

```sh
sudo apt update
sudo apt install postgresql postgresql-contrib
```
