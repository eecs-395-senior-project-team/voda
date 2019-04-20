# Voda
To run the full stack: `docker-compose -f (local.yml|production.yml) up --build`

Choose either local.yml or production.yml to replicate a local or production environment.

To run the webscraper: `docker-compose -f local.yml run webscraper python scraper.py`