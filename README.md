# Financial Analyst (Name pending)
This is a platform that is going to be used to do technical and fundamental analysis for different stocks. Calculate different ratios, use ML models in order mathematically predict stock prices and buy/sell accordingly

## Setup
### Environment
Create virtual environment
```
python3 -m venv venv
```

Activate virtual environment
```
source venv/bin/activate
```

Run migrations
```
python3 manage.py migrate
```

Start local server
```
python3 manage.py runserver
```

### Database
If models are added or updated, create a new migration with
```
python3 manage.py makemigrations <app_name>
```

Use Graphic Interface to see database information by typing:  
```
python3 manage.py createsuperuser
``` 

Then create username, add email and set a password. It is important to denotate that we should be carefull with this information because in here we are going to create a user that manipulates the database. After completing this step, go to http://127.0.0.1:8000/admin and see the django administrator.
```
Username (leave blank to use 'username'): 
Email address: mail@mail.com
Password: password
Password (again): password
```

Or open Django shell of the project
```
python3 manage.py shell
```

### Tests
Run all tests
```
python3 manage.py test
```

Run tests ofr specific app
```
python3 manage.py test <app_to_test>
```

Tests are located in tests directory

### Code quality 
Run code styler in the whole project
```
black .
```

## Future functionalities (ordered by priority)
1. Machine Learning models to predict stock price
2. Support technical analysis
3. Buy/Sell stocks depending on analysis
4. Use this as a daily bassis trading platform
5. Enhance UX/UI dessign (because a back-end engineer designed this)
6. Support several users
7. Support more languages
