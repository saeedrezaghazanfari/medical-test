### Create VirtualEnv
```
python -m venv venv
```

### Activate VirtualEnv
```
.\venv\Scripts\activate
```

### Install Requirements
```
pip install -r requirements.txt
```

### Run Server
```
python manage.py runserver 8000
```



### api usage:

send username and password as a json to http://127.0.0.1:8000/en/api/v1/get-token/
this request must be POST method.

{
    "username": "1111111111",
    "password": peaka
}

you have two token: refresh token and access token
for request to any urls, you must have access token.
you can update the "access token" with "refresh token" 