from flask import Flask, jsonify, request
from utilities import *

app = Flask(__name__)

@app.route('/login', methods = ['GET','POST'])
def login():
    content = request.json
    username = content["username"]
    password = content["password"]
    #print(email_id, password)

    user_data = read_user_data_db()
    users = user_data['username']
    pswd = user_data['password']

##    print(user_data)
##    print(username)
##    print(pswd, '\n', password)

    token = 0
    msg = ''

    if username in users:
        idx = users.index(username)
        if password == pswd[idx]:
            token = 1
            msg = "Success"
        else:
            token = 0
            msg = "Failed: Wrong Password !"
    else:
        token = -1
        msg = "User not found !"

    return jsonify({'token':token, 'msg': msg})

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
def get_garage_data():
    try:
        content = request.json
        item = content['item']
        garage_data = read_garage_data_db()

        #print(item)


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
def get_door():
    garage_data = read_garage_data_db()
    door = garage_data['door']
    return jsonify({'door': door})

@app.route('/door', methods=['POST'])
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
def get_lights():
    garage_data = read_garage_data_db()
    return jsonify(garage_data['Light'])


@app.route('/light', methods=['POST'])
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
def get_test():
    return "test 3"

@app.route('/co', methods=['GET'])
def get_co():
    co_data = read_co_data_db()
    return jsonify(co_data)

@app.route('/co', methods=['POST'])
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
