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

## Running the Scraper

1. Open main.py and examine the line containing the `run` command, which should look something like the following:

   `web_scraper.run(first_website_id=320, last_website_id=350, years=4, force_rescraping=False)`

2. Let's examine what each of these parameters does in greater detail.  
   * `first_website_id`: Represents the website ID of the first school to be scraped. This can be found by examining the URL of any valid AG school course page. For example, if I wanted the first scraped school to be the International Polytechnic High School (the default), I would search for this school on the AG Course List webpage, click on the school listing, and examine the address. In this case, the URL would be https://hs-articulation.ucop.edu/agcourselist/institution/320, so the value of first_website_id would be 320.
   * `last_website_id`: The same as `first_website_id`, except for the last school to be scraped.
   * `years`: The number of past years to scrape information from. For example, if `years` is set to 4, that means the four most recent years of course information will be scraped. Note that the individual years scraped depends on the information available via the AG course list. Let's assume the most recent year is 2020, and a given school does not have any information for the year 2017. If `years` is set to 4, then the scraper will obtain course data from the years 2020, 2019, 2018, and 2016 for that specific school. In summary, `years` will obtain the most recent four years of course information, regardless of the time gaps between such data.
   * `force_rescraping`: Tells the scraper whether or not it should rescrape information that it already has in Salesforce. By setting this parameter to `False`, the scraper will skip over any schools that have been scraped more recently than the page was last updated. When this parameter is set to `True`, it will rescrape all schools it encounters, regardless of whether or not the school has already been scraped recently. It can be useful to set this parameter to `True` if you want to overwrite all data on Salesforce for a given range of schools, perhaps if data was corrupted from an external source or if a clean data refresh is necessary for other reasons.

3. Change the values of parameters that are not to your liking. Given the descriptions of these parameters, it should be straightforward to identify the best values for your needs.

4. Save your changes, then open a Linux terminal with a valid python installation. If necessary, follow steps 4-8 of the previous section in order to run the scraper.

## Pushing to GitHub

1. Make sure your changes are thoroughly tested and fully ready to commit.
2. Ensure that you are still in the proper virtual environment for your development (you should see "env" prepended before your shell), and that you are on the proper branch that you wish to be updated.
3. If you have added any additional dependencies, add them to requirements.txt **manually**, as using `pip freeze` will add all dependencies from the Django project to this requirements.txt file.
4. Change into the directory where you have made changes, and add those changes with `git add .`. If you prefer to add files individually, you can specify the name of each file you modified/created with `git add <name-of-file>`.
5. Commit these changes with `git commit -m "<your-commit-message-here>"`.
6. Push these changes to the corresponding remote branch with `git push`. If this is your first time pushing, use the command `git push --set-upstream origin <remote-branch-name>`.
7. Your changes should be synced! Since the scraper does not rely on Heroku to function, the new build should have succeeded - if not, check the Heroku logs for an explanation.
