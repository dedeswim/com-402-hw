from flask import Flask, request
import bcrypt

app = Flask(__name__)

@app.route('/', methods=['POST'])
def bcrypt_hasher():
    
    data = request.get_json()
    username = data['user']
    password = data['pass']
    
    salt = bcrypt.gensalt()

    return bcrypt.hashpw(password.encode('utf-8'), salt)

if __name__ == "__main__":
    app.run()
