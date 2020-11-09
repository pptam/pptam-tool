import requests
import json
import datetime

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

session = requests.Session()
session.headers.update({'Accept': 'application/json'})
session.headers.update({'Content-Type': 'application/json'})

host = "http://socks3.inf.unibz.it:16686/"

start_timestamp = datetime.datetime(2020, 11, 6, 17, 52, 0).timestamp()
end_timestamp = datetime.datetime(2020, 11, 6, 17, 52, 10).timestamp()
step_seconds = 5

services = ['ts-order-service', 'ts-auth-service','ts-basic-service']

for service in services:

    print('Querying ' + service + '...')

    current_timestamp = start_timestamp
    while current_timestamp < end_timestamp:

        start_date = datetime.datetime.fromtimestamp(current_timestamp).strftime('%s') + '000000'
        current_timestamp = current_timestamp + step_seconds
        end_date = datetime.datetime.fromtimestamp(current_timestamp).strftime('%s') + '000000'
        #print(start_date + ' ' + end_date)

        uri =  host + "api/traces?end=" + end_date + "&limit=1500&lookback=1h&maxDuration&minDuration&service=" + service + "&start=" + start_date

        print(uri)

        req = session.get(uri)

        resp = json.loads(req.content)['data']
        trace_id = extract_values(resp, 'traceID')

        print('Collecting ' + str(int(len(trace_id)/2)) + ' traces...')

        log_file = 'jaeger_' + service + '_' + start_date + '-' + end_date + '.log'
        with open(log_file, 'a') as f:
            for i in range(0, int(len(trace_id)/2)):
                #print(i+1)
                resp = session.get(host + 'api/traces/' + trace_id[i*2])
                data = json.loads(resp.content)
                f.write(json.dumps(data) + '\n')
