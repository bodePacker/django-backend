# django-backend

## Getting started

```sh
# Step 1: Clone the repository using the project's Git URL.
git clone <YOUR_GIT_URL>

# Step 2: Navigate to the project directory.
cd django-backend

# Step 3: Create a virtual environment
python -m venv venv

# Step 3.5 Active the virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate

# Step 4: Insatll all the listed dependencies within your python env
pip install -r requirements.txt

#Step 5: Run the django server
python manage.py runserver

# Step 6: Open the admin pannel if there are any users you would like to view to validate any chagnes you may make at
http://127.0.0.1:8000/admin

# Step 6: If any errors are encounteredd with running the server you may need to make a database migration (simple update for your system while we still used a local db)
python manage.py migrate
```
