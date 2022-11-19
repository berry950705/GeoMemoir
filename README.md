# GeoMemoir

This is a project for sharing traveling experiences and photos. It was built with Flask as the frontend and Django as the backend. Scrapy was also utilized to extract data.
The website is being hosted on AWS and Route 53 was set up to route traffic for the domain. Nginx, as a reverse proxy, passes requests to either frontend (port 5000) or backend (port 8000).


## Install packages with pip
cd to the directory where requirements.txt is located and run the command:
```bash
$ pip install -r requirements.txt
```


## Application Structure & Settings
* **flask_geo** file: codes for the frontend, Flask
* **geo_memoir** file: codes for the backend, Django
* **Weather** file: codes for extracting weather data, Scrapy

### Flask 

#### 1. Prefix URLs with the language code - Blueprint
* [Click here](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xv-a-better-application-structure) to get more details about the application structure

#### 2. Translate the web page - Flask-Babel
run the command to install:
```bash
$ pip install flask-babel
```
* [Click here](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xiii-i18n-and-l10n) to get the tutorial for Flask-Babel


### Django

#### 1. Install MySQL and Redis
* [Click here](https://dev.mysql.com/doc/mysql-installation-excerpt/5.7/en/installing.html) for MySQL installation
* [Click here](https://redis.io/docs/getting-started/installation/install-redis-on-linux/) for Redis installation

#### 2. Create the database Django connects with
~~~~MySQL
create database geo_memoir character set UTF8;
~~~~

#### 3. Integrate Celery with Django
run the command to install celery:
```python
$ pip install celery
```


## Configuration File

### Flask 
1. To keep track of the supported languages, a config file **config.py** is created to include the language list:
```python
class Config(object):
        LANGUAGES = [ 'en', 'zh_Hant_TW', 'zh_Hans_CN']
```

2. **babel.cfg** is a configuration file created to let pybabel know what files to scan for translation. The following codes is an example for scanning all .py files and html templates.

```python
[python: app/**.py]
[jinja2: **/templates/**.html]
extensions=jinja2.ext.autoescape, jinja2.ext.with_
```


## How to Run the App

### Use PM2 to run Flask and Django app in daemon
PM2 is a daemon process manager to run the apps online. Follow the commands to install:
```bash
# Intall nvm
$ curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.2/install.sh | bash
$ nvm install v16.17.0
$ nvm use v16.17.0

# Next install pm2
$ npm install pm2 -g

```










## Reference







