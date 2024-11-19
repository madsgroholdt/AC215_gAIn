### Run Container

Run the startup script which makes building & running the container easy.

- Make sure you are inside the `data_scraping` folder and open a terminal at this location
- Run `sh docker-shell.sh`

### Scrape & Upload Articles

This container is responsible for scraping articles from the web, saving their contents
as `.txt` files, and uploading them to a GCP bucket in the gAIn project.

To run this container, create a secrets folder at the same level as the `src` folder.
This folder should contain:
 - opensecret.json: A JSON file containing the OpenAI API key connected to your account.
 - data-scraping-service.json: The credentials file connected to the gAIn GCP Service account.

To generate a list of URLs, run 'python3 find_urls.py'. This will create a file called
`urls.txt` in the `data_scraping` folder.

To scrape and upload articles, ensure that `find_urls.py` has been run and that a valid
`urls.txt` file exists in the `data_scraping` folder. Then, run 'python3 scrape.py'. The
scraped articles will be saved in the `/raw_articles` folder within the GCP bucket.
