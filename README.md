## Project setup
pip install -r requirements.txt

### Run Serve
python manage.py runserver

### Redis
You have get trial redis to run this server

### Hosting heroku
heroku login <br />
heroku create <br />
git heroku push master:main <br />
heroku run python manage.py migrate <br />

### Environment Variables
In .env files write following variables <br />
REDIS_HOST= <br />
SECRET_KEY= <br />
FRONT_END= <br />
REDIS_PASSWORD= <br />
REDIS_USERNAME= <br />
REDIS_PORT= <br />

### Web Frontend Reference
https://github.com/danikhil/zerodha-web