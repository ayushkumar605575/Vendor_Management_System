# Vendor Management System

A Django project with a RESTful API using Django REST Framework.


## Prerequisites

- Python (version 3.x recommended)
- Django
- Django REST Framework

# Setup Instructions

## Create a Virtual Environment:
- Clone the repository
- Open terminal inside the main repo folder and run the following command:
- `python -m venv env`
- `env\Scripts\activate.bat`
- Your Virtual Environment is successfully created and activated.

## Install Dependencies:
- Run `pip install -r requirements.txt` to install the requirements needed for this project.

## Database migration       
- Go inside the project folder `vms` by executing `cd vms` command in terminal.
- Once you are inside the project folder run the following command.             
- `python manage.py makemigrations`      
- `python manage.py migrate`

## Superuser creation
- Run `python manage.py createsuperuser` on terminal to create the superuser.

## Run the Server
- Run `python manage.py runserver` on terminal to run the server everytime.

## Access Django Admin:
- Open the Django admin panel at http://127.0.0.1:8000/admin/ and log in using the superuser credentials.
- Access the database as Admin user.

# Test different API endpoints of the server
- Run 'endpoint_request.py' file and follow the on-screen instructions to test the different functionality of the server.
- This file is specifically made to test the different API endpoints.

### Endpoints
1.  GET /api/vendors/
2.  POST /api/vendors/
3.  GET api/vendors/{vendors_id}/
4.  PUT api/vendors/{vendors_id}/
5.  DELETE api/vendors/{vendors_id}/
6.  GET api/vendors/{vendors_id}/performance/
7.  GET api/purchase_orders/
8.  POST api/purchase_orders/
9.  GET api/purchase_orders/{order_id}/
10. PUT purchase_orders/{order_id}/
11. PATCH purchase_orders/{order_id}/
12. DELETE purchase_orders/{order_id}/
13. PATCH purchase_orders/{order_id}/acknowledge/