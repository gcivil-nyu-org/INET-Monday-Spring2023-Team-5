# BAM

> From Noisy to Nice - Let BAM Help You Find Your Perfect Neighborhood.

![](https://img.shields.io/badge/python-3.7-blue) ![](https://img.shields.io/badge/code%20style-black-black) ![](https://img.shields.io/badge/linter-flake8-orange)

| Branch | Build | Coverage | Link |
|---|---|---|---|
| `main` | [![Build Status](https://app.travis-ci.com/gcivil-nyu-org/INET-Monday-Spring2023-Team-5.svg?branch=main&kill_cache=1)](https://app.travis-ci.com/gcivil-nyu-org/INET-Monday-Spring2023-Team-5) | <a href='https://coveralls.io/github/gcivil-nyu-org/INET-Monday-Spring2023-Team-5?branch=main'><img src='https://coveralls.io/repos/github/gcivil-nyu-org/INET-Monday-Spring2023-Team-5/badge.svg?branch=main' alt='Coverage Status' /></a> | [bam-nyc](http://bam-nyc.eba-7pq3incs.us-west-2.elasticbeanstalk.com/) |
| `develop` | [![Build Status](https://app.travis-ci.com/gcivil-nyu-org/INET-Monday-Spring2023-Team-5.svg?branch=develop&kill_cache=1)](https://app.travis-ci.com/gcivil-nyu-org/INET-Monday-Spring2023-Team-5) | <a href='https://coveralls.io/github/gcivil-nyu-org/INET-Monday-Spring2023-Team-5?branch=develop'><img src='https://coveralls.io/repos/github/gcivil-nyu-org/INET-Monday-Spring2023-Team-5/badge.svg?branch=develop' alt='Coverage Status' /> | [bam-nyc-dev](http://bam-nyc-dev.eba-humddqy5.us-west-2.elasticbeanstalk.com/) |


BAM (Big Apple Move) is a web-based application that provides comprehensive information and guidance for individuals looking to live in or move to New York City. It offers a personalized experience with features such as centralized location data, interactive forums, and user profiles. BAM offers an interactive map of NYC neighborhoods, complete with information on noise levels, crime statistics, safety, transportation, and more. Whether you're a first-time visitor, student, young professional, family, or retiree, BAM is your ultimate guide to finding the perfect home in the city that never sleeps.


# Setup

## Installation

We use [poetry](https://python-poetry.org/) to setup, manage and install dependencies for the project.

```bash
$ git clone https://github.com/gcivil-nyu-org/INET-Monday-Spring2023-Team-5/
$ cd INET-Monday-Spring2023-Team-5
$ poetry install
$ poetry shell
```

## Setup env variables
```bash
(.venv) $ export DJANGO_SECRET_KEY="$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')"
(.venv) $ export MAPBOX_API_KEY="<your-mapbox-api-key>"
```

## Run the project locally
```bash
(.venv) $ python manage.py makemigrations
(.venv) $ python manage.py migrate
(.venv) $ python manage.py createsuperuser # admin:admin
(.venv) $ python manage.py loaddata fixtures/neighborhood.json
(.venv) $ python manage.py runserver
```

## Run the tests
```bash
(.venv) $ coverage run --source='.' manage.py test
(.venv) $ coverage report
```


# Other
- Deployed using [AWS Elastic Beanstalk](https://aws.amazon.com/elasticbeanstalk/)
- Code formatting using [black](https://black.readthedocs.io/en/stable/)
- Code linting using [flake8](https://flake8.pycqa.org/en/latest/)
- Code coverage using [Coveralls.io](https://coveralls.io/)
- CI/CD using [Travis CI](https://www.travis-ci.com/)
- Maps integration with [Mapbox](https://www.mapbox.com/).

---

# Team 5
1. [Elfarouk Saleh](https://github.com/AlfaroukSaleh)
2. [Chenyu Gu](https://github.com/moringspeaker)
3. [Weiye Sun](https://github.com/ws2309nyu)
4. [Stephanie Hou](https://github.com/StephanieHou)
5. [Venu Vardhan Reddy Tekula](https://github.com/vchrombie)
