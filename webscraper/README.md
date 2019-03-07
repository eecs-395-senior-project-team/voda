# Voda Webscraper
Using Python 3.7.1
Using Scrapy

To Run the scraper run:

> scrapy runspider [pathToSpiderFile]
The spiders must be run in the following order:
- getContaminantsScraper.py
- contaminantInfoScraper.py
- findUtilitiesScraper.py (this one will take a long time)
- utilityInfoScraper.py
 

## Development
To start development run:
`
source env/bin/activate
`
To leave the virtual environment:
`
deactivate
`
To install a new package:
- Add a line to requirements.txt
- Run: `pip install -r requirements.txt`
