import json
global garage_db

global user_data, garage_data
def get_lights_door():
    global garage_data
    return garage_data

def get_user_data():
    global user_data
    return user_data

def save_new_user(first, last, email, username, password, user_data):
    try:
        user_data['username'].append(username)
        user_data['password'].append(password)
        user_data['first_name'].append(first)
        user_data['last_name'].append(last)
        user_data['email_id'].append(email)

        with open('login_db.json', 'w') as f:
            json.dump(user_data, f)

        return user_data
    except:
        return []



#def check_login()   

def set_light(light, action,  garage_data):
    garage_data[light] = action
    return garage_data

def read_user_data_db():
    with open('login_db.json', 'r') as myfile:
        data=myfile.read()
    login_data = json.loads(data)

    
    return login_data

def read_garage_data_db():
    with open('garage_db.json', 'r') as myfile:
        data=myfile.read()
    garage_data = json.loads(data)

    return garage_data

def read_co_data_db():
    with open('co_db.json', 'r') as myfile:
        data=myfile.read()
    co_data = json.loads(data)

    return co_data

#user_data, garage_data = read_db()

#a = get_lights_door()
#b = get_user_data()
#print(a,b)
#save_new_user('Bikramjeet', 'Singh', 'bikram@gmail.com', 'bikram', 'password', user_data)

#garage_data = set_light('light_ext', 1, garage_data)
#print(user_data, garage_data)

