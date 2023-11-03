# Instructions to Run the Code

1. Clone the repository to your local machine:

```
git clone https://github.com/Shrutika-jain/splitwise.git
cd <project_directory>
```

2. Create a Virtual Environment:

```
 python -m venv venv
 #for windows
 venv\Scripts\activate
```

3. Install Dependencies:

```
pip install -r requirements.txt
```

4. Migrate the model:
   
 ```
python manage.py makemigrations
python manage.py migrate
```

5. Create Superuser
```
python manage.py createsuperuser
```

6. Add the Crontab
```
python manage.py crontab add
```

7. Run the Server
```
python manage.py runserver
 ```

To send the email, add the EMAIL_HOST_USER and EMAIL_HOST_PASSWORD in settings.py file and uncomment the line 32 in api->utils.py to call the send_expense_email function
   
