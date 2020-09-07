from scraper_worker_sf import ScraperWorker
import concurrent.futures

class Scraper:
  def __init__(self):


  def run_scraper_worker(self, website_id, years, force_rescraping):
    scraper_worker = ScraperWorker()
    scraper_worker.run_page(website_id, years, force_rescraping)
    scraper_worker.close()

  def run(self, first_website_id=320, last_website_id=5461, years=4, force_rescraping=False):
    website_ids=list(range(first_website_id, last_website_id + 1))
    with concurrent.futures.ThreadPoolExecutor() as executor:
      executor.map(lambda website_id: run_scraper(website_id, years, force_rescraping), website_ids)