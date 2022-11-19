from flask import Flask, jsonify, request
from functools import wraps
from utilities import *
import datetime
import jwt

app = Flask(__name__)
app.config['SECRET_KEY'] = "ASEREMOTECONTROLLERsmartgarage"
app.config['ALGO'] = "HS256"

def check_for_token(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'message': 'Missing token'}), 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], app.config['ALGO'])
        except Exception as e:
            return jsonify({'messgae': 'Invalid token - ' + str(e)}), 403
        return func(*args, **kwargs)
    return wrapped

@app.route('/login', methods = ['POST'])
def login():
    content = request.json
    username = content["username"]
    password = content["password"]

    user_data = read_user_data_db()
    users = user_data['username']
    pswd = user_data['password']
    token = jwt.encode({
        'user': users,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60)
        },
        app.config['SECRET_KEY'],
        algorithm= app.config['ALGO']
    )
    return jsonify({'user':username , 'pswd': password, 'token': token})

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    try:
        content = request.json
        username = content["username"]
        password = content["password"]
        first = content["first_name"]
        last = content["last_name"]
        email = content["email_id"]

        user_data = read_user_data_db()
        user_data = save_new_user(first, last, email, username, password, user_data)
        print(user_data)

        if user_data == []:
            return jsonify({"status": 0})
        else:

            return jsonify({"status": 1})
    except:
        return jsonify({"status": 0})


@app.route('/get_garage_data', methods=['GET', 'POST'])
@check_for_token
def get_garage_data():
    try:
        content = request.json
        item = content['item']
        garage_data = read_garage_data_db()

        if item != 'all':
            print(item, garage_data[item])
            return jsonify({'status':1, item: garage_data[item]})
        else:
            print(garage_data)
            return jsonify({'status':1, 'data':garage_data})
            #return garage_data
    except:
        return jsonify({"status": 0})


@app.route('/door', methods=['GET'])
@check_for_token
def get_door():
    garage_data = read_garage_data_db()
    door = garage_data['door']
    return jsonify({'door': door})

@app.route('/', methods=['GET'])
@check_for_token
def check_valid():
    return jsonify({'valid': 1})

@app.route('/door', methods=['POST'])
@check_for_token
def set_door():
    try:
        content = request.json
        cmd = content['command']
        garage_data = read_garage_data_db()
        if cmd == 'OPEN':
            value = 1
        elif cmd == 'CLOSE':
            value = -1
        else:
            value = 0
        garage_data['door'] = value

        with open('garage_db.json', 'w') as f:
            json.dump(garage_data, f)

        return jsonify({'status': 1})

    except:
        return jsonify({"status": 0})



@app.route('/light', methods=['GET'])
@check_for_token
def get_lights():
    garage_data = read_garage_data_db()
    return jsonify(garage_data['Light'])


@app.route('/light', methods=['POST'])
@check_for_token
def set_light():
    try:
        content = request.json
        light = content['Light']
        value = content['Value']
        garage_data = read_garage_data_db()

        garage_data['Light'][light] = value

        with open('garage_db.json', 'w') as f:
            json.dump(garage_data, f)

        return jsonify({'status': 1})

    except:
        return jsonify({"status": 0})

@app.route('/test', methods=['GET'])
@check_for_token
def get_test():
    return "test 3"

@app.route('/co', methods=['GET'])
@check_for_token
def get_co():
    co_data = read_co_data_db()
    return jsonify(co_data)

@app.route('/co', methods=['POST'])
@check_for_token
def set_co():
    try:
        content = request.json
        value = content['value']
        co_data = read_co_data_db()
        co_data['CO'] = value

        with open('co_db.json', 'w') as f:
            json.dump(co_data, f)

        return jsonify({'status': 1})

    except:
        return jsonify({"status": 0})



if __name__ == "__main__":
    app.run()
