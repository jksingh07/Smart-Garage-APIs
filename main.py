from flask import Flask, jsonify, request
from functools import wraps
from utilities import *
import datetime
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

@app.route('/', methods=['GET'])
@check_for_token
def check_valid():
    return jsonify({config.KEY_VALID: 1})


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

        login_db = read_user_data_db();
        chk = check_valid_user(email, password, login_db)

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

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    try:
        content = request.json
        email = content[config.KEY_EMAIL]
        password = content[config.KEY_PASSWORD]
        first = content[config.KEY_FIRST_N]
        last = content[config.KEY_LAST_N]
        role = "guest"

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
        return jsonify({config.KEY_DOOR: config.get_command_stat(garage_data[config.KEY_DOOR])})
    except Exception as e:
        return jsonify({'status': str(e)})

@app.route('/door', methods=['POST'])
@check_for_token
def set_door():
    try:
        garage_data = read_garage_data_db()
        content = request.json
        cmd = content[config.KEY_COMMAND]

        if cmd in config.KEY_DOOR_STAT:
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
        else :
            raise Exception("Invalid CO level.")
        return jsonify({'status': 1})

    except Exception as e:
        return jsonify({"status": str(e)}), 422


if __name__ == "__main__":
    print("Reading values")
    app.run()
