# Financial Analyst (Name pending)
This is a platofrm that is going to be used to do tecnical and fundamental analysis to different stocks. Calculate different ratios, use ML models in order to predict and matematically  

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

Start local server
```
python3 manage.py runserver
```

### Database
Make migrations
```
python3 manage.py migrate
```

Open django shell of the project
```
python3 manage.py shell
```

Or use Graphic Interface by typing:  
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

### Tests
Run tests
```
python3 manage.py test <app_to_test>
```

Tests are located in tests.py file

## Future functionalities
- Machine Learning models to predict stock price
- Better UX/UI dessign (because a back-end engineer designed this)
- Buy/Sell stocks depending on price
- Use this as a daily bassis trading platform
- Support several users
