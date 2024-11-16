from flask import Flask, request, jsonify
import hashlib

app = Flask(__name__)


hash_db = {}


users_db = {}



@app.route('/gethash', methods=['GET'])
def get_hash():
    data = request.args.get('data', '')
    if not data:
        return jsonify({'error': 'No data provided'}), 400


    hash_value = hashlib.sha256(data.encode()).hexdigest()

    return jsonify({'hash': hash_value})



@app.route('/sethash', methods=['POST'])
def set_hash():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    
    password_hash = hashlib.sha256(password.encode()).hexdigest()


    users_db[username] = password_hash

    return jsonify({'message': 'Hash saved successfully'})


@app.route('/login', methods=['GET'])
def login():
    username = request.args.get('username')
    password = request.args.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400


    password_hash = hashlib.sha256(password.encode()).hexdigest()


    if users_db.get(username) == password_hash:
        return jsonify({'message': 'Login successful'})
    else:
        return jsonify({'error': 'Invalid username or password'}), 401



@app.route('/register', methods=['GET'])
def register():
    username = request.args.get('username')
    password = request.args.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400


    password_hash = hashlib.sha256(password.encode()).hexdigest()

    if username in users_db:
        return jsonify({'error': 'Username already exists'}), 409


    users_db[username] = password_hash
    return jsonify({'message': 'User registered successfully'})


if __name__ == '__main__':
    app.run(debug=True)
