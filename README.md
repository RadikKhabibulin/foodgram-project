![foodgram_workflow.yml](https://github.com/radikkhabibulin/foodgram_project/actions/workflows/foodgram_workflow.yml/badge.svg)

# Foodgram

This project is a database of various recipes for cooking dishes.
On this site, you can register, subscribe to authors, add recipes to favorites, download a list of ingredients for a selected list of dishes.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system. This project contains the yamdb_workflow.yml file. This file performs some instructions when push the project to its github directory. To understand these actions go to the website https://docs.github.com/en/actions.

### Prerequisites

To start the project, you need to install Docker. Download this program from the official [website](https://www.docker.com/).

```
Install Docker by following the installation instructions on Windows and macOS.
Installation instructions for Linux: https://docs.docker.com/engine/install/ubuntu/

```

## Deployment

1. Сreate an env file in the root directory of the project and add the following variables to it:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=<postgres_name>
POSTGRES_USER=<postgres_user>
POSTGRES_PASSWORD=<postgres_password>
DB_HOST=db
DB_PORT=<port>
LANG = en_US.utf-8

DEFAULT_FROM_EMAIL = <email server>
EMAIL_HOST = <email host>
EMAIL_PORT = <email port>
EMAIL_HOST_USER = <email user>
EMAIL_HOST_PASSWORD = <email app password>
```

2. Create an image and run the containers with the command:
```
docker-compose up
```

## Create a superuser in database container

1. After deployment find out the container id of the foodgram_web command:
```
docker container ls
```

2. Log in to the container using its ID and perform database migrations:
```
docker exec -it <CONTAINER ID> bash
```
or
```
winpty docker exec -it <CONTAINER ID> bash
```
and
```
python manage.py createsuperuser
```

3. If you need to populate the database with your own data, replace
   the "fixtures.json" file with your own and run the Deployment section.

## Built With

* [Django](https://www.djangoproject.com/) - The web framework used
* [Docker](https://www.docker.com/) - Automatic deployment of the project

## Authors

* **Radik Khabibulin** - *Initial work* - [RadikKhabibulin](https://github.com/RadikKhabibulin)

## Project

View the project - http://217.28.229.197:5003/redoc
