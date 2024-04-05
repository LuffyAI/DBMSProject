from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import sys
sys.path.append('../')
from DatabaseManager import dbManager
db = dbManager.DBManager("../DatabaseManager/RecallDatabase.db")

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your-secret-key'
jwt = JWTManager(app)
CORS(app)

############################################
#         Session State Mangement          #
############################################
# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    print(email,password)
    result, message, id = db.handle_signin(email, password)
    access_token = create_access_token(identity=email)
    print(access_token)
    
    if result == 0:
        # Subscriber
        return jsonify({"success": True, "role": "Subscriber", "ID": id,"email": email, "message": message, "Token": access_token}), 200
    elif result == 1:
        # Admin
        return jsonify({"success": True, "role": "Admin", "ID": id,"email": email, "message": message, "Token": access_token}), 201
    elif result == 2:
        # User does not exist
        return jsonify({"success": False, "message": "User does not exist!"}), 404
    else:
        # Unexpected error
        return jsonify({"success": False, "message": "Unexpected error occurred!"}), 500

# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    """Access the identity of the current user with get_jwt_identity"""
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

############################################
#         Sign up API Endpoint             #
############################################
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

############################################
#         Subscriber API Endpoints         #
############################################
@app.route("/fetchSubbedStates", methods=['POST'])
def subbedStates():
    # Extract user details from the request
    user_details = request.json
    SUB_ID = user_details.get("subscriber_id")
    
    # Check if any required detail is missing
    if not all([SUB_ID]):
        return jsonify({"error": "Missing user details"}), 400
    
    result = db.get_subscriber_states(SUB_ID)
    return jsonify({"statelist": result, "message": "Fetch successful"}), 200

@app.route("/subscribe", methods=['POST'])
def subscribe():
    # Extract subscription details from the request
    subscription_details = request.json
    subscriber_id = subscription_details.get("subscriber_id")
    state_name = subscription_details.get("state_name")
    
    # Check if any required detail is missing
    if not all([subscriber_id, state_name]):
        return jsonify({"error": "Missing subscription details"}), 400
    
    result, message = db.sub_to_state(subscriber_id, state_name)
    
    if result == 0:
        return jsonify({"message": message}), 200
    elif result == 1:
        return jsonify({"error": message}), 409  # Conflict, integrity error
    elif result == 2:
        return jsonify({"error": message}), 404  # State not found
    else:
        return jsonify({"error": message}), 500  # Unexpected error
    
@app.route("/unsubscribe", methods=['POST'])
def unsubscribe():
    # Extract unsubscription details from the request
    unsubscription_details = request.json
    subscriber_id = unsubscription_details.get("subscriber_id")
    state_name = unsubscription_details.get("state_name")
    
    # Check if any required detail is missing
    if not all([subscriber_id, state_name]):
        return jsonify({"error": "Missing unsubscription details"}), 400
    
    result, message = db.unsub_to_state(subscriber_id, state_name)
    
    if result == 0:
        return jsonify({"message": message}), 200
    elif result == 1:
        return jsonify({"error": message}), 409  # Conflict, integrity error
    elif result == 2:
        return jsonify({"error": message}), 404  # State not found
    elif result == 3:
        return jsonify({"error": message}), 404  # Subscriber not found
    else:
        return jsonify({"error": message}), 500  # Unexpected error


if __name__ == "__main__":
    app.run(debug=True)