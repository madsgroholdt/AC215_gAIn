This container is responsible for procuring and preprocessing training materials for
the fine-tuning of the gAIN LLM. These articles cover topics including fitness, health, 
diet, wellness, exercise, and other related fields. 

To run this container, create a secrets folder at the same level as the data-scraping 
folder. This folder should contain:
 - opensecret.json: A JSON file containing the OpenAI API key connected to your account.
 - data-scraping-service.json: The credentials file connected to the gAIn GCP Service account.

To generate a list of URLs, run 'python3 find_urls.py'.

To scrape articles, place URLs in the list contained within scrape.py and run 'python3 scrape.py'.

To upload scraped articles to GCP, run 'python3 send_to_bucket.py'.
