from school_db import School
from course_db import Course
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from traceback import format_exc
from os import environ
from datetime import datetime
from uuid import NAMESPACE_URL, uuid5
import time

from simple_salesforce import Salesforce
from simple_salesforce.exceptions import SalesforceMalformedRequest

# import requests
import concurrent.futures

class ScraperWorker:
  """ 
  Summary:
      A web scraper worker written with the Selenium/ChromeDriver framework to interactively scrape the A-G Course List
      website by clicking on elements and extracting course/institution information. Designed to be a singular worker
      instance in a parallel processing environment.

  Author:
      Ryan Beckwith

  Organization:
      Tufts Code For Good: The Village Method Project
  """

  #####################################################################################################################
  ################################ PUBLIC METHODS FOR CREATING SCRAPERWORKER OBJECTS ##################################
  #####################################################################################################################

  def __init__(self):
    """ 
    Summary:
        Initializes a ScraperWorker object. This instantiates a new headless Chrome window instance where future
        actions involving scraping will occur.

    Fields:
        driver (WebDriver): The WebDriver object representing the current webpage that is being scraped. Essential to
                            nearly every operation relating to extracting information from a webpage.
        website_address (string): The partially complete address of a listing of the A-G Course List website, requires
                                  a 3-4 digit code to be completed.
        schools (list): A list of School objects that stores all information relevant to a school listing on the A-G
                        Course List website.
        num_courses (list): A list containing the number of courses for each of the school course pages that were
                            scraped.
        invalid_ids (list): Contains the website IDs of all pages that were not valid institution pages.
        school_error_ids (list): Contains the website IDs of all pages that experienced an error while creating a
                                 School object.
        course_error_ids (list): Contains the website IDs of all pages that experienced an error while creating a
                                 Course object.

    """
    # Initializes the webdriver object, installing ChromeDriver if necessary
    self.driver = self.create_driver()

    # Initializes remaining fields
    self.website_address = "https://hs-articulation.ucop.edu/agcourselist/institution/"
    self.schools = []
    self.num_courses = []
    self.invalid_ids = []
    self.school_error_ids = []
    self.course_error_ids = []
    self.error_output = ""
    self.sf = Salesforce(username=environ.get('SF_USERNAME'), password=environ.get('SF_PASSWORD'), 
                         security_token=environ.get('SF_TOKEN'), domain='test')

    # This field is dynamically set in parse_school depending on the website URL
    self.NAMESPACE = None
  
  def create_driver(self, cache_valid_range=7):
    """ 
    Summary:
        Instantiates a headless WebDriver instance, installing the ChromeDriver framework if necessary, which will be
        cached in local storage for a default of 7 days.

    Args:
        cache_valid_range (int, optional): Represents the number of days that the ChromeDriver installation should
                                           remain cached in local storage. Defaults to 7.

    Returns:
        WebDriver: The WebDriver instance to be utilized for scraping.
    """
    # Ensures no excess printing will occur when installing the ChromeDriver framework
    environ['WDM_LOG_LEVEL'] = '0'

    # Initializes proper preferences for a headless browser
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-features=NetworkService")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--disable-features=VizDisplayCompositor")

    return webdriver.Chrome(ChromeDriverManager(cache_valid_range=cache_valid_range).install(), \
      options=chrome_options)

  #####################################################################################################################
  ######################################### PRIVATE GENERAL PURPOSE METHODS ###########################################
  #####################################################################################################################

  def wait(self, search_tactic_specifier, search_tactic=By.XPATH, wait_tactic=EC.presence_of_element_located,
    wait_time=30):
    """ 
    Summary:
        Waits for a page element to be loaded before attempting to access that element, returning the element after it
        is successfully loaded. Throws a TimeoutException if the element does not load in time, or if the element is
        not found.

    Args:
        search_tactic_specifier (string): Specifies the value of some attribute (specified by search_tactic) to find
                                          the desired element. Since search_tactic defaults to By.XPATH, this will
                                          usually be an XPath query.
        search_tactic (string, optional): Specifies the search method utilized to identify the element corresponding
                                          to search_tactic_specifier. Defaults to By.XPATH.
        wait_tactic (function, optional): Function that takes a tuple containing a search_tactic and a
                                          search_tactic_specifier, returning a WebElement object. In general, this
                                          should always be an EC find function, like EC.presence_of_element_located or
                                          EC.element_to_be_clickable. Defaults to EC.presence_of_element_located.
        wait_time (int, optional): Specifies the maximum amount of time, in seconds, that the driver will wait for a
                                   response after any interaction. Defaults to 10.

    Returns:
        WebElement: the element on the page that was searched for and identified.
    """
    return WebDriverWait(self.driver, wait_time, poll_frequency=1).until(wait_tactic((search_tactic, search_tactic_specifier)))

  def load_webpage(self, address, website_id, academic_id=None):
    # Try to load the webpage
    try:
      if academic_id == None:
        # self.error_output += "Trying to load webpage " + address + "\n"
        self.driver.get(address)
      else:
        # self.error_output += "Trying to load webpage " + address + ";academicYearId=" + str(academic_id) + "\n"
        self.driver.get(address + ";academicYearId=" + str(academic_id))
    except Exception:
      error_string = "Could not open school course page properly (ID: " + str(website_id) + ")"
      error_message = format_exc()
      print(error_string)
      print(error_message)
      self.error_output += error_string + "\n" + error_message + "\n"
      return

  #####################################################################################################################
  ################################# PRIVATE METHODS FOR OBTAINING COURSE INFORMATION ##################################
  #####################################################################################################################

  def get_course_divs(self):
    """ 
    Summary:
        Searches the current A-G school course page for all div elements containing course information, returning a
        list containing all such elements.
        Note: Exception handling is not included in this method so that the run function can properly catch
        and handle relevant errors from this function.

    Returns:
        list: A list of WebElement objects containing every div element containing course information. If no such
              WebElement objects are found, this function will return an empty list.
    """
    search_results_div = self.wait("//div[@id='search-results']")
    return search_results_div.find_elements_by_xpath(".//div[@class='grid-row']")

  def get_subject(self, course_div):
    """ 
    Summary:
        Searches course_div for the subject of the course, returning it as a string.

    Args:
        course_div (WebElement): The WebElement object representing a course listing on an A-G school course page
                                 before being clicked on.

    Returns:
        string: The subject of the specified course. If no such subject is found, returns an empty string.
    """
    try:
      # self.error_output += course_div.find_element_by_xpath(".//div[@class='resultsDiscipline']").text + "\n"
      return course_div.find_element_by_xpath(".//div[@class='resultsDiscipline']").text
    except NoSuchElementException:
      # self.error_output += "\nCould not find subject of a course\n"
      return ""

  def get_expanded_course_div(self, course_div):
    """ 
    Summary:
        Searches the current A-G school course page for an expanded course listing. This will be the course div that
        was just clicked on by the create_course method.
        Note: Exception handling is not included in this method so that the create_school function can properly catch
        and handle relevant errors from this function.

    Returns:
        WebElement: The WebElement object representing the expanded course div.
    """
    # Clicks on the course div using JS to avoid width errors
    self.driver.execute_script("arguments[0].click();", \
      course_div.find_element_by_xpath(".//div[@class='resultsCourseTitle']"))
    return self.wait("//div[@class='expand-in show']")

  def get_course_title(self, course_div):
    """ 
    Summary:
        Searches expanded_course_div for the title of the course, returning it as a string.

    Args:
        expanded_course_div (WebElement): The WebElement object created by clicking on a course listing on an A-G
                                          school course page.

    Returns:
        string: The title of the specified course. If no such title is found, returns an empty string.
    """
    try:
      self.wait("//div[@class='resultsCourseTitle']", wait_tactic=EC.element_to_be_clickable)
      title = course_div.find_element_by_xpath(".//div[@class='resultsCourseTitle']").text
      # self.error_output += "\n" + title + "\n"
      return title
    except TimeoutException:
      # self.error_output += "\nCould not find title of a course\n"
      return ""

  def get_is_honors(self, expanded_course_div):
    """ 
    Summary:
        Searches expanded_course_div for the honors status of the course, returning True if the course is an honors
        course, and False otherwise.

    Args:
        expanded_course_div (WebElement): The WebElement object created by clicking on a course listing on an A-G
                                          school course page.

    Returns:
        bool: True if the specified course is an honors course, False otherwise.
    """
    try:
      expanded_course_div.find_element_by_xpath(".//div[@class='honors']")
      return True
    except NoSuchElementException:
      return False

  def get_provider(self, expanded_course_div):
    """ 
    Summary:
        Searches expanded_course_div for the provider of the course, returning it as a string.

    Args:
        expanded_course_div (WebElement): The WebElement object created by clicking on a course listing on an A-G
                                          school course page.

    Returns:
        string: The provider of the specified course. If no such provider is found, returns an empty string.
    """
    try:
      return expanded_course_div.find_element_by_xpath(".//div[@class='font-italic']").text
    except NoSuchElementException:
      return ""

  def get_academic_years(self, expanded_course_div):
    """ 
    Summary:
        Searches expanded_course_div for the academic years for which the specified course was available, returning a
        list of such years stored as strings.

    Args:
        expanded_course_div (WebElement): The WebElement object created by clicking on a course listing on an A-G
                                          school course page.

    Returns:
        list: A list of strings containing each of the years in which the specified course was available. If no such
              years are found, returns an empty list.
    """
    try:
      academic_years_div = expanded_course_div.find_element_by_xpath(".//div[@class='academicYearOffered']")
      spans = academic_years_div.find_elements_by_xpath(".//span")
      valid_spans = []
      for span in spans:
        if not ("notOffered" in span.get_attribute("class")):
          valid_spans.append(span.text)
      return valid_spans
    except NoSuchElementException:
      return []

  def get_grade_levels(self, expanded_course_div):
    """ 
    Summary:
        Searches expanded_course_div for the possible grade levels that can take the specified course, returning a list
        of such grade levels as strings.

    Args:
        expanded_course_div (WebElement): The WebElement object created by clicking on a course listing on an A-G
                                          school course page.

    Returns:
        list: A list of strings containing each of the grade levels that can take the specified course. If no such
              grade levels are found, returns an empty list.
    """
    try:
      grade_levels_div = expanded_course_div.find_element_by_xpath(".//div[@class='gradeLevel']")
      spans = grade_levels_div.find_elements_by_xpath(".//span")
      return [span.text for span in spans]
    except NoSuchElementException:
      return []

  def get_course_length(self, expanded_course_div):
    """ 
    Summary:
        Searches expanded_course_div for the full-year status of the course, returning True if the course is full-year
        and False if the course is half-year.

    Args:
        expanded_course_div (WebElement): The WebElement object created by clicking on a course listing on an A-G
                                          school course page.

    Returns:
        bool: True if the course is full-year, False if the course is half-year.

    """
    try:
      full_year_div = expanded_course_div.find_element_by_xpath(".//div[@class='yearLocationLine muted']")
      spans = full_year_div.find_elements_by_xpath(".//span")
      for span in spans:
        if ("year" in span.text.lower()):
          return span.text.replace(",", "")
      return ""
    except NoSuchElementException:
      return ""

  def get_transcript_abbs(self, expanded_course_div):
    """ 
    Summary:
        Searches expanded_course_div for the possible transcript abbreviations for that course, returning such
        abbreviations as strings in a list.

    Args:
        expanded_course_div (WebElement): The WebElement object created by clicking on a course listing on an A-G
                                          school course page.

    Returns:
        list: A list of strings containing each of the possible transcript abbreviations for the course. If no such
              abbreviations are found, returns an empty list.
    """
    try:
      transcript_div = expanded_course_div.find_element_by_xpath(".//div[@class='transcriptPod']")
      list_elements = transcript_div.find_elements_by_xpath(".//li")
      return [li.text for li in list_elements]
    except NoSuchElementException:
      return []

  def get_ag_designation(self, expanded_course_div):
    """ 
    Summary:
        Searches expanded_course_div for both the subject and the A-G designation of the course, returning both as a
        tuple pair.

    Args:
        expanded_course_div (WebElement): The WebElement object created by clicking on a course listing on an A-G
                                          school course page.

    Returns:
        tuple: A tuple pair containing the subject (a string) as the first element, and the A-G designation (a string)
               as the second element. If either element is not found, a tuple pair of empty strings is returned.
    """
    try:
      subject_line_div = expanded_course_div.find_element_by_xpath(".//div[@class='subjectLine muted']")
      return subject_line_div.find_element_by_xpath(".//span").text
    except NoSuchElementException:
      return ""

  def create_course(self, course_div, subject, course_title, school_uuid):
    """ 
    Summary:
        Creates and returns a Course object by obtaining all relevant data from an A-G school course list page.

    Args:
        course_div (WebElement): The WebElement object containing the relevant course information. This should be a div
                                 that has not been previously clicked on.

    Returns:
        Course: The newly initialized Course object.
    """
    # Gets all relevant course information
    expanded_course_div = self.get_expanded_course_div(course_div)
    is_honors = self.get_is_honors(expanded_course_div)
    provider = self.get_provider(expanded_course_div)
    academic_years = self.get_academic_years(expanded_course_div)
    grade_levels = self.get_grade_levels(expanded_course_div)
    course_length = self.get_course_length(expanded_course_div)
    transcript_abbs = self.get_transcript_abbs(expanded_course_div)
    ag_designation = self.get_ag_designation(expanded_course_div)

    # Clicks on the close button using JS to avoid width errors, and to prevent access to already scraped courses
    self.driver.execute_script("arguments[0].click();", expanded_course_div.find_element_by_xpath(".//a"))

    # return Course(course_title, is_honors, provider, academic_years, grade_levels, course_length, transcript_abbs, \
    #   subject, ag_designation, school_uuid)
    return {
        'Name': course_title,
        'High_School__c': school_uuid, 
        'Academic_Years__c': ";".join(academic_years),
        'Is_Honors__c': is_honors,
        'Provider__c': provider,
        'Grade_Levels__c': ";".join(grade_levels),
        'Course_Length__c': course_length,
        'Transcript_Abbs__c': ";".join(transcript_abbs),
        'Subject__c': subject,
        'AG_Designation__c': ag_designation
    }

  def is_in_courses(self, courses, course_title):
    for course in courses:
      if course['Name'] == course_title:
        # self.error_output += "\n" + course.name + " and " + course_title + " matched.\n"
        return True
    return False

  def recently_scraped(self, school_id, address, academic_id, last_updated_sf, force_rescraping):
    # print('Beginning to check for recent scraping')
    if not force_rescraping:
      last_updated = self.get_last_updated()
      # print(last_updated)
      # if not last_updated:
      #   print(f"Could not find the date when this page (Address: {address}, Academic ID: {academic_id}) was loaded")
      # else:
      #   print(f"This page (Address: {address}, Academic ID: {academic_id}) was last updated on {last_updated}")
      
      # last_modified_sf = self.get_last_modified_date(school_id)
      # if not last_modified_sf:
      #   print(f"Could not find the date of last modification for school with external ID {school_id} from Salesforce.")
      # else:
      #   print(f"School with external ID {school_id} was last modified on {last_modified_sf}")

      if last_updated and last_updated_sf and last_updated_sf >= last_updated:
        print("This school was already scraped recently: Last updated on", str(last_updated).partition(" ")[0],
          "versus last modified on Salesforce on", str(last_updated_sf).partition(" ")[0])
        return True
    return False


  def parse_courses(self, school_id, website_id, years, school_uuid, last_updated_sf, force_rescraping):
    # Create the list of courses
    courses = []
    # TODO: Loop through the desired years of course pages
    academic_year_ids = self.get_academic_year_ids(website_id, years)
    # self.error_output += "Academic year IDs: " + str(academic_year_ids) + "\n"
    # year_counter = 0
    for academic_id in academic_year_ids:
      # year_counter += 1
      # print(f"Beginning to scrape school {website_id} with academic ID {academic_id} for courses")
      self.load_webpage(self.website_address + str(website_id), website_id, academic_id=academic_id)
      # print("About to check for recent scraping")
      if not self.recently_scraped(school_id, self.website_address + str(website_id), academic_id, last_updated_sf, force_rescraping):
        for course_div in self.get_course_divs():
          # print(course_div.text)
          course_title = self.get_course_title(course_div)
          course_subject = self.get_subject(course_div)
          try:
            if not self.is_in_courses(courses, course_title):
              # print("Creating new course with title", course_title)
              courses.append(self.create_course(course_div, course_subject, course_title, school_uuid))
            # else:
            #   # print("Duplicate found:", course_title)
          except Exception:
            error_string = "There was an error creating a course (ID: " + str(website_id) + "):"
            error_message = format_exc()
            print(error_string)
            print(error_message)
            self.error_output += error_string + "\n" + error_message + "\n"
            if not website_id in self.course_error_ids:
              self.course_error_ids.append(website_id)
            continue
      # print(f"Length of courses at the end of ID {academic_id}: {len(courses)}")
    
    # print(courses)
    return courses
  
  #####################################################################################################################
  ################################# PRIVATE METHODS FOR OBTAINING SCHOOL INFORMATION ##################################
  #####################################################################################################################

  def get_school_name(self):
    """ 
    Summary:
        Searches the school course page for the name of the current institution.

    Returns:
        string: The name of the current institution. If no such name exists, returns an empty string.
    """
    try:
      return self.driver.find_element_by_xpath("//h5[@class='instName']").text
    except NoSuchElementException:
      return ""

  def get_institution_type(self):
    """ 
    Summary:
        Searches the school course page for the type of the current institution.
        Note: Since this method is used to check for the validity of a school course page, it uniquely uses the wait
        method, which introduces a delay for this function.

    Returns:
        string: The type of the current institution. If no such type is found, returns an empty string.
    """
    try:
      return self.wait("//span[@class='instGovBadge']", wait_time=12).text
    except TimeoutException:
      return ""

  def get_school_id(self):
    """ 
    Summary:
        Searches the school course page for the unique ID of the current institution.

    Returns:
        string: The unique ID of the current institution. If no such unique ID is found, returns an empty string.
    """
    try:
      return self.driver.find_element_by_xpath("//span[@class='instATPcodeBadge']").text
    except NoSuchElementException:
      return ""

  def get_city(self, location):
    """ 
    Summary:
        Searches the given location for the city where the current institution is located.

    Args:
        location (string): A string containing a comma separated location of the form "city, state".

    Returns:
        string: The city where the current institution is located. If no such city is found, returns an empty string.
    """
    try:
      return location.split(", ")[0]
    except IndexError:
      return ""
  
  def get_state(self, location):
    """ 
    Summary:
        Searches the given location for the state where the current institution is located.

    Args:
        location (string): A string containing a comma separated location of the form "city, state".

    Returns:
        string: The state where the current institution is located. If no such state is found, returns an empty string.
    """
    try:
      return location.split(", ")[1]
    except IndexError:
      return ""
  
  def get_location(self):
    """ 
    Summary:
        Searches the school course page for the location (city and state) where the current institution is located.

    Returns:
        string: Returns a string containing both the city and state of the current school in the comma separated form
                "city, state". If no such location is found, returns an empty string.
    """
    try:
      sub_inst_info_div = self.driver.find_element_by_xpath("//div[@class='subInstInfo']")
      return sub_inst_info_div.find_element_by_xpath(".//div[@class='font-italic']").text
    except NoSuchElementException:
      return ""

  def get_location_tuple(self):
    """ 
    Summary:
        Searches the school course page for its location, returning it as a tuple pair of the form (city, state).

    Returns:
        tuple: A tuple pair of the form (city, state) representing the location of the current institution.
    """
    location = self.get_location()
    return (self.get_city(location), self.get_state(location))

  def get_last_updated(self):
    try:
      # last_updated_div = self.wait("//div[@class='listLastUpdated']")
      last_updated_div = self.wait("//div[@class='listLastUpdated']")
      last_updated_div = self.driver.find_element_by_xpath("//div[@class='listLastUpdated']")
      # time.sleep(0)
      # print("Text of last_updated_div:", last_updated_div.text)
      date_string = last_updated_div.text.partition(': ')[2]
      if date_string:
      # print("Date string from website:", date_string)
        return datetime.strptime(date_string, '%b %d, %Y')
      else:
        return None
    # except Exception:
    #   print(format_exc())
    except TimeoutException:
      print("Timeout exception occurred when trying to find last updated")
      return None

  def create_school(self, website_id, institution_type, years, school_id, force_rescraping):
    """ 
    Summary:
        Creates and returns a School object for the current school course page.

    Args:
        website_id (int): The unique 3-4 digit ID used by the A-G course list website to identify institutions.
        institution_type (string): The type of the current institution, usually specified by the get_institution_type
                                   method.

    Returns:
        School: The newly initialized School object.
    """
    # Gets all necessary information to create the School object (except institution type, which is passed)
    school_name = self.get_school_name()
    # school_id = self.get_school_id()
    city, state = self.get_location_tuple()
    
    # s = School(school_name, institution_type, school_id, city, state, website_id)
    s = {
        'Name': school_name,
        'Website_ID__c': website_id,
        'City__c': city,
        'State__c': state,
        'Institution_Type__c': institution_type
    }
    # Check to see if the school needs to be scraped
    last_updated_sf = self.get_last_updated_sf(school_id)
    # Create or update school on Salesforce database
    if not self.upsert_school(school_id, s):
      return

    courses_to_add = self.parse_courses(school_id, website_id, years, self.get_sf_high_school_id(school_id), last_updated_sf, force_rescraping)
    # print(courses_to_add)
    for course in courses_to_add:
      # print(course)
      # try:
      # external_id = course['Name'] + '-' + school_id
      external_id = self.get_uuid_of_course(course['Name'])
      self.upsert_sf_course(external_id, course)
      # print("Course upserted.")
      # except SalesforceMalformedRequest:
      #   error_string = "A malformed request was made to the Salesforce database while creating a Course object:"
      #   error_message = traceback.format_exc()
      #   print(error_message)
      #   self.error_output += error_string + "\n" + error_message + "\n"
      #   continue


    # Appends the length of the courses list to num_courses to keep track of the average number of courses
    self.num_courses.append(len(courses_to_add))
    return s
    
  def parse_school(self, address, website_id, years, force_rescraping):
    """
    Summary:
        Parses the school course page specified by address by first loading the webpage, ensuring the webpage is valid,
        then scraping the relevant data.

    Args:
        address (string): A string containing the full address of the school course page.
        website_id (int): The unique 3-4 digit ID used by the A-G course list website to identify institutions. In this
                          function, website_id must exactly match the final 3-4 digits at the end of address.
    """
    # Save the namespace for this website, which is a hash linked to the address of the webpage
    self.NAMESPACE = uuid5(NAMESPACE_URL, address)
    # Try to load the webpage
    self.load_webpage(address, website_id)
    
    # Ensure that the webpage is valid by checking to see if it has a valid institution type
    inst_type = self.get_institution_type()
    if inst_type == "":
      # self.error_output += "\nInvalid course with ID" + str(website_id) + "\n"
      self.invalid_ids.append(website_id)
      return

    # Get the school ID
    school_id = self.get_school_id()
    # Check to see if the modification date on the A-G page is later than the last modified date for the school
    # if not force_rescraping:
    #   last_updated = self.get_last_updated()
    #   if not last_updated:
    #     print(f"Could not find the date when this page (Website ID: {website_id}) was loaded")
    #   else:
    #     print(f"Page with website ID {website_id} was last updated on {last_updated}")
      
    #   last_modified_sf = self.get_last_modified_date(school_id)
    #   if not last_modified_sf:
    #     print(f"Could not find the date of last modification for school with external ID {school_id} from Salesforce.")
    #   else:
    #     print(f"School with external ID {school_id} was last modified on {last_modified_sf}")

    #   if last_updated and last_modified_sf and last_modified_sf >= last_updated:
    #     print("This school was already scraped recently: Last updated on", last_updated, "versus last modified on Salesforce on", last_modified_sf)
    #     return
    # Begin to scrape the current school course page
    self.schools.append(self.create_school(website_id, inst_type, years, school_id, force_rescraping))

  def get_property_from_query(self, prop, query):
    return query['records'][0][prop]

  def upsert_school(self, school_id, data):
    # print('before')
    if not school_id:
      print("School ID was not found, aborting upsert.")
      return False
    self.sf.HighSchool__c.upsert(f'School_ID__c/{school_id}', data)
    return True
    # print(code)

  def get_sf_high_school_id(self, school_id):
    query = self.sf.query(f"SELECT Id FROM HighSchool__c WHERE School_ID__c = '{school_id}'")
    return self.get_property_from_query('Id', query)

  def create_sf_course(self, data):
    self.sf.Course__c.create(data)

  def upsert_sf_course(self, external_id, data):
    # print("Beginning upsert")
    try:
      # print(getattr(self.sf, "Course__c").describe())
      code = getattr(self.sf, "Course__c").upsert(f'External_ID__c/{external_id}', data)
      # code = self.sf.Course__c.upsert(f'External_ID__c/{external_id}', data)
      # print(f"Status code for upserting course {data['Name']} ({external_id}): {code}")
    except Exception:
      print("Some exception occurred while upserting")
      print(format_exc())

  def get_last_updated_sf(self, school_id):
    try:
      # school_id = "abcdef"
      query = self.sf.query(f"SELECT LastModifiedDate FROM HighSchool__c WHERE School_ID__c = '{school_id}'")
      # sf_id = self.get_sf_high_school_id(school_id)
      # query = self.sf.query(f"SELECT Last_Updated_Formula__c FROM HighSchool__c WHERE School_ID__c = '{school_id}'")
      # print(query)
      if query['records']:
        lmd_string = query['records'][0]['LastModifiedDate']
        # print("Last modified date:", lmd_string)
        date_string_dashes = lmd_string.partition('T')[0]
        # print("Salesforce date:", date_string_dashes)
        return datetime.strptime(date_string_dashes, '%Y-%m-%d')
      else:
        return None
    except Exception:
      print(format_exc())
      return None

  # def get_hex_of_course_name(self, course_name):
  #   hex_string = "0x"
  #   for char in course_name:
  #     hex_string += hex(ord(char)).partition("0x")[2]
  #   print(hex_string)
  #   return hex_string

  def get_uuid_of_course(self, course_name):
    return str(uuid5(self.NAMESPACE, course_name))

  #####################################################################################################################
  ################################## PRIVATE METHODS FOR OBTAINING YEAR INFORMATION ###################################
  #####################################################################################################################

  def get_buttons_div(self):
    try:
      return self.wait("//div[@class='gridButtonMain']")
    except TimeoutException:
      error_string = "There was an error accessing the buttons div:"
      error_message = format_exc()
      self.error_output += error_string + "\n" + error_message + "\n"
      return None

  def get_active_button(self):
    try:
      buttons_div = self.get_buttons_div()
      if buttons_div:
        buttons_list = buttons_div.find_elements_by_xpath(".//button")
        for button in buttons_list:
          if "btnActive" in button.get_attribute("class").split(" "):
            return button
        # self.error_output += "Last button text: " + buttons_list[len(buttons_list) - 1].text + "\n"
        if buttons_list:
          return buttons_list[len(buttons_list) - 1]
        else:
          return None
      else:
        return None
    except NoSuchElementException:
      error_string = "There was an error accessing the active button:"
      error_message = format_exc()
      self.error_output += error_string + "\n" + error_message + "\n"
      return None

  def get_valid_academic_year_ids(self, website_id, years, first_academic_id, first_active_button_text):
    if years < 1:
      return []
    # Include first year as a special case
    valid_academic_ids = [first_academic_id]
    # Loop through the possible academic IDs
    for i in range(first_academic_id - 1, first_academic_id - years, -1):
      # Ensure each ID is valid by comparing the active button text with the text for the active button when the first
      # academic ID was used (except the first time). If it matches, but the academic ID differs from the first ID, the
      # year is invalid. Otherwise, the year can be scraped (although the course list may be empty still).
      self.load_webpage(self.website_address + str(website_id), website_id, academic_id=i)
      active_button = self.get_active_button()
      if active_button and (not active_button.text == first_active_button_text):
        valid_academic_ids.append(i)
    
    return valid_academic_ids

  def get_academic_year_ids(self, website_id, years):
    # Find button for current academic year
    first_active_button = self.get_active_button()
    # Click on button for current academic year
    if first_active_button:
      self.driver.execute_script("arguments[0].click();", first_active_button)
    else:
      self.error_output += "\nFirst active button was not found properly (ID " + str(website_id) + ")\n"
      return []

    # Extract academic ID from link and save, get range of academic IDs based on the value of years
    wait = WebDriverWait(self.driver, 12)
    wait.until(lambda driver: "academicYearId" in driver.current_url)
    # wait.until(EC.title_contains("academicYearId"))
    first_academic_id = int(self.driver.current_url[self.driver.current_url.rfind("=") + 1:])
    
    # Return the list of academic IDs, which are ensured to be scrapeable, as self.get_course_divs() will handle the
    # empty course list case
    return self.get_valid_academic_year_ids(website_id, years, first_academic_id, first_active_button.text)

  # TODO: Skip page if last update was before second most recent run

  #####################################################################################################################
  ####################################### PUBLIC METHODS FOR USE BY THE CLIENT ########################################
  #####################################################################################################################

  def run_page(self, website_id, years, force_rescraping):
    """ 
    Summary:
        Scrapes the school course page with the specified ID, returning a tuple containing each of the relevant data
        fields for use by the client.

    Args:
        website_id (int): The unique 3-4 digit ID used by the A-G course list website to identify institutions.

    Returns:
        tuple: A tuple containing each of the relevant data fields for client use. Follows the format specified below:
               (schools, error_output, num_courses, invalid_ids, school_error_ids, course_error_ids).
               Reference the constructor for descriptions of each field.
    """
    try:
      self.parse_school(self.website_address + str(website_id), website_id, years, force_rescraping)
    #   return (self.schools, self.error_output, self.num_courses, self.invalid_ids, self.school_error_ids, \
    #     self.course_error_ids)
    except Exception:
      error_string = "An error occurred while scraping school with ID " + str(website_id) + "."
      error_message = format_exc()
      print(error_string)
      print(error_message)
      self.error_output += error_string + "\n" + error_message + "\n"
      self.school_error_ids.append(website_id)
    #   return (self.schools, self.error_output, self.num_courses, self.invalid_ids, self.school_error_ids, \
    #     self.course_error_ids)

  def close(self):
    """ 
    Summary:
        Closes the WebDriver instance associated with a ScraperWorker instance. This function should always be called
        directly after the ScraperWorker instance has completed its scraping objective.
    """
    self.driver.close()

def run_scraper(website_id, years, force_rescraping=False):
  scraper_worker = ScraperWorker()
  scraper_worker.run_page(website_id, years, force_rescraping)
  scraper_worker.close()

if __name__ == "__main__":
  # sw = ScraperWorker()
  # school_id = "052508"
  # print(sw.get_last_updated_sf(school_id))

  years = 4
  website_ids = list(range(320, 500))
  force_rescraping = False
  with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(lambda website_id: run_scraper(website_id, years, force_rescraping), website_ids)