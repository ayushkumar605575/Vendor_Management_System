# Django REST API Setup

This repository contains a Django project with a RESTful API using Django REST Framework.

## Prerequisites

- Python (version 3.x recommended)
- Django
- Django REST Framework

# Setup Instructions

## Create a Virtual Environment:
- Open terminal inside a folder (of your choice) and run the following command:
- python -m venv env
- env\Scripts\activate.bat
- Copy the project directory along with the 'env' directory

## Install Dependencies:
- pip install django
- pip install djangorestframework
- pip install requests (for testing APIs)

## Database migration                    
- python manage.py makemigrations      
- python manage.py migrate

## Superuser creation
- python manage.py createsuperuser

## Run the Server
- python manage.py runserver

# Test different API endpoints of the server
- Run 'endpoint_request.py' file and follow the on-screen instructions to test the different functionality of the server.

## Access Django Admin:
- Open the Django admin panel at http://127.0.0.1:8000/admin/ and log in using the superuser credentials.
- Access the database as Admin user.

## Running API endpoints:
- Make sure the models are migrated to database, using the above database migration commands.
- Start the server by executing "python manage.py runserver" command in vms directory containing "manage.py" file.
- Open a terminal window for testing the API endpoints using curl commands.

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