# GeoMemoir

This is a project for sharing traveling experiences and photos. It was built with Flask as the frontend where Bootstrap 4 was added and Django as the backend. Scrapy was also utilized to extract data.
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
1. __To keep track of the supported languages, a config file **config.py** is created to include the language list:__
```python
class Config(object):
        LANGUAGES = [ 'en', 'zh_Hant_TW', 'zh_Hans_CN']
```

2. __**babel.cfg** is a configuration file created to let pybabel know what files to scan for translation. The following codes is an example for scanning all .py files and html templates.__

```python
[python: app/**.py]
[jinja2: **/templates/**.html]
extensions=jinja2.ext.autoescape, jinja2.ext.with_
```


## How to Run the App

### Use PM2 to run Flask and Django app in daemon
1. __PM2 is a daemon process manager to run the apps online. Follow the commands to install:__
```bash
# Intall nvm
$ curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.2/install.sh | bash
$ nvm install v16.17.0
$ nvm use v16.17.0

# Next install pm2
$ npm install pm2 -g
```

2. __cd to where GeoMemoir directory is located and create scripts **start_f** and **start_d** for Flask and Django app respectively__
```script
# Content in **start_f.sh**
python3 ./GeoMemoir/flask_geo/geo_memoir.py runserver 0.0.0.0:5000

# Content in **start_d.sh**
python3 ./GeoMemoir/geo_memoir/manage.py runserver 0.0.0.0:8000
```

3. __Use PM2 to run the apps__
```bash
$ pm2 start start_f.sh
$ pm2 start start_d.sh

# List all running applications
$ pm2 list
# Monitor the resource usage of the application
$ pm2 monit
```
* PM2 can start any kind of application like bash commands, script, binaries. [Click here](https://pm2.keymetrics.io/docs/usage/process-management/) for more info.

### Run a celery worker in the background
cd to where the manage.py file is located and run the command below:
```bash
$ nohup celery -A geo_memoir worker > celery.log 2>1& &
```


## Reference
1. [Make An Image Gallery With Reflection](https://www.youtube.com/watch?v=8ZAbDfS3GjI)
2. [Tutorial for A Multilingual Web Application](https://medium.com/@nicolas_84494/flask-create-a-multilingual-web-application-with-language-specific-urls-5d994344f5fd)
3. [Bootstrap framework](https://getbootstrap.com/docs/4.6/getting-started/introduction/) used by the web





