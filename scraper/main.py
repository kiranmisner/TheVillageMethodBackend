from scraper_sf import Scraper

if __name__ == "__main__":
  web_scraper = Scraper()
  web_scraper.run(first_website_id=320, last_website_id=350, years=4, force_rescraping=False)