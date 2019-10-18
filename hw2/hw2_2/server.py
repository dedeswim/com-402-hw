from flask import Flask, request, make_response
from base64 import b64decode, b64encode
from collections import defaultdict
import hmac
import time
import os

app = Flask(__name__)

cookie_name = "LoginCookie"

new_random = lambda: os.urandom(20)

secret_dict = defaultdict(new_random)

def compute_hmac(username, timestamp, user_type, user_secret):

    user_secret = secret_dict[username]
    return hmac.new(user_secret, bytes(username + timestamp + user_type, 'utf-8')).hexdigest().upper()

def login_cookie_builder(username, timestamp, user_type):

    user_secret = secret_dict[username]

    hmac_ = compute_hmac(username, str(timestamp), user_type, user_secret)

    cookie = '{username},{timestamp},com402,hw2,ex3,{type},{hmac_}'.format(
            username=username, timestamp=str(timestamp), type=user_type, hmac_=hmac_
    )

    return b64encode(bytes(cookie, 'utf-8'))

@app.route("/login",methods=['POST'])
def login():

    username = request.form['username']
    password = request.form['password']

    if (not username) | (not password):
        return 'Invalid login data', 401

    timestamp = round(time.time())

    if username == 'admin' and password == '42':
        response = make_response('Welcome admin!')
        admin_type = 'admin'
        login_cookie = login_cookie_builder(username, timestamp, admin_type)
        response.set_cookie('LoginCookie', login_cookie)
        
        return response
    
    response = make_response('Welcome user!')
    admin_type = 'user'
    login_cookie = login_cookie_builder(username, timestamp, admin_type)
    response.set_cookie('LoginCookie', login_cookie)
    
    return response

@app.route("/auth",methods=['GET'])
def auth():

    login_cookie = b64decode(request.cookies.get('LoginCookie')).decode('utf-8')

    if not login_cookie:
        return 'No cookie here...', 403
    
    username_pos = 0
    timestamp_pos = 1
    type_pos = 5
    hmac_pos = 6

    cookie_array = login_cookie.split(',')

    try:
        username = cookie_array[username_pos]
        timestamp = cookie_array[timestamp_pos]
        user_type = cookie_array[type_pos]
        cookie_hmac = cookie_array[hmac_pos]
    except IndexError:
        return 'Tampered cookie', 403

    user_secret = secret_dict[username]
    expected_hmac = compute_hmac(username, timestamp, user_type, user_secret)

    if not hmac.compare_digest(expected_hmac, cookie_hmac):
        return 'Tampered cookie', 403

    if user_type == 'admin':
        return 'You are admin!', 200

    elif user_type == 'user':
        return 'You are user', 201

    else:
        return 'Tampered cookie', 403

if __name__ == '__main__':
    app.run()