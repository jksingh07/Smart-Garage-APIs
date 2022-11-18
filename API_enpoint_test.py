import requests
import json
import collections
import pandas as pd

SERVER_URL = 'http://4.229.225.201:5000/'

# Routes
GET_LIGHTS = 'light'
GET_DOOR = 'door'
GET_CO = 'co'

SET_LIGHT = 'light'
SET_DOOR = 'door'
SET_CO = 'co'

compare = lambda x, y: collections.Counter(x) == collections.Counter(y)

test_cases = [
    'Check if the Get Light route is able to fetch the right data from the cloud storage.',      #0
    'Check if the Get Door route is able to fetch the correct data from the cloud storage.',     #1
    'Check if the Get Co Level route is able to fetch the correct data from the cloud storage.', #2
    'Check if the value set Lights operation is able to set value on the cloud storage.',        #3
    'Check if the value set Door operation is able to set value on the cloud storage.',          #4
    'Check if the value set Co level operation is able to set value on the cloud storage.',      #5
]

def assert_endpoint(route, payload, value_range) :
    stat = 'FAIL'
    stat_code = -1
    expected = 'Error'
    actual = 'Error'
    try:
        url = SERVER_URL + route
        req = requests.get(url)

        stat_code = req.status_code
        response = req.text

        if stat_code != 200:
            print(route, ":", stat_code, '=>', stat)
            return (route, stat_code, 'none',expected, actual, stat)

        expected = json.loads(payload)
        actual = json.loads(response)
        #print("Expected :", expected)
        #print("Actual   :", actual)

        if compare(expected.keys(), actual.keys()):
            stat = 'PASS'
        else :
            stat = 'FAIL'

        if stat == 'PASS':
            error = 0
            for k,v in actual.items():
                #print("k,V :", k ,v)
                if int(v) not in range(value_range[0], value_range[1] + 1):
                    error += 1
            stat = 'PASS' if (error < 1) else 'FAIL'
        print(route, ":", stat_code, '=>', stat)
        return (route, stat_code, 'none',expected, actual, stat)
    except Exception as e:
        print(route, ":", stat_code, '=>', stat)
        return (route, stat_code, 'none',expected, actual, stat)

def assert_endpoint_value(route, payload) :
    stat = 'FAIL'
    stat_code = -1
    expected = 'Error'
    actual = 'Error'
    try:
        url = SERVER_URL + route
        req = requests.get(url)

        stat_code = req.status_code
        response = req.text

        if stat_code != 200:
            print(route, ":", stat_code, '=>', stat)
            return (route, stat_code, 'none',expected, actual, stat)

        expected = json.loads(payload)
        actual = json.loads(response)
        #print("Expected :", expected)
        #print("Actual   :", actual)

        if compare(expected.keys(), actual.keys()):
            stat = 'PASS'
        else :
            stat = 'FAIL'

        if stat == 'PASS':
            if compare(expected.values(), actual.values()):
                stat = 'PASS'
            else :
                stat = 'FAIL'
        print(route, ":", stat_code, '=>', stat)
        return (route, stat_code, 'none',expected, actual, stat)
    except Exception as e:
        print("Error   :", e)
        print(route, ":", stat_code, '=>', stat)
        return (route, stat_code, 'none',expected, actual, stat)

def assert_set_status(route, body) :
    stat = 'FAIL'
    stat_code = -1
    expected = 'Error'
    actual = 'Error'
    try:
        url = SERVER_URL + route
        headers = {'Content-type': 'application/json'}
        req = requests.post(url, data=body, headers=headers)

        stat_code = req.status_code
        response = req.text

        if stat_code != 200:
            print(route, ":", stat_code, '=>', stat)
            return (route, stat_code, body, expected, actual, stat)

        payload = '{"status":1}'
        expected = json.loads(payload)
        actual = json.loads(response)
        #print("Expected :", expected)
        #print("Actual   :", actual)

        if compare(expected.keys(), actual.keys()):
            stat = 'PASS'
        else :
            stat = 'FAIL'

        if stat == 'PASS':
            error = 0
            for k,v in actual.items():
                #print("k,V :", k ,v)
                if v != 1:
                    error += 1
            stat = 'PASS' if (error < 1) else 'FAIL'
        print(route, ":", stat_code, '=>', stat)
        return (route, stat_code, body, expected, actual, stat)
    except Exception as e:
        print(route, ":", stat_code, '=>', stat)
        return (route, stat_code, body, expected, actual, stat)

test_case_id_list = []
test_cases_list = []
route_list = []
status_code_list = []
input_list = []
expected_list = []
actual_list = []
status_list = []

count = 0
def add_test_case(case_index, tup) :
    global count
    test_case_id_list.append("TC" + "-" + str(case_index) + "-"+ str(count).rjust(2, '0'))
    test_cases_list.append(test_cases[case_index])
    route_list.append(tup[0])
    status_code_list.append(tup[1])
    input_list.append(tup[2])
    expected_list.append(tup[3])
    actual_list.append(tup[4])
    status_list.append(tup[5])
    count += 1

# Get Lights Test
add_test_case(0, assert_endpoint(GET_LIGHTS, '{"Light_Ext":1,"Light_L":1,"Light_M":0,"Light_R":0}', [0,1]))

# Get Door Test
add_test_case(1, assert_endpoint(GET_DOOR, '{"door":0}', [-1,1]))

# Get CO Level
add_test_case(2, assert_endpoint(GET_CO, '{"CO":0}', [0,100]))

# send Open Door Check
add_test_case(4, assert_set_status(SET_DOOR, '{"command": "OPEN"}'))
# Actual value test
add_test_case(1, assert_endpoint(GET_DOOR, '{"door":0}', [1,1]))

# send STOP Door Check
add_test_case(4, assert_set_status(SET_DOOR, '{"command": "STOP"}'))
# Actual value test
add_test_case(1, assert_endpoint(GET_DOOR, '{"door":0}', [0,0]))

# send Open Door Check
add_test_case(4, assert_set_status(SET_DOOR, '{"command": "CLOSE"}'))
# Actual value test
add_test_case(1, assert_endpoint(GET_DOOR, '{"door":0}', [-1,-1]))

# All Lights Off Test
add_test_case(3, assert_set_status(SET_LIGHT, '{"Light": "Light_Ext","Value":0}'))
add_test_case(3, assert_set_status(SET_LIGHT, '{"Light": "Light_L","Value":0}'))
add_test_case(3, assert_set_status(SET_LIGHT, '{"Light": "Light_R","Value":0}'))
add_test_case(3, assert_set_status(SET_LIGHT, '{"Light": "Light_M","Value":0}'))

# Get Lights Test
add_test_case(0, assert_endpoint_value(GET_LIGHTS, '{"Light_Ext":0,"Light_L":0,"Light_M":0,"Light_R":0}'))

# Light_Ext Light Check
add_test_case(3, assert_set_status(SET_LIGHT, '{"Light":"Light_Ext", "Value":1}'))
add_test_case(0, assert_endpoint_value(GET_LIGHTS, '{"Light_Ext":1,"Light_L":0,"Light_M":0,"Light_R":0}'))

# Light_L Light Check
add_test_case(3, assert_set_status(SET_LIGHT, '{"Light":"Light_L", "Value":1}'))
add_test_case(0, assert_endpoint_value(GET_LIGHTS, '{"Light_Ext":1,"Light_L":1,"Light_M":0,"Light_R":0}'))

# Light_M Light Check
add_test_case(3, assert_set_status(SET_LIGHT, '{"Light":"Light_M", "Value":1}'))
add_test_case(0, assert_endpoint_value(GET_LIGHTS, '{"Light_Ext":1,"Light_L":1,"Light_M":1,"Light_R":0}'))

# Light_R Light Check
add_test_case(3, assert_set_status(SET_LIGHT, '{"Light":"Light_R", "Value":1}'))
add_test_case(0, assert_endpoint_value(GET_LIGHTS, '{"Light_Ext":1,"Light_L":1,"Light_M":1,"Light_R":1}'))

# Check Co sensor set Co level
add_test_case(5, assert_set_status(SET_CO, '{"value":10}'))
# Check read Co level
add_test_case(2, assert_endpoint_value(GET_CO, '{"CO":10}'))

df = pd.DataFrame({
    'Test Case ID': test_case_id_list,
    'Test Case Series': test_cases_list,
    'API Endpoint': route_list,
    'Connection Status': status_code_list,
    'Input Data': input_list,
    'Expected Data': expected_list,
    'Actual Data': actual_list,
    'Test Status': status_list
})
df.to_csv('API_Test_report.csv', index=False)

if 'FAIL' in df['Test Status'].values:
    print("Test Complete : FAIL")
    raise Exception("Testing Failed, Check the test report.")
else :
    print("Test Complete : PASS")
