1- create postgres database AE_Back  
2- open directory `SAD_Project_Back/SAD_backend`    
3- run redis with `redis-server`    
4- run  celery with `celery -A backend worker -l INFO`    
5- run `python3 manage.py migrate`   
6- run  `python3 manage.py loaddata Content-type.json`  
7- run `python3 manage.py runserver`