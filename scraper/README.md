# The Village Method Backend 

## Summary

This folder represents a complete web scraper for the A-G Course List webpage, which can be found at
https://hs-articulation.ucop.edu/agcourselist. This scraper provides public methods for scraping the most recent
year of courses from every institution registered with the A-G system, as well as courses for previous years.

The scraper utilizes a Python based Selenium framework and parallel execution to source data from this website, 
which is uploaded to The Village Method's Salesforce database in real time.

## Getting started with a local development environment 

1. If you haven't already, follow the steps in the general README file to set up a local development environment.
2. Open a Linux terminal instance (on Windows, you can use the integrated terminal on VSCode or the Bash terminal from your Git installation). 
3. (Mac) Activate your existing virtual environment with `source env/bin/activate`. Your shell should now be prepended with "env".  
   (Windows) Activate your existing virtual environment with `source env/Scripts/activate`. Your shell should now be prepended with "env".
4. Change into the scraper directory with `cd scraper`.
5. Install the project dependencies into the virtual environment with `pip install -r requirements.txt`.
6. Visit https://dashboard.heroku.com/ and log in to your Heroku account. Under the Settings tab, click the Reveal Config Vars button.
7. Run the command `export SF_USERNAME="<insert from Heroku>" && export SF_PASSWORD="<insert from Heroku>" && export SF_TOKEN="<insert from Heroku>"`. Make sure to source the values for each environment variable from the list on Heroku.
8. To run the scraper with the settings already entered in main.py, run the command `python main.py`. If you would like to modify these settings, open main.py and modify the parameters being passed into the `run` method.
9. The scraper should be up and running! Follow the progress in your Linux terminal, and once the scraper has finished, check the newly created log file in the logs subdirectory to view a summary of the scraping process.

## Pushing to GitHub

1. Make sure your changes are thoroughly tested and fully ready to commit.
2. Ensure that you are still in the proper virtual environment for your development (you should see "env" prepended before your shell), and that you are on the proper branch that you wish to be updated.
3. If you have added any additional dependencies, add them to requirements.txt **manually**, as using `pip freeze` will add all dependencies from the Django project to this requirements.txt file.
4. Change into the directory where you have made changes, and add those changes with `git add .`. If you prefer to add files individually, you can specify the name of each file you modified/created with `git add <name-of-file>`.
5. Commit these changes with `git commit -m "<your-commit-message-here>"`.
6. Push these changes to the corresponding remote branch with `git push`. If this is your first time pushing, use the command `git push --set-upstream origin <remote-branch-name>`.
7. Your changes should be synced! Since the scraper does not rely on Heroku to function, the new build should have succeeded - if not, check the Heroku logs for an explanation.