from flask import Flask, request, jsonify
import hashlib

app = Flask(__name__)

# Store hashes in a dictionary (acting as a simple in-memory database)
hash_db = {}

# A simple in-memory "user database" to simulate login and registration
users_db = {}


# GET /gethash - Return the hash of a predefined input
@app.route('/gethash', methods=['GET'])
def get_hash():
    data = request.args.get('data', '')
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    # Hash the data using SHA-256
    hash_value = hashlib.sha256(data.encode()).hexdigest()

    return jsonify({'hash': hash_value})


# POST /sethash - Accept a POST request to save a hash for a user (simulating a "password hash")
@app.route('/sethash', methods=['POST'])
def set_hash():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    # Hash the password using SHA-256 (real applications should use stronger algorithms like bcrypt)
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    # Save the hash in our "users_db"
    users_db[username] = password_hash

    return jsonify({'message': 'Hash saved successfully'})


# GET /login - Simulate a login by checking the hash for a given user
@app.route('/login', methods=['GET'])
def login():
    username = request.args.get('username')
    password = request.args.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    # Hash the provided password
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    # Check if the hash matches the stored hash for the user
    if users_db.get(username) == password_hash:
        return jsonify({'message': 'Login successful'})
    else:
        return jsonify({'error': 'Invalid username or password'}), 401


# GET /register - Simulate a registration by saving a new user with their hashed password
@app.route('/register', methods=['GET'])
def register():
    username = request.args.get('username')
    password = request.args.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    # Hash the password before saving it
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    if username in users_db:
        return jsonify({'error': 'Username already exists'}), 409

    # Save the user with their hashed password
    users_db[username] = password_hash
    return jsonify({'message': 'User registered successfully'})


if __name__ == '__main__':
    app.run(debug=True)