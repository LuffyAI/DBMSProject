from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
import sys
sys.path.append('../')
from DatabaseManager import dbManager
db = dbManager.DBManager("../DatabaseManager/RecallDatabase.db")
app = Flask(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, id):
        self.id = id
        
@login_manager.user_loader
def user_loader(user_id):
    # This function is required for loading the user from the session
    # Adapt this to your method of retrieving a user by their ID
    return User(user_id)


@app.route("/login", methods=['POST'])
def login():
    # Extract username and password from request
    data = request.get_json()
    email = data.get("username")
    password = data.get("password")
    print(email)
    print(password)
    result, message = db.handle_signin(email, password)
    print(message)
    
    if result == 0:
        # Subscriber
        return jsonify({"success": True, "name": "Subscriber", "message": message}), 200
    elif result == 1:
        # Admin
        return jsonify({"success": True, "name": "Admin", "message": message}), 200
    elif result == 2:
        # User does not exist
        return jsonify({"success": False, "message": "User does not exist!"}), 404
    else:
        # Unexpected error
        return jsonify({"success": False, "message": "Unexpected error occurred!"}), 500

@app.route("/signup", methods=['POST'])
def signup():
    # Extract user details from the request
    user_details = request.json
    name = user_details.get("name")
    password = user_details.get("password")
    phonenum = user_details.get("phonenum")
    email = user_details.get("email")
    
    # Check if any required detail is missing
    if not all([name, password, phonenum, email]):
        return jsonify({"error": "Missing user details"}), 400
    
    # Insert user into the USER table
    user_insertion_result = db.insert_user(name, password, phonenum, email)
    
    # Handle potential errors from inserting user
    if user_insertion_result[0] != 0:
        return jsonify({"error": user_insertion_result[1]}), 400
    
    # Insert user into the SUBSCRIBER table
    subscriber_insertion_result = db.insert_subscriber(email)
    
    # Handle potential errors from inserting subscriber
    if subscriber_insertion_result[0] != 0:
        return jsonify({"error": subscriber_insertion_result[1]}), 400
    
    # If everything went well
    return jsonify({"message": "Signup successful"}), 200
    
    
    
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({"success": True, "message": "Logged out successfully."})

@app.route('/protected')
@login_required
def protected():
    return jsonify({"message": "This is a protected route."})

if __name__=="__main__":
    app.run(debug=True)
