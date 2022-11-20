import json
import config
import main


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

# Save data to the local File System
def save_garage_data(garage_data):
    with open(config.GARAGE_DB, 'w') as file:
        json.dump(garage_data, file)

def save_login_data(login_db):
    with open(config.LOGIN_DB, 'w') as file:
        json.dump(login_db, file)

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
            login_db[email]  : {
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
