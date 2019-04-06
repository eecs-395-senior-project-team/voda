# Voda Webscraper
Using Python 3.6
Using Scrapy

To Run the scraper run:
python scraper.py

## Running the Scraper with Docker
First build the image:
`docker build --tag=vodawebscraper .`

Then run the image:
`docker run vodawebscraper`

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

## Style
Enable [Editorconfig](http://editorconfig.org) on your IDE

To run the linter: `flake8`
