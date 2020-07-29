# The Village Method Backend 

## Getting started with a local development environment 

### To Setup up Postgres Locally on a Mac

1. Install [homebrew](https://brew.sh/) if it's not already on your Mac.
2. Update brew with `brew update`.
3. Install postgres with `brew install postgres`.
4. To start postgres consistently run in the background, use the command `brew services start postgresql`. If you'd prefer to start it manually and not have it automatically start use `pg_ctl -D /usr/local/var/postgres start`.
5. Make sure that everything is working properly by entering postgres's command line interface with `psql postgres`. You should see you enter a shell that looks like `postgres=#`.
6. Once in the interface, create a new database named thevillagemethod with the command `CREATE DATABASE thevillagemethod;` If creating the database succeeds, you will see the response `CREATE DATABASE`. This will be the database that our django application will connect and write to for local development. 
7. For anyone to connect and access the database we created, they need a valid postgres username and password combination. This means that we need to create a dedicated user for django app to interact with our new database. We create it with  `CREATE USER thevillagemethod WITH PASSWORD 'thevillagemethod';` 
8. Our new postgres user needs explicit permission to have read and write capabilities on our newly created database. We can do that with the command `GRANT ALL PRIVILEGES ON DATABASE "thevillagemethod" to thevillagemethod;` .  
9. Exit out of postgres 


### Running The Django Project 
1. Make sure to have python3 installed globally on your development computer 
2. Make sure that the virtualenv package installed globally. 
3. Create virtual environment with `virtualenv -p python3 env`
4. Activate the environment with `source env/bin/activate` Your shell should now be pre-pended with "env"
5. Install the project dependencies into the virtual environment with `pip install -r requirements.txt`
6. Set the project settings file with `export DJANGO_SETTINGS_MODULE=thevillagemethod.settings.dev`
7. Create any relevant migrations with `python manage.py makemigrations` 
8. Migrate the existing database according to the latest migrations `python manage.py migrate`
9. Import dummy data with `python manage.py loaddata users.json`

### Further Resources

* [Optimizing Postgres Configuration](https://docs.djangoproject.com/en/2.1/ref/databases/#optimizing-postgresql-s-configuration)
* [The Library that drives the connection between django to postgres](http://initd.org/psycopg/docs/install.html)
* [Good Overview of Relational Database Fundamental Concepts](https://www.postgresql.org/docs/8.4/static/tutorial-concepts.html)
* [How to Create a Data Schema in raw sql](https://www.postgresql.org/docs/8.4/static/tutorial-table.html)
* [How to insert new data in raw sql](https://www.postgresql.org/docs/8.4/static/tutorial-populate.html)


# TheVillageMethodBackend
