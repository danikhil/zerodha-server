## Project setup
pip install -r requirements.txt

### Run Serve
python manage.py runserver

### Redis
You have get trial redis to run this server

### Hosting heroku
```
heroku login 
heroku create 
git heroku push master:main
heroku run python manage.py migrate
```

### Environment Variables
In .env files write following variables
```
REDIS_HOST=
SECRET_KEY=
FRONT_END=
REDIS_PASSWORD=
REDIS_USERNAME=
REDIS_PORT=
```

### Web Frontend Reference
https://github.com/danikhil/zerodha-web