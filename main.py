from flask import Flask, jsonify, request
from functools import wraps
from utilities import *
import datetime
import requests
import jwt
import config


app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['ALGO'] = config.TOKEN_ALGO

def check_for_token(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        token = request.args.get(config.KEY_TOKEN)
        if not token:
            return jsonify({'message': 'Missing token'}), 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], app.config['ALGO'])
        except Exception as e:
            return jsonify({'messgae': 'Invalid token - ' + str(e)}), 403
        return func(*args, **kwargs)
    return wrapped

@app.route('/', methods=['POST'])
@check_for_token
def check_valid():
    try:
        content = request.json
        if (config.KEY_DEVICE in content.keys()):
            deviceId = content[config.KEY_DEVICE]
            user = content[config.KEY_EMAIL]
            login_db = read_user_data_db();
            guest_db = read_guest_data_db();
            if user in login_db.keys():
                login_db[user][config.KEY_DEVICE] = deviceId
                save_login_data(login_db)
            elif user in guest_db.keys():
                return jsonify({config.KEY_VALID: 1})
            else :
                raise Exception("User not registered. Plz sign up again.")
        return jsonify({config.KEY_VALID: 1})
    except Exception as e:
        return jsonify({config.KEY_VALID: str(e)}), 422

@app.route('/sim', methods = ['GET'])
def simlogin():
    token = jwt.encode({
        'user': 'sim',
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=4)
        },
        app.config['SECRET_KEY'],
        algorithm= app.config['ALGO']
    )
    return jsonify({config.KEY_TOKEN: token})

@app.route('/login', methods = ['POST'])
def login():
    try:
        content = request.json
        email = content[config.KEY_EMAIL]
        password = content[config.KEY_PASSWORD]
        deviceId = content[config.KEY_DEVICE]
        login_db = read_user_data_db();
        chk = check_valid_user(email, password, login_db)

        if chk == 0 :
            if deviceId != "":
                login_db[email][config.KEY_DEVICE] = deviceId
                save_login_data(login_db)
            token = jwt.encode({
                'user': email,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60)
                },
                app.config['SECRET_KEY'],
                algorithm= app.config['ALGO']
            )
            return jsonify({config.KEY_TOKEN: token})
        elif chk == -1:
            raise Exception("User not registered in the database.")
        elif chk == -2:
            raise Exception("The password entered is incorrect, please enter the correct password.")
    except Exception as e:
        return jsonify({'status': str(e)}), 422

@app.route('/login_guest', methods = ['POST'])
def guest_login():
    try:
        content = request.json
        email = content[config.KEY_EMAIL]
        password = content[config.KEY_PASSWORD]
        guest_db = read_guest_data_db();
        chk = check_valid_guest(email, password, guest_db)

        if chk == 0 :
            token = jwt.encode({
                'user': email,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60)
                },
                app.config['SECRET_KEY'],
                algorithm= app.config['ALGO']
            )
            return jsonify({config.KEY_TOKEN: token})
        elif chk == -1:
            raise Exception("User not registered in the database.")
        elif chk == -2:
            raise Exception("The password entered is incorrect, please enter the correct password.")
    except Exception as e:
        return jsonify({'status': str(e)}), 422

@app.route('/add_guest', methods=['POST'])
@check_for_token
def add_guest():
    try:
        content = request.json
        email = content[config.KEY_EMAIL]
        guest_db = read_guest_data_db()
        guest_email = email + config.KEY_GUEST_CONJUSCTION + str(len(guest_db) - 1)
        password = generate_pasword()
        email, password,chk = save_new_guest(guest_email, password, guest_db)
        if chk == 0:
            return jsonify({config.KEY_EMAIL: email, config.KEY_PASSWORD: password})
        elif chk == -2:
            raise Exception("Unable to create new guest, try again later." + str(password))
    except Exception as e:
        return jsonify({"status": str(e)}), 422

@app.route('/revoke_guest', methods=['POST'])
@check_for_token
def revoke_guest():
    try:
        content = request.json
        email = content[config.KEY_EMAIL]
        password = content[config.KEY_PASSWORD]

        guest_db = read_guest_data_db()
        if email not in guest_db.keys():
            # User not present
            raise Exception("The guest email provided is not valid.")
        else :
            user = guest_db[email]
            if user[config.KEY_PASSWORD] == password:
                # Valid user
                del guest_db[email]
                save_guest_data(guest_db)
                return jsonify({"status": 1})
            else :
                # Password incorrect
                raise Exception("The password and email conbination provided is not valid.")

    except Exception as e:
        return jsonify({"status": str(e)}), 422

@app.route('/guest', methods=['POST'])
@check_for_token
def get_guest():
    try:
        content = request.json
        email = content[config.KEY_EMAIL]
        guest_db = read_guest_data_db()
        guests = []
        for guest in guest_db:
            if guest.split(config.KEY_GUEST_CONJUSCTION)[0] == email:
                guests.append(guest_db[guest])
        return jsonify(guests)
    except Exception as e:
        return jsonify({"status": str(e)}), 422

@app.route('/user', methods=['POST'])
@check_for_token
def get_user():
    try:
        content = request.json
        email = content[config.KEY_EMAIL]
        user_db = read_user_data_db()
        if email in user_db.keys():
            return jsonify(user_db[email])
        else:
            raise Exception("User not found in the login db.");
    except Exception as e:
        return jsonify({"status": str(e)}), 422

@app.route('/update_profile', methods=['POST'])
@check_for_token
def update_user_profile():
    try:
        content = request.json
        email = content[config.KEY_EMAIL]
        first_name = content[config.KEY_FIRST_N]
        last_name = content[config.KEY_LAST_N]
        user_db = read_user_data_db()
        if first_name == "" or last_name == "" :
            raise Exception("The first Name or last Name is invalid.")
        if email in user_db.keys():
            user_db[email][config.KEY_FIRST_N] = first_name
            user_db[email][config.KEY_LAST_N] = last_name
            save_login_data(user_db)
            return jsonify({"status":1})
        else:
            raise Exception("User not found in the login db.");
    except Exception as e:
        return jsonify({"status": str(e)}), 422

@app.route('/sign_up', methods=['POST'])
def sign_up():
    try:
        content = request.json
        email = content[config.KEY_EMAIL]
        password = content[config.KEY_PASSWORD]
        first = content[config.KEY_FIRST_N]
        last = content[config.KEY_LAST_N]
        role = "admin"

        login_db = read_user_data_db();
        login_db,chk = save_new_user(email, password, first, last, role, login_db)
        if chk == 0:
            return jsonify({"status": 1})
        elif chk == -1 :
            raise Exception("User already registered, Please try to login.")
        elif chk == -2:
            raise Exception("User write error in database, try again later.")
    except Exception as e:
        return jsonify({"status": str(e)})


@app.route('/door', methods=['GET'])
@check_for_token
def get_door():
    try:
        garage_data = read_garage_data_db()
        return jsonify({config.KEY_DOOR: garage_data[config.KEY_DOOR]})
    except Exception as e:
        return jsonify({'status': str(e)})

@app.route('/door', methods=['POST'])
@check_for_token
def set_door():
    try:
        garage_data = read_garage_data_db()
        content = request.json
        cmd = content[config.KEY_COMMAND]

        if -1 <= cmd <= 1:
            garage_data[config.KEY_DOOR] = cmd
            save_garage_data(garage_data)
        else :
            raise Exception("Invalid Door Status.")
        return jsonify({'status': 1})
    except Exception as e:
        return jsonify({"status": str(e)}), 422


@app.route('/light', methods=['GET'])
@check_for_token
def get_lights():
    try:
        garage_data = read_garage_data_db()
        return jsonify(garage_data[config.KEY_LIGHT])
    except Exception as e:
        return jsonify({'status': str(e)})


@app.route('/light', methods=['POST'])
@check_for_token
def set_light():
    try:
        garage_data = read_garage_data_db()
        content = request.json
        light = content[config.KEY_LIGHT]
        value = content[config.KEY_VALUE]

        if light in config.KEY_LIGHT_ID:
            if 0 <= value <= 1:
                garage_data[config.KEY_LIGHT][light] = value
                save_garage_data(garage_data)
            else :
                raise Exception("Invalid value for Light Status.")
        else :
            raise Exception("Invalid Identifier for Light.")
        return jsonify({"status": 1})
    except:
        return jsonify({'status': str(e)}), 422

@app.route('/co', methods=['GET'])
@check_for_token
def get_co():
    try:
        garage_data = read_garage_data_db()
        return jsonify({config.KEY_CO: garage_data[config.KEY_CO]})
    except Exception as e:
        return jsonify({'status': str(e)})

@app.route('/co', methods=['POST'])
@check_for_token
def set_co():
    try:
        garage_data = read_garage_data_db()
        content = request.json
        value = content[config.KEY_CO]
        if 0 <= value <= 1000:
            garage_data[config.KEY_CO] = value
            save_garage_data(garage_data)
            # ead to check if notification was sent
            if (value > 50) :
                n_db = read_notify_data_db()
                cur_n = datetime.datetime.now()
                old_n = datetime.datetime.fromtimestamp(n_db['CO'])
                if (cur_n-old_n).total_seconds() > 10 :
                    n_db['CO'] = datetime.datetime.timestamp(datetime.datetime.now())
                    save_notify_data(n_db)
                    send_co_notification()
        else :
            raise Exception("Invalid CO level.")
        return jsonify({'status': 1})

    except Exception as e:
        return jsonify({"status": str(e)}), 422

@app.route('/vehicle', methods=['POST'])
@check_for_token
def get_cars():
    try:
        content = request.json
        email = content[config.KEY_EMAIL]
        car_data = read_car_data_db()
        cars = []
        for car in car_data:
            if car.split(config.KEY_GUEST_CONJUSCTION)[0] == email:
                cars.append(car_data[car])
        return jsonify(cars)
    except Exception as e:
        return jsonify({'status': str(e)})

@app.route('/add_vehicle', methods=['POST'])
@check_for_token
def add_vehicle():
    try:
        content = request.json
        email = content[config.KEY_EMAIL]
        car_id = content[config.KEY_CAR_ID]
        milage = content[config.KEY_MILAGE]
        ls_date = content[config.KEY_LAST_SERVICE_DATE]
        ls_milage = content[config.KEY_LAST_SERVICE_MILAGE]
        oilType = content[config.KEY_OIL_TYPE]
        tiers = content[config.KEY_TYERS]
        air_filter = content[config.KEY_AIR_FILTER]
        brake_oil = content[config.KEY_BRAKE_OIL]

        car_id_key = email + config.KEY_GUEST_CONJUSCTION + car_id

        lastest_update = datetime.date.today().strftime("%d-%m-%Y")

        car_data = read_car_data_db()

        if car_id_key not in car_data.keys():
            car_data[car_id_key] = {
                config.KEY_CAR_ID : car_id,
                config.KEY_MILAGE : milage,
                config.KEY_LAST_SERVICE_DATE : ls_date,
                config.KEY_LAST_SERVICE_MILAGE : ls_milage,
                config.KEY_OIL_TYPE: oilType,
                config.KEY_TYERS : tiers,
                config.KEY_AIR_FILTER: air_filter,
                config.KEY_BRAKE_OIL: brake_oil,
                config.KEY_LAST_UPDATE: lastest_update,
                }
            save_car_data(car_data)
            return jsonify({"status": 1})
        else:
            raise Exception("Unable to add new vehicle, try again later." + str(car_id))
    except Exception as e:
        return jsonify({"status": str(e)}), 422

@app.route('/update_tiers', methods=['POST'])
@check_for_token
def update_tiers():
    try:
        content = request.json
        email = content[config.KEY_EMAIL]
        car_id = content[config.KEY_CAR_ID]
        tiers = content[config.KEY_TYERS]
        car_id = email + config.KEY_GUEST_CONJUSCTION + car_id
        car_db = read_car_data_db()
        if car_id not in car_db.keys():
            # Vehicle not present
            raise Exception("The Vehicle ID provided is not valid.")
        else :
            car_db[car_id][config.KEY_TYERS] = tiers
            save_car_data(car_db)
            return jsonify({"status": 1})
    except Exception as e:
        return jsonify({"status": str(e)}), 422

@app.route('/update_milage', methods=['POST'])
@check_for_token
def update_milag():
    try:
        content = request.json
        email = content[config.KEY_EMAIL]
        car_id = content[config.KEY_CAR_ID]
        milage = content[config.KEY_MILAGE]
        car_id = email + config.KEY_GUEST_CONJUSCTION + car_id
        lastest_update = datetime.date.today().strftime("%d-%m-%Y")
        car_db = read_car_data_db()
        if car_id not in car_db.keys():
            # Vehicle not present
            raise Exception("The Vehicle ID provided is not valid.")
        else :
            if (car_db[car_id][config.KEY_MILAGE] <= milage) :
                car_db[car_id][config.KEY_MILAGE] = milage
                car_db[car_id][config.KEY_LAST_UPDATE] = lastest_update
                save_car_data(car_db)
                return jsonify({"status": 1})
            else:
                raise Exception("The Odometer reading (milage) is in valid.")
    except Exception as e:
        return jsonify({"status": str(e)}), 422

@app.route('/update_engine', methods=['POST'])
@check_for_token
def update_engine():
    try:
        content = request.json
        email = content[config.KEY_EMAIL]
        car_id = content[config.KEY_CAR_ID]
        milage = content[config.KEY_LAST_SERVICE_MILAGE]
        oilType = content[config.KEY_OIL_TYPE]
        car_id = email + config.KEY_GUEST_CONJUSCTION + car_id
        car_db = read_car_data_db()
        if car_id not in car_db.keys():
            # Vehicle not present
            raise Exception("The Vehicle ID provided is not valid.")
        else :
            if (car_db[car_id][config.KEY_LAST_SERVICE_MILAGE] <= milage) :
                car_db[car_id][config.KEY_LAST_SERVICE_MILAGE] = milage
                car_db[car_id][config.KEY_OIL_TYPE] = oilType
                if (milage > car_db[car_id][config.KEY_MILAGE]) :
                    car_db[car_id][config.KEY_MILAGE] = milage
                    lastest_update = datetime.date.today().strftime("%d-%m-%Y")
                    car_db[car_id][config.KEY_LAST_UPDATE] = lastest_update
                save_car_data(car_db)
                return jsonify({"status": 1})
            else:
                raise Exception("The Odometer reading (milage) is in valid.")
    except Exception as e:
        return jsonify({"status": str(e)}), 422

@app.route('/update_brake', methods=['POST'])
@check_for_token
def update_brake():
    try:
        content = request.json
        email = content[config.KEY_EMAIL]
        car_id = content[config.KEY_CAR_ID]
        milage = content[config.KEY_BRAKE_OIL]
        car_id = email + config.KEY_GUEST_CONJUSCTION + car_id
        car_db = read_car_data_db()
        if car_id not in car_db.keys():
            # Vehicle not present
            raise Exception("The Vehicle ID provided is not valid.")
        else :
            if (car_db[car_id][config.KEY_BRAKE_OIL] <= milage) :
                car_db[car_id][config.KEY_BRAKE_OIL] = milage
                if (milage > car_db[car_id][config.KEY_MILAGE]) :
                    car_db[car_id][config.KEY_MILAGE] = milage
                    car_db[car_id][config.KEY_LAST_SERVICE_MILAGE] = milage - 100
                    lastest_update = datetime.date.today().strftime("%d-%m-%Y")
                    car_db[car_id][config.KEY_LAST_UPDATE] = lastest_update
                save_car_data(car_db)
                return jsonify({"status": 1})
            else:
                raise Exception("The Odometer reading (milage) is in valid.")
    except Exception as e:
        return jsonify({"status": str(e)}), 422

@app.route('/update_air', methods=['POST'])
@check_for_token
def update_air():
    try:
        content = request.json
        email = content[config.KEY_EMAIL]
        car_id = content[config.KEY_CAR_ID]
        milage = content[config.KEY_AIR_FILTER]
        car_id = email + config.KEY_GUEST_CONJUSCTION + car_id
        car_db = read_car_data_db()
        if car_id not in car_db.keys():
            # Vehicle not present
            raise Exception("The Vehicle ID provided is not valid.")
        else :
            if (car_db[car_id][config.KEY_AIR_FILTER] <= milage) :
                car_db[car_id][config.KEY_AIR_FILTER] = milage
                if (milage > car_db[car_id][config.KEY_MILAGE]) :
                    car_db[car_id][config.KEY_MILAGE] = milage
                    car_db[car_id][config.KEY_LAST_SERVICE_MILAGE] = milage - 100
                    lastest_update = datetime.date.today().strftime("%d-%m-%Y")
                    car_db[car_id][config.KEY_LAST_UPDATE] = lastest_update
                save_car_data(car_db)
                return jsonify({"status": 1})
            else:
                raise Exception("The Odometer reading (milage) is in valid.")
    except Exception as e:
        return jsonify({"status": str(e)}), 422


@app.route('/remove_vehicle', methods=['POST'])
@check_for_token
def remove_vehicle():
    try:
        content = request.json
        email = content[config.KEY_EMAIL]
        car_id = content[config.KEY_CAR_ID]
        car_id = email + config.KEY_GUEST_CONJUSCTION + car_id
        car_db = read_car_data_db()
        if car_id not in car_db.keys():
            # Vehicle not present
            raise Exception("The Vehicle ID provided is not valid.")
        else :
            del car_db[car_id]
            save_car_data(car_db)
            return jsonify({"status": 1})
    except Exception as e:
        return jsonify({"status": str(e)}), 422


@app.route('/notify_poor_health', methods=['POST'])
@check_for_token
def send_poor_health_notification():
    try:
        content = request.json
        car_ID = content[config.KEY_CAR_ID]
        email = car_ID.split(config.KEY_GUEST_CONJUSCTION)[0]
        carID = car_ID.split(config.KEY_GUEST_CONJUSCTION)[1]
        health = content[config.KEY_HEALTH]
        component = content[config.KEY_COMPONENT]
        url = 'https://onesignal.com/api/v1/notifications'
        headers = {'Content-type': 'application/json', 'Authorization': "Basic YTA3NDk3NDUtNjE0OC00ZjNiLTkxNDgtNTQ4MTU5MDRiYzVj"}
        body = json.dumps({
        "app_id":"b22e4e51-0fdf-4c75-9d95-f023e9c32c74",
        "included_segments":["Subscribed Users"],
        "priority": 10,
        "headings": {"en":"Poor " + component + " Health"},
        "contents": {"en": "You vehicle " + carID + "'s "+ component + " health levels are below the standard threshold. Changing the " + component + " is highly recommended within the upcoming weeks."},
        "data": {
               "CarID": carID,
               "Mode": health
         },
        })
        req = requests.post(url, data=body, headers=headers)
        return jsonify({"status": req.text})
    except Exception as e:
        return jsonify({"status": str(e)}), 422

@app.route('/notify_tiers', methods=['POST'])
@check_for_token
def send_tiers_notification():
    try:
        content = request.json
        carID = content[config.KEY_CAR_ID]
        vehcile = carID.split(config.KEY_GUEST_CONJUSCTION)[1]
        tiers = content[config.KEY_TYERS]
        msg = ""
        if tiers == "Winter":
            msg = "Winter is coming!! Changing you " + vehcile + "'s Tiers to winter set is recommended."
        elif tiers == "Summer":
            msg = "Summer is coming!! Changing you " + vehcile + "'s Tiers to summer set is recommended."
        else :
            msg = "Great to hear that you are using All season Tiers set for " + vehcile + ", But changing to " + tiers + " set is highly recommended."
        url = 'https://onesignal.com/api/v1/notifications'
        headers = {'Content-type': 'application/json', 'Authorization': "Basic YTA3NDk3NDUtNjE0OC00ZjNiLTkxNDgtNTQ4MTU5MDRiYzVj"}
        body = json.dumps({
        "app_id":"b22e4e51-0fdf-4c75-9d95-f023e9c32c74",
        "included_segments":["Subscribed Users"],
        "priority": 10,
        "headings": {"en":"Tiers Change recommended"},
        "contents": {"en": msg},
        "data": {
               "CarID": carID,
               "Mode": tiers
         },
        })
        req = requests.post(url, data=body, headers=headers)
        return jsonify({"status": req.text})
    except Exception as e:
        return jsonify({"status": str(e)})

@app.route('/notify_co', methods=['POST'])
@check_for_token
def send_co_notification():
    try:
        content = request.json
        url = 'https://onesignal.com/api/v1/notifications'
        headers = {'Content-type': 'application/json', 'Authorization': "Basic YTA3NDk3NDUtNjE0OC00ZjNiLTkxNDgtNTQ4MTU5MDRiYzVj"}
        body = json.dumps({
        "app_id":"b22e4e51-0fdf-4c75-9d95-f023e9c32c74",
        "included_segments":["Subscribed Users"],
        "priority": 10,
        "headings": {"en":"Emergency - CO Level Too High"},
        "contents": {"en": "The CO Level inside your garage are above normal. Please, try not to enter the garage untill the garage is properly vented."},
        "data": {
               "CarID": "None",
               "Mode": "CO"
         },
        })
        req = requests.post(url, data=body, headers=headers)
        return jsonify({"status": req.text})
    except Exception as e:
        return jsonify({"status": str(e)})

if __name__ == "__main__":
    print("Reading values")
    app.run()
