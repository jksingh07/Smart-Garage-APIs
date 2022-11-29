import json
import config
import os
import datetime

def create_user_db():
    user_data = {
        'admin@a.com': {
            config.KEY_EMAIL : "admin@a.com",
            config.KEY_PASSWORD : "admin",
            config.KEY_FIRST_N : "jashan",
            config.KEY_LAST_N : "singh",
            config.KEY_ROLE : "admin"
            }
    }
    return user_data

def create_car_db():
    car_data = {
        'CMKR234': {
            config.KEY_CAR_ID : "CMKR234",
            config.KEY_MILAGE : 25000,
            config.KEY_LAST_UPDATE: "21-11-2022",
            config.KEY_LAST_SERVICE_DATE : "01-10-2022",
            config.KEY_LAST_SERVICE_MILAGE : 20500,
            config.KEY_OIL_TYPE: "TYPE_A",
            config.KEY_TYERS : "Winter",
            config.KEY_AIR_FILTER: 10000,
            config.KEY_BRAKE_OIL: 1000
            }
    }
    return car_data

def create_guest_db():
    guest_data = {
        'admin@a.com+ASE#1': {
            config.KEY_EMAIL : "admin@a.com+ASE#1",
            config.KEY_PASSWORD : 'admin',
            }
    }
    return guest_data

def create_garage_db():
    garage_data = {
        config.KEY_DOOR : -1,
        config.KEY_CO : 0,
        config.KEY_LIGHT : {
            config.KEY_LIGHT_ID[0] : 0,
            config.KEY_LIGHT_ID[1] : 0,
            config.KEY_LIGHT_ID[2] : 0,
            config.KEY_LIGHT_ID[3] : 0
            }
        }
    return garage_data


if __name__ == '__main__':
    # if (not os.path.exists(config.DATA_ROOT)) :
    #     os.mkdir(config.DATA_ROOT)
    # user_data = create_user_db()
    # with open(config.LOGIN_DB, 'w') as f:
    #     json.dump(user_data, f)
    #
    # garage_data = create_garage_db()
    # with open(config.GARAGE_DB, 'w') as f:
    #     json.dump(garage_data, f)
    #
    # car_data = create_car_db()
    # with open(config.CAR_DB, 'w') as f:
    #     json.dump(car_data, f)
    #
    # guest_data = create_guest_db()
    # with open(config.GUEST_DB, 'w') as f:
    #     json.dump(guest_data, f)

    notification_records = {"CO": datetime.datetime.timestamp(datetime.datetime.now())}
    with open(config.NOTIFY_DB, 'w') as f:
            json.dump(notification_records, f)
