# flaskCeleryRedisExample
simple way to perform async tasks

## Instructions
### Install Redis For Windows 10 
Go to this link : https://github.com/microsoftarchive/redis/releases
Download the latest zip version, unzip it and copy the file path and then paste it in windows env variable. Start cmd and run the redis server using the command redis-server

### Install Flask and Celery
using the command pip install flask celery


### Run the app
using the command py app.py
then in a seperate terminal run the command celery -A app.celery worker --loglevel=info
