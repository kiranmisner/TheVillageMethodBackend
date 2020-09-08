# The Village Method Backend 

## Summary

This repository represents the backend framework for [The Village Method](https://thevillagemethod.org/)'s student progress tracker application. Included are public endpoints for accessing school, course, and user information, which are necessary for the frontend of this application.

School and course information is sourced from the [University of California A-G Course List](https://hs-articulation.ucop.edu/agcourselist) via an interactive web scraper (see the scraper folder). The scraper utilizes a Python based Selenium framework and parallel execution to source data from this website, which is uploaded to The Village Method's Salesforce database in real time.

The backend framework itself is located in the backend folder, which utilizes the Django REST framework to create a RESTful API for general CRUD operations. The backend interacts with a Postgresql database, which is used as a middle ground for serializing user information, and The Village Method's Salesforce database for sourcing school and course information. The app itself is hosted through Heroku, and can be found at https://the-village-method-app.herokuapp.com/.

Developed by Tufts undergraduates as a part of the Code for Good initiative during the summer of 2020.

## Getting started with a local development environment 

### Setting up Postgres Locally on a Mac

1. Install [homebrew](https://brew.sh/) if it's not already on your Mac.
2. Update brew with `brew update`.
3. Install postgres with `brew install postgres`.
4. To start postgres consistently run in the background, use the command `brew services start postgresql`. If you'd prefer to start it manually and not have it automatically start use `pg_ctl -D /usr/local/var/postgres start`.
5. Make sure that everything is working properly by entering postgres's command line interface with `psql postgres`. You should see you enter a shell that looks like `postgres=#`.
6. Once in the interface, create a new database named thevillagemethod with the command `CREATE DATABASE thevillagemethod;` If creating the database succeeds, you will see the response `CREATE DATABASE`. This will be the database that our django application will connect and write to for local development. 
7. For anyone to connect and access the database we created, they need a valid postgres username and password combination. This means that we need to create a dedicated user for django app to interact with our new database. We create it with  `CREATE USER thevillagemethod WITH PASSWORD 'thevillagemethod';`.
8. Our new postgres user needs explicit permission to have read and write capabilities on our newly created database. We can do that with the command `GRANT ALL PRIVILEGES ON DATABASE "thevillagemethod" to thevillagemethod;`.  
9. Exit out of postgres with `\q`.

### Setting up Postgres Locally on a Windows PC

1. Install Postgres from https://www.postgresql.org/download/windows/.
2. Open the Setup Wizard and follow the default instructions, entering a password of your choice for the "postgres" superuser.
3. Open a Command Prompt window (or a Linux terminal) and type `psql -U postgres`.
4. Enter the same password you used in the Setup Wizard for the "postgres" superuser.
5. You should see you enter a shell that looks like `postgres=#`.
6. Once in the interface, create a new database named thevillagemethod with the command `CREATE DATABASE thevillagemethod;` If creating the database succeeds, you will see the response `CREATE DATABASE`. This will be the database that our django application will connect and write to for local development.
7. For anyone to connect and access the database we created, they need a valid postgres username and password combination. This means that we need to create a dedicated user for django app to interact with our new database. We create it with  `CREATE USER thevillagemethod WITH PASSWORD 'thevillagemethod';`.
8. Our new postgres user needs explicit permission to have read and write capabilities on our newly created database. We can do that with the command `GRANT ALL PRIVILEGES ON DATABASE "thevillagemethod" to thevillagemethod;`.  
9. Exit out of postgres with `\q`.

### Setting Up The Django Project Locally 
1. Make sure to have python3 installed globally on your development computer, as well as a Git installation.
2. Open a Linux terminal instance (on Windows, you can use the integrated terminal on VSCode or the Bash terminal from your Git installation).
3. Clone the repository with `git clone https://github.com/kiranmisner/TheVillageMethodBackend.git`.
4. Make sure that the virtualenv package is installed globally.
5. Create virtual environment with `virtualenv -p python3 env`.
6. (Mac) Activate the environment with `source env/bin/activate`. Your shell should now be prepended with "env".  
   (Windows) Activate the environment with `source env/Scripts/activate`. Your shell should now be prepended with "env".
7. Install the project dependencies into the virtual environment with `pip install -r requirements.txt`.
8. Set the project settings file with `export DJANGO_SETTINGS_MODULE=thevillagemethod.settings.dev`.
9. Create a superuser with `python manage.py createsuperuser` and follow the prompts.
10. Create any relevant migrations with `python manage.py makemigrations`.
11. Migrate the existing database according to the latest migrations `python manage.py migrate`.
12. Run the project with `python manage.py runserver`.
13. Ensure that the project is running properly by visiting http://127.0.0.1:8000/. You will know that the project is running properly if you see a Page Not Found (404) error.

### Pushing to GitHub and Migrating on Heroku
1. After you have made changes and thoroughly tested them on your local development environment, you are ready to sync the remote repository with your local environment.
2. Ensure that you are still in the proper virtual environment for your development (you should see "env" prepended before your shell), and that you are on the proper branch that you wish to be updated.
3. If you have added any additional dependencies, add them to requirements.txt with the command `pip freeze > requirements.txt`.
4. Change into the directory where you have made changes, and add those changes with `git add .`. If you prefer to add files individually, you can specify the name of each file you modified/created with `git add <name-of-file>`.
5. Commit these changes with `git commit -m "<your-commit-message-here>"`.
6. Push these changes to the corresponding remote branch with `git push`. If this is your first time pushing, use the command `git push --set-upstream origin <remote-branch-name>`.
7. Ensure that these changes were pushed properly by visiting https://github.com/kiranmisner/TheVillageMethodBackend and checking the repository. Again, make sure you are viewing the correct branch while doing so.
8. Ensure that you have a Heroku account linked to the Heroku app for this project. To do so, create an account at https://signup.heroku.com/ and contact Kiran Misner who will add your account as an authorized contributor.
9. Visit https://dashboard.heroku.com/ and log in to your Heroku account. A new build should either be in progress or recently completed, as the Heroku app is set to rebuild itself after every push to the master branch on this repository.
10. Click on the Activity tab and ensure that the latest build succeeded properly. If the build failed, click View Build log to attempt to debug the issue.
11. Once the build has successfully been deployed, click on More > Run Console and run the command `python manage.py makemigrations && python manage.py migrate`. Ensure that the migrations are properly applied.
12. Ensure that the project is running properly by clicking the Open App button and visiting all defined endpoints at https://the-village-method-app.herokuapp.com/


### Further Resources

* [Optimizing Postgres Configuration](https://docs.djangoproject.com/en/2.1/ref/databases/#optimizing-postgresql-s-configuration)
* [The Library that drives the connection between django to postgres](http://initd.org/psycopg/docs/install.html)
* [Good Overview of Relational Database Fundamental Concepts](https://www.postgresql.org/docs/8.4/static/tutorial-concepts.html)
* [How to Create a Data Schema in raw sql](https://www.postgresql.org/docs/8.4/static/tutorial-table.html)
* [How to insert new data in raw sql](https://www.postgresql.org/docs/8.4/static/tutorial-populate.html)
