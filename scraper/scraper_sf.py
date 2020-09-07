from scraper_worker_sf import ScraperWorker
import concurrent.futures
import time
import datetime
import os.path
from os import path
from statistics import mean
import sys

class Scraper:
  """ 
  Summary:
      Represents a complete web scraper for the A-G Course List webpage, which can be found at
      https://hs-articulation.ucop.edu/agcourselist. This scraper provides public methods for scraping the most recent
      year of courses from every institution registered with the A-G system, as well as courses for previous years.

  Author:
      Ryan Beckwith

  Organization:
      Tufts Code For Good: The Village Method Project
  """

  def __init__(self):
    """
    Summary:
        Constructor that initializes a Scraper object.

    Fields:
        _fsc (int): A unique 3-4 digit ID used by the A-G course list website to identify institutions. Specifies the
                   school where scraping will begin.
        _lsc (int): A unique 3-4 digit ID used by the A-G course list website to identify institutions. Specifies the
                   school where scraping will end.
        _num_websites (int): Represents the number of websites that will be visited in the process of scraping.
        _years (int): The number of years, starting from the most recent year, from which data should be scraped.
        _force_rescraping (bool): Specifies whether the scraper should rescrape data which has not been recently
                                 updated.
        _run_start_time (float): Stores a float value representing the starting time, in seconds, of the run function.
        _error_output_list (list): Contains all errors that were collected during the execution of the scraper.
        _school_dicts_list (list): Contains all scraped data in the form of dictionaries representing School objects.
        _completed_ids (list): Contains all website IDs for the institutions that have been fully scraped.
        _num_courses_list (list): Contains the number of courses from each school course page visited.
        _invalid_ids_list (list): Contains the website IDs of all pages that were not valid institution pages.
        _school_error_ids_list (list): Contains the website IDs of all pages that experienced an error while creating a
                                      School object.
        _course_error_ids_list (list): Contains the website IDs of all pages that experienced an error while creating a
                                      Course object.
    """
    self._fsc = None
    self._lsc = None
    self._num_websites = None
    self._years = None
    self._force_rescraping = None
    self._run_start_time = None
    self._error_output_list = []
    self._school_dicts_list = []
    self._completed_ids = []
    self._num_courses_list = []
    self._invalid_ids_list = []
    self._school_error_ids_list = []
    self._course_error_ids_list = []

  #####################################################################################################################
  ######################################### PRIVATE GENERAL PURPOSE METHODS ###########################################
  #####################################################################################################################

  def _block_print(self):
    """
    Summary:
        Prevents any code following a call to this function from printing to the terminal.
    """
    sys.stdout = open(os.devnull, 'w')

  def _enable_print(self):
    """
    Summary:
        Enables any code following a call to this function from printing to the terminal.
    """
    sys.stdout = sys.__stdout__

  def _populate(self, list_to_populate, data_list):
    """
    Summary: Populates the list specified by list_to_populate with the elements of data_list

    Args:
        list_to_populate (list): The list to be populated.
        data_list (list): The list containing elements to populate list_to_populate
    """
    for elem in data_list:
      list_to_populate.append(elem)

  def _format_time(self, time_diff):
    """
    Summary:
        Formats a time, specified in seconds, into the form "hours:minutes:seconds.milliseconds".

    Args:
        time_diff (float): The time, in seconds, to be formatted.

    Returns:
        string: The formatted version of time_diff.
    """
    hours, rem = divmod(time_diff, 3600)
    minutes, seconds = divmod(rem, 60)
    return "{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds)

  def _print_progress_bar(self, decimals=1, length=50, fill="█", print_end=""):
    """
    Summary:
        Prints a progress bar to monitor the progress and remaining time of the scraping process.

    Args:
        decimals (int, optional): The number of decimal places to display for the completion percentage. Defaults to 1.
        length (int, optional): The length of the progress bar in characters. Defaults to 50.
        fill (string, optional): The string to fill the progress bar with. Defaults to "█".
        print_end (string, optional): The string to print at the end of the progress bar. Defaults to "".
    """
    # The current iteration, or progress level, is the length of self._completed_ids
    iteration = len(self._completed_ids)
    current_id = "none"
    remaining_time = "unknown"

    # If _completed_ids is not empty, obtain values for current_id and remaining_time
    if self._completed_ids:
      current_id = str(self._completed_ids[-1])
      # Remaining time is the average time to scrape one school times the number of schools left to scrape
      remaining_time = self._format_time((time.time() - self._run_start_time) / float(iteration) * \
        (self._num_websites - iteration))

    # Format the progress bar
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(self._num_websites)))
    filled_length = int(length * iteration // self._num_websites)
    bar = fill * filled_length + '-' * (length - filled_length)

    # Print the progress bar
    print(f'\rProgress: |{bar}| {percent}% Complete, Time Remaining: {remaining_time}, Latest ID: {current_id}', \
      end = print_end, flush=True)

    # Print a newline when the progress bar finishes
    if iteration == self._num_websites: 
      print()

  #####################################################################################################################
  ########################################## PRIVATE FILE CREATION METHODS ############################################
  #####################################################################################################################

  def _create_file_name(self):
    """ 
    Summary:
        Returns a valid filename of the form "month-day-year-ids-fsc-lsc(num).ext", ensuring that no other file with
        the same name exists in the "logs" subdirectory by incrementing the value of num until a new file name is
        guaranteed.

    Returns:
        string: The properly formatted, unique filepath of the specified form.
    """
    here = os.path.dirname(os.path.realpath(__file__))
    subdir = "logs"
    try:
      os.mkdir(os.path.join(here, subdir))
    except Exception:
      pass

    extension = ".txt"
    curr_date = datetime.datetime.now()
    base_filename = curr_date.strftime("%b").lower() + "-" + curr_date.strftime("%d") + "-" \
                    + curr_date.strftime("%Y") + "-ids-" + str(self._fsc) + "-" + str(self._lsc)
    filename = base_filename + extension

    filepath = os.path.join(here, subdir, filename)

    # Ensure that the filename is unique by adding an optional "(num)" to the filename
    i = 1
    while path.exists(filepath):
      filename = base_filename + "(" + str(i) + ")" + extension
      filepath = os.path.join(here, subdir, filename)
      i += 1
    
    return filepath

  def _get_error_list_string(self, error_list):
    """
    Summary:
        Returns a properly formatted representation of a list of error IDs for use in the .txt debug file.

    Args:
        error_list (list): The list of error IDs to format into a string separated by newline characters for
                           readability.

    Returns:
        string: The properly formatted list of error IDs (as a string separated by newline characters).
    """
    # Return "None" if no errors existed
    if not error_list:
      return "None"

    error_list_str = "\n    "
    current_line_str = ""

    # Add each error to the error list string, adding a newline and spaces if the line length exceeds 80
    for error_id in error_list:
      current_line_str += str(error_id) + ", "
      error_list_str += str(error_id) + ", "
      if (len(current_line_str) > 80):
        error_list_str += "\n    "
        current_line_str = ""

    # Find the last instance of a comma and remove it from the string before returning
    return error_list_str[:error_list_str.rfind(",")]

  def _get_avg_num_courses_str(self):
    """
    Summary:
        Returns the average number of courses per website visited, utilizing self._num_courses_list to do so.

    Returns:
        float: The average number of courses per website visited.
    """
    avg_num_courses_string = ""
    avg_num_courses_string += "Average number of courses per school course page: "
    avg_num_courses = None
    if self._num_courses_list:
      avg_num_courses = mean(self._num_courses_list)
      avg_num_courses_string += str(avg_num_courses) + "\n"
    else:
      avg_num_courses_string += "0\n"

    return avg_num_courses_string

  def _get_header_str(self):
    """ 
    Summary:
        Returns the string representation of the .txt debug file's header. This includes the current date, number of
        websites visited, average number of courses per webpage, and various timings for scraping operations.

    Returns:
        string: The string representation of the .txt debug file's header.
    """
    # Get the time it took to run the scraper
    time_to_run_program = time.time() - self._run_start_time
    # Save relevant information into header_str
    header_str = ""
    header_str += "Date: " + datetime.datetime.now().strftime("%x") + "\n"
    header_str += "Time to run scraper: " + self._format_time(time_to_run_program) + "\n"
    header_str += "Websites visited: " + str(self._num_websites) + "\n"
    header_str += "Years scraped: " + str(self._years) + "\n"
    header_str += self._get_avg_num_courses_str()
    time_per_school = time_to_run_program / self._num_websites
    header_str += "Average time to scrape one school course page: " + self._format_time(time_per_school) + "\n"
    header_str += "Estimated time to run scraper fully (~5141 school course pages): " + \
      self._format_time(5141 * time_per_school) + "\n"
    header_str += "\nInvalid website IDs: " + self._get_error_list_string(self._invalid_ids_list) + "\n"
    header_str += "Error website IDs (while creating a School object): " + \
      self._get_error_list_string(self._school_error_ids_list) + "\n"
    header_str += "Error website IDs (while creating a Course object): " + \
      self._get_error_list_string(self._course_error_ids_list) + "\n"
    header_str += "\nError Messages:\n\n" 

    return header_str

  def _format_data_tuples(self, data_tuples):
    """
    Summary:
        Formats the list of data tuples obtained from the ScraperWorker objects into string format.

    Args:
        data_tuples (list): The list of data tuples obtained from the ScraperWorker objects.

    Returns:
        string: The properly formatted data from each data tuple in string format.
    """
    for data_tuple in data_tuples:
      self._populate(self._school_dicts_list, data_tuple[0])
      self._error_output_list.append(data_tuple[1])
      self._populate(self._num_courses_list, data_tuple[2])
      self._populate(self._invalid_ids_list, data_tuple[3])
      self._populate(self._school_error_ids_list, data_tuple[4])
      self._populate(self._course_error_ids_list, data_tuple[5])

    data_string = ""
    data_string += self._get_header_str()
    for error_string in self._error_output_list:
      data_string += error_string + "\n"
    return data_string

  def _write_debug_output(self, data_tuples):
    """
    Summary:
        Writes debug metadata to an output file in the "logs" subdirectory.

    Args:
        data_tuples (list): The list of data tuples obtained from the ScraperWorker objects.
    """
    try:
      f = open(self._create_file_name(), 'w')
      data_string = self._format_data_tuples(data_tuples)
      f.write(data_string)
      f.close()
    except Exception:
      print("An error occurred while attempting to write to the debug output log.")

  #####################################################################################################################
  ############################################ PRIVATE SCRAPING METHODS ###############################################
  #####################################################################################################################

  def _run_scraper_worker(self, website_id, years, force_rescraping):
    """
    Summary:
        Creates a new ScraperWorker instance to obtain data from a specified school, returning that data for later use.

    Args:
        website_id (int): The unique 3-4 digit ID used by the A-G course list website to identify institutions.
        years (int): The number of years, starting from the most recent year, from which data should be scraped.
        force_rescraping (bool): Specifies whether the scraper should rescrape data which has not been recently
                                 updated.

    Returns:
        tuple: A tuple containing all necessary school/course/debug information collected by the ScraperWorker
               instance.
    """
    self._block_print()
    scraper_worker = ScraperWorker()
    data_tuple = scraper_worker.run_page(website_id, years, force_rescraping)
    scraper_worker.close()
    self._completed_ids.append(website_id)
    self._enable_print()
    self._print_progress_bar()
    return data_tuple

  #####################################################################################################################
  ######################################### PUBLIC METHODS FOR USE BY CLIENT ##########################################
  #####################################################################################################################

  def run(self, first_website_id=320, last_website_id=5461, years=4, force_rescraping=False):
    """
    Summary:
        Scrapes the A-G Course List webpage, utilizing parallel processing to increase time efficiency.

    Args:
        fsc (int, optional): A unique 3-4 digit ID used by the A-G course list website to identify institutions.
                             Specifies the school where scraping will begin. Defaults to 320.
        lsc (int, optional): A unique 3-4 digit ID used by the A-G course list website to identify institutions.
                             Specifies the school where scraping will end. Defaults to 5461.
        years (int): The number of years, starting from the most recent year, from which data should be scraped.
        force_rescraping (bool): Specifies whether the scraper should rescrape data which has not been recently
                                 updated.
    """
    # Initialize values of fields
    self._fsc = first_website_id
    self._lsc = last_website_id
    self._run_start_time = time.time()
    self._num_websites = self._lsc - self._fsc + 1
    self._years = years
    self._force_rescraping = force_rescraping

    # Print initial run configuration
    page_str = "pages"
    if self._num_websites == 1:
      page_str = "page"
    year_str = "scraping data from " + str(self._years) + " most recent school years"
    if self._years == 1:
      year_str = "scraping data from most recent school year only"
    print("Running scraper (" + str(self._num_websites) + " school course " + page_str + ", " + year_str + ")...")
    
    # Print the progress bar initially
    self._print_progress_bar()

    # Generate the list of website IDs to visit
    website_ids=list(range(self._fsc, self._lsc + 1))

    # Utilize a ThreadPoolExecutor instance to leverage multithreading while scraping
    with concurrent.futures.ThreadPoolExecutor() as executor:
      # Map the output of self.run_scraper to a Future object
      future = executor.map(lambda website_id: self._run_scraper_worker(website_id, years, force_rescraping),
                            website_ids)
      # When data collection has completed, cast the Future object to a list of tuples containing the scraped data
      data_tuples = list(future)
      # Write the data to a new debug output file
      self._write_debug_output(data_tuples)