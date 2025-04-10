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
