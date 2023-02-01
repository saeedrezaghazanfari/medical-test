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

### create db
```
python manage.py makemigrations
```
```
python manage.py migrate
```

### Run Server
```
python manage.py runserver 8000
```



### api usage:

send username and password as a json to http://127.0.0.1:8000/en/api/v1/get-token/
this request must be POST method.
```
{
    "username": "1111111111",
    "password": peaka
}
```
you have two token: refresh token and access token
for request to any urls, you must have access token.
you can update the "access token" with "refresh token" 


## api documentation

POST: send (username) (password)
```
/fa/api/v1/get-token/
```


POST: send (refresh_token)
```
/fa/api/v1/get-token/refresh-token/
```


POST: send (code: this is patient international code)
```
/fa/api/v1/get/patient/data/
```


POST: dont need to any data, just send request (you must have valid access token)

this url for get user labels, if you dont use 'permission' parameter.
```
/fa/api/v1/get/user/data/
```


POST: send (title: title of sono center) (code: code of sono center) (password) (pos: position of sono center) (phone) (permission)
```
/fa/api/v1/create/sonography-center/
```


POST: send (title: title of lab center) (code: code of lab center) (password) (pos: position of lab center) (phone) (permission)
```
/fa/api/v1/create/lab/
```


POST: send (title: title of lab category)
```
/fa/api/v1/create/lab-category/
```


POST: send (username: manager national code) (password) (first_name) (last_name) (email) (phone) (permission)
```
/fa/api/v1/create/manager/
```


POST: send (medical_code: doctor medical code) (username: manager national code) (password) (first_name) (last_name) (email) (phone) (permission)
```
/fa/api/v1/create/doctor/
```


POST: send (username: patient national code)
```
/fa/api/v1/create/patient/
```


POST: send (category_title: enter title of lab category) (patinet_username: international code of patient) (lab_username: code of lab) (title) (result: result of patient lab)
```
/fa/api/v1/create/patient/lab/
```


POST: send  (patinet_username: international code of patient) (sono_username: code of sono center) (result: result of patient sonography)
```
/fa/api/v1/create/patient/sonography/
```