import json
import config
import os
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
    if (not os.path.exists(config.DATA_ROOT)) :
        os.mkdir(config.DATA_ROOT)
    user_data = create_user_db()
    with open(config.LOGIN_DB, 'w') as f:
        json.dump(user_data, f)

    garage_data = create_garage_db()
    with open(config.GARAGE_DB, 'w') as f:
        json.dump(garage_data, f)
