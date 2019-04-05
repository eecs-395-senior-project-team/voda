# Voda Backend
Using Python 3.6. Make sure you install [Docker](https://www.docker.com/) and Docker-compose.
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

## Run Tests
`docker-compose -f local.yml run django pytest`

## Style
Enable [Editorconfig](http://editorconfig.org) on your IDE

To run the linter: `flake8`

