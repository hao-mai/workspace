
## Welcome

The repo is called workspace where different applications will be created to highlight my experience with Django. First project is:

* Create a RESTful API that allows developers to interact with data stored in a database. This app will provide various functionalities and features for devs with data already generated and/or new data to be created for an app called `virtual_library`.

## Swagger file

The `schema/` directory contained the swagger specificiation for our first API; virtual library. It can be used to automatically generate documentation and libraries for the API, it can validate incoming requests and outgoing responses. Developers can access the schema by visiting `/virtual_library/schema` endpoint or by viewing it on the web browser `/virtual_library/docs`
 Here is the expected endpoints:

 ![image](https://user-images.githubusercontent.com/75281072/223545369-e901fb0e-d73b-4a82-a24f-fd2ed1a4d6fd.png)


## Enviroment

### Container

The project is run inside a container to house a development enviroment with all needed dependencies. I have decided to use a docker container because of
- Portability: run the same container on different machines or environments without worrying about differences in the underlying OS or system configuration.
- Isolation: the container runs in its own environment and does not interfere with other applications or services running on the host machine.
- Reproducibility: to define the entire application stack, including the database and other services, and spin up the entire stack.

services:
* The requirements.txt will install all the packages needed.
* DB is MySQL on port 3306

### Setup TBD

* how to clone repo
* how to build the Docker image for project
* how to run it
* how to test it
* how to load system data from fixture

## Pre-commit

Installed from [pre-commit](https://pre-commit.com/).

To install the git hook (which will run only on changed files upon commit):

    pip3 install pre-commit

To manually run hooks only on files you've changed:

    pre-commit

To manually run hooks on the entire project:

    pre-commit run --all-files

Issue that may arises:
* Permission denied: '/home/vscode/.cache/pre-commit' - input `whoami` into the docker terminal, then run `sudo chown -R vscode /home/vscode/.cache`

## Running Tests

I chose [pytest](https://docs.pytest.org/en/6.2.x/getting-started.html) for all tests in my app(s).
For the setup, [pytest-django](https://pytest-django.readthedocs.io/en/latest/)

To run all tests, simply run pytest with no arguments:

    pytest

Issues that may arises:
* django.core.exceptions.ImproperlyConfigured - run in terminal `export DJANGO_SETTINGS_MODULE=virtual_library.settings`
* Got an error creating the test database: (1044, "Access denied for user 'user'@'%' to database 'test_db'") - ensure that you have ran `GRANT ALL PRIVILEGES ON test_db.* TO 'user'@'%';` in mysql

## Model Fixtures

To provide initial data with migrations for virtual_library app. Fixtures can be used to pre-populate database with data for tests or to provide some initial data.
The specific details of each book are completely made up and for illustrative purposes only.
* You can load data by calling `./manage.py loaddata fixtures.yaml`

## Scheduled Tasks

Tasks are scheduled via a cron scheduler and then queued.
* TBD
