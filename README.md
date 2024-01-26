# Netbox Docker Plugin

[![Testing Report](https://github.com/SaaShup/netbox-docker-plugin/actions/workflows/main_ci.yml/badge.svg)](https://github.com/SaaShup/netbox-docker-plugin/actions/workflows/main_ci.yml)

Manage Docker with Netbox & style. Made to work with [netbox-docker-agent](https://github.com/SaaShup/netbox-docker-agent).

![UI Container view with dependencies](/docs/assets/screenshot.png)

## Contribute

### Install our development environment

Requirements:
* Python 3.11
* PostgreSQL 15 [Official Netbox doc](https://github.com/netbox-community/netbox/blob/master/docs/installation/1-postgresql.md)
  - user: netbox (with database creation right)
  - password: secret
  - database: netbox
  - port: 5432
* Redis 7.2
  - port: 6379

Set a PROJECT variable :

```
PROJECT="/project/netbox"
```

Create a project directory `$PROJECT`:

```bash
mkdir $PROJECT
```

Go inside your project directory, clone this repository and the Netbox repository:

```bash
cd $PROJECT
git@github.com:SaaShup/netbox-docker-plugin.git
git clone git@github.com:netbox-community/netbox.git
```

Create your venv and activate it:

```bash
python -m venv venv
source venv/bin/activate
```

Install netbox-docker-plugin dependencies:

```bash
cd $PROJECT/netbox-docker-plugin
pip install -e .
```

Configure Netbox and install Netbox dependencies:

```bash
cd $PROJECT/netbox
cp $PROJECT/netbox-docker-plugin/netbox_configuration/configuration_dev.py $PROJECT/netbox/netbox/netbox/configuration.py
pip install -r requirements.txt
```

Run database migrations:

```bash
cd $PROJECT/netbox
python3 netbox/manage.py migrate
```

Create a Netbox super user:

```bash
cd $PROJECT/netbox
python3 netbox/manage.py createsuperuser
```

Start Netbox instance:

```bash
cd $PROJECT/netbox
python3 netbox/manage.py runserver 0.0.0.0:8000 --insecure
```

Visit http://localhost:8000/

### Run tests

After installing you development environment, you can run the tests plugin (you don't need to start the Netbox instance):

```bash
cd $PROJECT/netbox
python3 netbox/manage.py test netbox_docker_plugin.tests --keepdb -v 2
```

With code coverage, install [coverage.py](https://coverage.readthedocs.io/en/7.3.2/) and use it:

```bash
cd $PROJECT/netbox
python3 -m pip install coverage
```

The run the test with coverage.py and print the report:

```bash
cd $PROJECT/netbox
coverage run --include='*/netbox_docker_plugin/*' netbox/manage.py test netbox_docker_plugin.tests --keepdb -v 2
coverage report -m
```

# Hosting

Check https://saashup.com for more information.
