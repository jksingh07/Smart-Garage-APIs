import json
import config
import main
import random

#
# Local File Systems
#
# Read the saved garage Data
def read_garage_data_db():
    with open(config.GARAGE_DB, 'r') as file:
        data = file.read()
    d = json.loads(data)
    return d


# Read the saved user Data
def read_user_data_db():
    with open(config.LOGIN_DB, 'r') as file:
        data = file.read()
    d = json.loads(data)
    return d

# Read the saved car Data
def read_car_data_db():
    with open(config.CAR_DB, 'r') as file:
        data = file.read()
    d = json.loads(data)
    return d

# Read the saved guest Data
def read_guest_data_db():
    with open(config.GUEST_DB, 'r') as file:
        data = file.read()
    d = json.loads(data)
    return d

# Read the saved notification Data
def read_notify_data_db():
    with open(config.NOTIFY_DB, 'r') as file:
        data = file.read()
    d = json.loads(data)
    return d

# Save data to the local File System
def save_garage_data(garage_data):
    with open(config.GARAGE_DB, 'w') as file:
        json.dump(garage_data, file)

def save_login_data(login_db):
    with open(config.LOGIN_DB, 'w') as file:
        json.dump(login_db, file)

def save_guest_data(guest_db):
    with open(config.GUEST_DB, 'w') as file:
        json.dump(guest_db, file)

def save_car_data(car_db):
    with open(config.CAR_DB, 'w') as file:
        json.dump(car_db, file)

def save_notify_data(n_db):
    with open(config.NOTIFY_DB, 'w') as file:
        json.dump(n_db, file)

#
# User System
#
# Check if the user exist in login Data
def check_valid_user(email, password, login_db):
    if email not in login_db.keys():
        # User not present
        return -1
    else :
        user = login_db[email]
        if user[config.KEY_PASSWORD] == password:
            # Valid user
            return 0
        else :
            # Password incorrect
            return -2

# Save new user data
def save_new_user(email, password, first, last, role, login_db):
    try:
        if email in login_db.keys():
            # User alreay registered
            return login_db,-1
        else :
            login_db[email]  = {
                config.KEY_EMAIL : email,
                config.KEY_PASSWORD : password,
                config.KEY_FIRST_N : first,
                config.KEY_LAST_N : last,
                config.KEY_ROLE : role
            }
        save_login_data(login_db)
        return login_db,0
    except Exception as e:
        return login_db,-2

#
# Guest Access
#
# Check if the user exist in Guest Data
def check_valid_guest(email, password, guest_db):
    if email not in guest_db.keys():
        # User not present
        return -1
    else :
        user = guest_db[email]
        if user[config.KEY_PASSWORD] == password:
            # Valid user
            return 0
        else :
            # Password incorrect
            return -2

def get_max_guest_id(email, guest_db):
    email_d = email.split(config.KEY_GUEST_CONJUSCTION)
    for i in range(3):
        chk_e = email_d[0] + config.KEY_GUEST_CONJUSCTION + str(i)
        if (chk_e not in guest_db.keys()):
            return chk_e


# save newly generated guest data
def save_new_guest(email, password, guest_db):
    try:
        if email in guest_db.keys():
            # User alreay registered
            email = get_max_guest_id(email, guest_db)
        guest_db[email]  = {
                config.KEY_EMAIL : email,
                config.KEY_PASSWORD : password,
        }
        save_guest_data(guest_db)
        return email, password ,0
    except Exception as e:
        return email, e,-2

# generate random password
def generate_pasword():
    pas = ""
    for i in range(10):
        rand = random.randint(97,122)
        pas += chr(rand)
    return pas
#
# Lighting System
#
# Read the lights status
def get_lights_status(garage_data):
    return garage_data[config.KEY_LIGHT]

# set the status of the given light with given value
def set_light_status(light, value, garage_data):
    garage_data[config.KEY_LIGHT][light] = value
    save_garage_data(garage_data)
    return garage_data

#
# Door System
#
# Read the current Door Status
def get_door_stat(garage_data):
    return garage_data[config.KEY_DOOR]

def set_door_status(value, garage_data):
    garage_data[config.KEY_DOOR] = value
    save_garage_data(garage_data)
    return garage_data

#
# Co system
#
# Read the current Co value
def get_co_level(garage_data):
    return garage_data[config.KEY_CO]

# Read the current Co value
def set_co_level(value, garage_data):
    garage_data[config.KEY_CO] = value
    save_garage_data(garage_data)
    return garage_data
