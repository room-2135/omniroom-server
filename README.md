### Omniroom - signaling server + web server
Omniroom is a video monitoring solution designed for escape games but not excluding other use cases.

# Usage
```
virtualenv env
source env/bin/activate
pip install redis
pip install channels
pip install channels-redis
pip install django
pip install django-rest_framework
pip install django-sass
./manage.py migrate core
./manage.py sass core/static/scss core/static/css
./manage.py runserver 0.0.0.0:8000
```
opening http://localhost:8000
