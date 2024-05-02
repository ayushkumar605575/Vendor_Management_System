import requests, json


cred = {'username':"abhishek", 'password':'abhi@123'}

with requests.Session() as session:
    response = session.post('http://localhost:8000/api-token-auth/', data= cred)
    # print(response.headers)
    
    # print(response.status_code)
    
    dat = {'Authorization': f"Token {response.json()['token']}"}

    print(dat)

    dataa = {
    "vendor_code": "AIR3543TEL",
    "name": "Airtel",
    "contact_details": "Contact 2",
    "address": "Address 2",
    "on_time_delivery_rate": 1.5,
    "quality_rating_avg": 2.4,
    "average_response_time": 1,
    "fulfillment_rate": 6.5}

    dataa = {"acknowledgment_date":"2024-05-01T16:55:03Z",}


    response = session.patch('http://localhost:8000/api/purchase_orders/SAM3543SUNG0001/acknowledge/', headers = dat, data = dataa)
    print(response.text)
    print(response.status_code)

    session.close()

