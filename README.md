System Analysis and Design Final Project Backend
========================================

This repo is the backend part of the file management project for the SAD course instructed by Dr. Mehdi Mostafazade at the Sharif University of Technology. The frontend code can be found [here](https://github.com/theablemo/System-Analysis-and-Design-Project-Frontend).

# Collborators

- [Mohammad Abolnejadian](https://github.com/theablemo)
- [Mohammadali Khodabandelou](https://github.com/amirrezamirzaei)
- [Amirreza Mirzaei](https://github.com/MohammadAli-Khodabandelou)
- [Alireza Eiji](https://github.com/AlirezaEiji191379)
- [Matin Daghyani](https://github.com/mtndaghyani)

# Introduction to the platform

This project is an Android-first application that can be used as a file-sharing platform. Easily upload your files to your account and download them anywhere using your personal account. This app is made to make managing your files easy and delightful, with a modern and colorful design.

# Setup

1. Create Postgres database AE_Back  
2. open directory `SAD_Project_Back/SAD_backend`    
3. run redis with `redis-server`    
4. run  celery with `celery -A backend worker -l INFO`    
5. run `python3 manage.py migrate`   
6. run  `python3 manage.py loaddata Content-type.json`  
7. run `python3 manage.py runserver`
