import json

def create_user_db():
    user= 'admin'
    pswd = 'admin'
    f_name = ' '
    l_name = ' '
    email = 'admin@gmail.com'
    
    user_data = {'username': [user, ], 'password': [pswd,], 'first_name': [f_name, ], 'last_name':[l_name,], 'email_id':[email, ]}

    return user_data

def create_garage_db():
    garage_data = {
        'door':-1,
        'Light':{
        'Light_Ext':0,
        'Light_R':0,
        'Light_L':0,
        'Light_M':0}
        }
    return garage_data


def create_co_db():
    co_data = {'CO': 0}
    return co_data

if __name__ == '__main__':
    user_data = create_user_db()
    garage_data = create_garage_db()
    co_data = create_co_db()
    #print (user_data, garage_data)
    
    user_data['username'].append('guest')
    user_data['password'].append('password')
    user_data['first_name'].append('Jaskaran')
    user_data['last_name'].append('Singh')
    user_data['email_id'].append('jaskaransingh@gmail.com')
    
    
    #print(user_data)
    with open('login_db.json', 'w') as f:
        json.dump(user_data, f)
    
    with open('garage_db.json', 'w') as f:
        json.dump(garage_data, f)

    with open('co_db.json', 'w') as f:
        json.dump(co_data, f)    

