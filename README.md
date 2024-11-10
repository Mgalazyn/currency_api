
# Simple API for currencies' exchange rate 

This is a simple API built with Django REST Framework (DRF) that integrates with the external 'exchangerate-api' service. It stores exchange rates and currency codes in a local database (SQLite).

There is 3 endopoints:

```bash
  /admin/ - to log in into django admin panel after creating super user
  /api/ - with all endpoints for exchange rate
  /api/currency/ - for taking all currencies codes avaliable in the api
  /api/currency/load-initial-date/ - to initialize data into db for selected time (every time we send request then we get currnet rates)
  /api/currency/<from_currency>/<to_currency>/ - in "<>" we can enter ISO codes of currencies to display exchangerate for entered data
```



## Deployment of API

Neccessary for staring with app is getting your API Key for 'exchangerate-api' and adding it into created .env file as 
api_key = 'YOUR-API-KEY'

LINK TO GET API KEY
https://app.exchangerate-api.com/dashboard


1. If you have cloned repository - then redirected to it, have added your .env file with YOUR API KEY, then you have to
create your virtual env by
```bash
  python -m venv "name_of_your_venv"
```

then you should active it, by command (IN WINDOWS)
```bash
  name_of_your_venv\Scripts\activate
```

After that enter command 

```bash
  pip install -r requirements.txt
```

After few moments your needed packaged should be installed into your virutalenv

Now you are almost ready to start using your API,
now just use commands

```bash
  python manage.py runserver
  python manage.py makemigrations
  python manage.py migrate
```
To initialize your models into DB, to get your data and store it locally 

After that your aplication is ready to use, 
Open browser with ip of your localhost
Enter for example: 

http://127.0.0.1:8000/api/currency/load-initial-data/

after few seconds your data should be save locally, then you can use other endpoint with correct output

http://127.0.0.1:8000/api/currency/
http://127.0.0.1:8000/api/currency/EUR/USD/

and other from the list of 
```bash
          initial_pairs = [
            ("EUR", "USD"),
            ("USD", "EUR"),
            ("USD", "JPY"),
            ("JPY", "USD"),
            ("PLN", "USD"),
            ("USD", "PLN"),
        ]
```

if you want check data in admin panel just use command 
python manage.py createsuperuser

fill all fieds and then redirect to endpoint 
/admin/ 
enter used credentials, now you have access to your admin panel for those api

If you want to run test just use command 
```bash
  python manage.py test
```