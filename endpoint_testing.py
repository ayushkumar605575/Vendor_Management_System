import requests, json
from datetime import datetime

Choice = '''
Choose your endpoint to test:
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
Press Any Other Numeric Key to Exit
'''

cred = {'username':str(input("Enter your superuser username: ")), 'password':str(input("Enter your superuser password: "))}

with requests.Session() as session:
    response = session.post('http://localhost:8000/api-token-auth/', data= cred)
    # print(response.headers)
    
    # print(response.status_code)
    try:
        auth = {'Authorization': f"Token {response.json()['token']}"}
    except:
        print("Wrong Username or Password\nExiting...")
        exit()
    print("------------------------")
    print(auth)
    print("------------------------")
    while 1:
        print(Choice)
        try:
            choice = int(input("Enter your Choice: "))
        except:
            continue
        if choice == 1:
            response = session.get('http://localhost:8000/api/vendors/', headers = auth)
            print("--------------------------------")
            print(response.text)
            print("--------------------------------")
        elif choice == 2:

            data = {
                "vendor_code": str(input("Enter Vendor Code:(Case Sensitive) ")),
                "name": str(input("Enter Vendor Name: ")),
                "contact_details": str(input("Enter Vendor Contact Details: ")),
                "address": str(input("Enter Vendor Address: ")),
                "on_time_delivery_rate": 0.0,
                "quality_rating_avg": 0.0,
                "average_response_time": 0.0,
                "fulfillment_rate": 0.0
            }

            response = session.post('http://localhost:8000/api/vendors/', headers = auth, data = data)

            print("--------------------------------")
            if response.status_code == 201:
                print("Vendor Successfully Added")
            print(response.text)
            print("--------------------------------")

        elif choice == 3:

            vendor_id = str(input("Enter Vendor Code:(Case Sensitive) "))
            response = session.get(f'http://localhost:8000/api/vendors/{vendor_id}/', headers = auth)
            print("--------------------------------")
            print(response.text)
            print("--------------------------------")

        elif choice == 4:
            vendor_id = str(input("Enter Vendor Code:(Case Sensitive) "))

            data = {
                "vendor_code": vendor_id,
                "name": str(input("Enter New Vendor Name: ")),
                "contact_details": str(input("Enter New Vendor Contact Details: ")),
                "address": str(input("Enter New Vendor Address: ")),
                "on_time_delivery_rate": float(input("Enter updated on time delivery rate:(Float value) ")),
                "quality_rating_avg": float(input("Enter updated quality rating average:(Float value) ")),
                "average_response_time": float(input("Enter  updated average response time:(Float value) ")),
                "fulfillment_rate": float(input("Enter  updated fulfillment rate:(Float value) ")),
            }

            response = session.put(f'http://localhost:8000/api/vendors/{vendor_id}/', headers = auth, data=data)

            print("--------------------------------")
            print(response.text)
            print("--------------------------------")

        elif choice == 5:

            vendor_id = str(input("Enter Vendor Code:(Case Sensitive) "))

            response = session.delete(f'http://localhost:8000/api/vendors/{vendor_id}/', headers = auth)

            print("--------------------------------")
            if response.status_code == 204:
                print("Order Successfully Deleted")
            else:
                print(response.text)
            print("--------------------------------")

        elif choice == 6:

            vendor_id = str(input("Enter Vendor Code:(Case Sensitive) "))

            response = session.get(f'http://localhost:8000/api/vendors/{vendor_id}/performance/', headers = auth)

            print("--------------------------------")
            print(response.text)
            print("--------------------------------")
        elif choice == 7:
            
            response = session.get('http://localhost:8000/api/purchase_orders/', headers = auth)

            print("--------------------------------")
            print(response.text)
            print("--------------------------------")

        elif choice == 8:

            data = {"po_number":str(input("Create Purchase Order Code: ")),
                    "order_date":datetime.now(),
                    "delivery_date":"2025-05-23T21:59:00Z",
                    "delivered_data":None,
                    "items":json.dumps([{"item_name":"Name1"},{"item_name":"Name2"}]),
                    "status":"Order Placed","quality_rating":88.0,
                    "issue_date":datetime.now(),
                    "acknowledgment_date":datetime.now(),
                    "vendor":str(input("Enter Vendor Code:(Case Sensitive) ")),
                    }
            
            response = session.post('http://localhost:8000/api/purchase_orders/', headers = auth, data = data)

            print("--------------------------------")
            print(response.text)
            print("--------------------------------")

        elif choice == 9:

            order_id = str(input("Enter Purchase Order Code:(Case Sensitive) "))

            response = session.get(f'http://localhost:8000/api/purchase_orders/{order_id}/', headers = auth)

            print("--------------------------------")
            print(response.text)
            print("--------------------------------")

        elif choice == 10:

            order_id = str(input("Enter Purchase Order Code:(Case Sensitive) "))

            data = {"po_number":str(input("Enter New Purchase Order Code: ")),
                    "order_date":datetime.now(),
                    "delivery_date":"2025-05-23T21:59:00Z",
                    "delivered_data":None,
                    "items":json.dumps([{"item_name":"Name1"},{"item_name":"Name2"}]),
                    "status":"Order Placed","quality_rating":88.0,
                    "issue_date":datetime.now(),
                    "acknowledgment_date":datetime.now(),
                    "vendor":str(input("Enter Vendor Code:(Case Sensitive) "))
                    }
            
            response = session.put(f'http://localhost:8000/api/purchase_orders/{order_id}/', headers = auth, data = data)

            print("--------------------------------")
            print(response.text)
            print("--------------------------------")

        elif choice == 11:

            order_id = str(input("Enter Purchase Order Code:(Case Sensitive) "))
            
            data = {"po_number":order_id,
                    # "order_date":datetime.now(),
                    # "delivery_date":"2025-05-23T21:59:00Z",
                    # "delivered_data":None,
                    # "items":json.dumps([{"item_name":"Name1"},{"item_name":"Name2"}]),
                    # "status":"Order Placed",
                    "quality_rating" : float(input("Enter Quality Rating(Float Value): ")),
                    # "issue_date":datetime.now(),
                    # "acknowledgment_date":datetime.now(),
                    # "vendor":str(input("Enter Vendor Code:(Case Sensitive) "))
                    }

            response = session.patch(f'http://localhost:8000/api/purchase_orders/{order_id}/', headers = auth, data = data)

            print("--------------------------------")
            print(response.text)
            print("--------------------------------")


        elif choice == 12:

            order_id = str(input("Enter Purchase Order Code:(Case Sensitive) "))

            response = session.delete(f'http://localhost:8000/api/purchase_orders/{order_id}/', headers = auth)

            print("--------------------------------")
            if response.status_code == 204:
                print("Order Successfully Deleted")
            else:
                print(response.text)
            print("--------------------------------")

        elif choice == 13:

            order_id = str(input("Enter Order ID:(Case Sensitive) "))

            data = {"acknowledgment_date":datetime.now()}

            response = session.patch(f'http://localhost:8000/api/purchase_orders/{order_id}/acknowledge/', headers = auth, data = data)

            print("--------------------------------")
            print("Acknowledged Date Updated to Current Time")
            print("--------------------------------")

        else:
            break


    # data = {"acknowledgment_date":"2024-05-01T16:55:03Z"}


    # response = session.get('http://localhost:8000/api/vendors/', headers = dat)#, data = data)
    # print(response.text)
    # print(response.status_code)

    session.close()

