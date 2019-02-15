# Voda Backend
Using Python 3.6. Make sure you install [Docker](https://www.docker.com/).
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
- Add a line to requirements/local.txt
- Run: `pip install -r requirements/local.txt`

## Build the stack
`docker-compose -f local.yml build`

## Run the stack
`docker-compose -f local.yml up`

## Style
Enable [Editorconfig](http://editorconfig.org) on your IDE

## Running the server
`python manage.py runserver 8080`

