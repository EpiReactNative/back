# Epigram - back

## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Running the app](#running-the-app)
* [Deployment](#deployment)
* [Documentation](#documentation)
* [Migrations](#migrations)
* [License](#license)
* [Contact](#contact)

## About The Project

Epigram is an Instagram-like allows yout to post, like and share photos!

Api of the [app](https://github.com/EpiReactNative/app) project.

### Built With

* [Django Rest Framework](https://www.django-rest-framework.org/)

## Getting Started

### Prerequisites

* [Python](https://www.python.org/downloads/) ^3.6.9

### Installation

Create virtual environment
```sh
py -m venv env
```

Activate virtual environment
```sh
.\env\Scripts\Activate.ps1 # PowerShell
source env/Scripts/activate # Linux
```

Install required python packages
```sh
pip install -r requirements.txt
```

## Running the app

Run server
```sh
py manage.py runserver
```

## Deployment

This project is link with an [Heroku](https://www.heroku.com) application, pushing to master will trigger an auto-deployment :
* https://epigrambe.herokuapp.com/

## Documentation

The code is documented using a [Swagger](https://swagger.io/) that you can browse at the */swagger* endpoint

## Migrations

Create migrations
```sh
py manage.py makemigrations
```

Apply migrations
```sh
py manage.py migrate
```


## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Project Link: [https://github.com/EpiReactNative/back](https://github.com/EpiReactNative/back)  
Swagger url [http://localhost:8000/api/swagger](http://localhost:8000/api/swagger)
