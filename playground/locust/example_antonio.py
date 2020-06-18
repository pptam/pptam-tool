import requests
import json
import datetime
from random import seed
from random import random
import secrets
import string

def extract_values(obj, key):
    """Pull all values of specified key from nested JSON."""
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    results = extract(obj, arr, key)
    return results

#L'applicazione train ticket è configurata con il fuso orario cinese
add_time = 7
time_to_add = datetime.timedelta(hours=add_time)
today = datetime.datetime.today()
china_date = today + time_to_add

today = str(china_date).split()[0]

s = requests.Session()
s.headers.update({'Accept': 'application/json'})
s.headers.update({'Content-Type': 'application/json'})

req=s.get('http://localhost:8080/index.html')

print('GET http://localhost:8080/index.html')
print(req)
print("Response Time: "+str(req.elapsed.total_seconds()))

data = '{"username":"fdse_microservice","password":"111111"}'
req=s.post('http://localhost:8080/api/v1/users/login', data)

# input('Press ENTER to continue')

r = json.loads(req.content)['data']
token = extract_values(r, 'token')[0]
userId = extract_values(r, 'userId')[0]

bearer = "Bearer "+token

s.headers.update({"Authorization": bearer})

r =[]
#iterator = 0
while (not r): #and iterator < 10):
    #iterator=iterator+1
    # seed(1)
    num = random()
    # print(num)
    if(num<0.8):
        end = "Su Zhou"
        start = "Shang Hai"
    else:
        end = str(''.join(secrets.choice(string.ascii_uppercase + string.digits) for i in range(10)))
        start = str(''.join(secrets.choice(string.ascii_uppercase + string.digits) for i in range(10)))

    data = '{"departureTime":"'+today+'","endPlace":"'+end+'","startingPlace":"'+start+'"}'

    req=s.post('http://localhost:8080/api/v1/travelservice/trips/left', data)

    print('POST http://localhost:8080/api/v1/travelservice/trips/left '+data)
    print(req)
    print("Response Time: "+str(req.elapsed.total_seconds()))

    r = json.loads(req.content)['data']
    # print(req.content)

    # input('Press ENTER to continue')

    if r:
        r = json.loads(req.content)['data']

        types = extract_values(r, 'type')
        numbers = extract_values(r, 'number')
        # print(types[0]+numbers[0])

        req=s.get('http://localhost:8080/api/v1/contactservice/contacts')

        # print(req.content)

        # input('Press ENTER to continue')

        r = json.loads(req.content)['data']

        num = random()
        # print(num)
        if(num<0.9):
            contact = extract_values(r, 'id')[0]
        else:
            contact = str(''.join(secrets.choice(string.ascii_uppercase + string.digits) for i in range(10)))

        data = '{"accountId":"'+userId+'","contactsId":"'+contact+'","tripId":"'+types[0]+numbers[0]+'","seatType":"3","date":"'+today+'","from":"'+start+'","to":"'+end+'","assurance":"0","foodType":1,"foodName":"Bone Soup","foodPrice":2.5,"stationName":"","storeName":""}' 

        req=s.post('http://localhost:8080/api/v1/preserveservice/preserve', data)

        print('POST http://localhost:8080/api/v1/preserveservice/preserve '+data)
        print(req)
        print(req.content)
        print("Response Time: "+str(req.elapsed.total_seconds()))

        r = json.loads(req.content)['status']

        # input('Press ENTER to continue')

        if(str(r) != '500'):
            req=s.get('http://localhost:12031/api/v1/orderservice/order')

            # print(req)
            # print(req.content)

            # input('Press ENTER to continue')

            r = json.loads(req.content)['data']

            orders = extract_values(r, 'id')
            # print(orders[len(orders)-1]) 

            data = '{"orderId":"'+orders[len(orders)-1]+'","price":"22.5","tripId":"'+types[0]+numbers[0]+'","userId":"'+userId+'"}' 

            req=s.post('http://localhost:8080/api/v1/inside_pay_service/inside_payment', data)

            print('POST http://localhost:8080/api/v1/inside_pay_service/inside_payment '+data)
            print(req)
            print("Response Time: "+str(req.elapsed.total_seconds()))
            # print(req.content)

            # input('Press ENTER to continue')

            num = random()
            # print(num)
            if(num<0.3):
                req=s.get('http://localhost:8080/api/v1/cancelservice/cancel/refound/'+orders[len(orders)-1])

                print('http://localhost:8080/api/v1/cancelservice/cancel/refound/'+orders[len(orders)-1])
                print(req)
                print("Response Time: "+str(req.elapsed.total_seconds()))
                # print(req.content)

                # input('Press ENTER to continue')

                req=s.get('http://localhost:8080/api/v1/cancelservice/cancel/'+orders[len(orders)-1]+'/'+userId)

                print('http://localhost:8080/api/v1/cancelservice/cancel/'+orders[len(orders)-1]+'/'+userId)
                print(req)
                print("Response Time: "+str(req.elapsed.total_seconds()))
                # print(req.content)

                # input('Press ENTER to continue')