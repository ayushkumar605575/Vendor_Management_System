import requests


with requests.Session() as session:
    response = session.post('http://localhost:8000/api-token-auth/', data={'username':"abhishek", 'password':'abhi@123'})
    
    print(response.status_code)
    print(response.json())

    response = session.post('http://localhost:8000/api/vendors/', data= response.json())
    print(response.json())

    session.close()
