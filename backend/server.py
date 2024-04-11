from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import sys
import os
sys.path.append('../')
from DatabaseManager import dbManager

# If the DATABASE_URL environment variable is set, it uses the test_API.py database
# If not set, it uses the main database
db = dbManager.DBManager(os.getenv('DATABASE_URL', "../DatabaseManager/RecallDatabase.db"))

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
    try:
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
    except Exception as e:
        return jsonify({"error": "Unknown", "details": e}), 500

# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    """Access the identity of the current user with get_jwt_identity"""
    try:
        current_user = get_jwt_identity()
        return jsonify(logged_in_as=current_user), 200
    except Exception as e:
        return jsonify({"error": "Unknown", "details": e}), 500
    
############################################
#         Sign up API Endpoint             #
############################################
@app.route("/signup", methods=['POST'])
def signup():
    try:
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
    except Exception as e:
        return jsonify({"error": "Unknown", "details": e}), 500

############################################
#         Subscriber API Endpoints         #
############################################
@app.route("/fetchSubbedStates", methods=['POST'])
def subbedStates():
    try:
        # Extract user details from the request
        user_details = request.json
        SUB_ID = user_details.get("subscriber_id")
        
        # Check if any required detail is missing
        if not all([SUB_ID]):
            return jsonify({"error": "Missing user details"}), 400
        
        result = db.get_subscriber_states(SUB_ID)
        return jsonify({"statelist": result, "message": "Fetch successful"}), 200
    except Exception as e:
        print(e)

@app.route("/subscribe", methods=['POST'])
def subscribe():
    try:
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
        elif result == 3:
            return jsonify({"error": message}), 404  # Subscriber not found
        else:
            return jsonify({"error": message}), 500  # Unexpected error
    except Exception as e:
        return jsonify({"error": "Unknown", "details": e}), 500
    
@app.route("/unsubscribe", methods=['POST'])
def unsubscribe():
    try:
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
    except Exception as e:
          return jsonify({"error": "Unknown", "details":e}), 500


@app.route("/subscription_details", methods=["POST"])
def subscription_details():
    try:
        # Insert subscriber details from the request
        recall_details = request.json
        subscriber_id = recall_details.get("subscriber_id")

        # Call get_subscription_recalls information
        recalls = db.get_subscription_recalls(subscriber_id)

        # Return response based on the result
        if recalls:
            print(jsonify({"recalls": recalls}), 200)
            return jsonify({"recalls": recalls}), 200
        else:
            return jsonify({"message": "Subscriber ID was not found"}), 404
    except Exception as e:
        return jsonify({"error": "Unknown", "details": "Unknown"}), 500

############################################
#         Admin API Endpoints         #
############################################

@app.route("/view/recall", methods=["GET"])
def view_recall():
    try:
        recall_num = request.json.get("recall_num")

        result, message = db.view_recall(recall_num)

        if result == 0:
            return jsonify({"message": "Recall added successfully"}), 200
        elif result == 1:
            return jsonify({"error": "Integrity Error", "details": message}), 400
        elif result == 2:
            return jsonify({"error": "Unexpected Error", "details": message}), 500
    except Exception as e:
          return jsonify({"error": "Unknown", "details": e}), 500


@app.route("/edit/recall", methods=["POST"])
def edit_recall():
    try:
        recall_details = request.json
        current_admin_id = recall_details.get("admin_id")
        recall_number = recall_details.get("recall_num")
        recall_update = recall_details.get("updates")

        result, message = db.edit_recall(current_admin_id, recall_number, recall_update)

        if result == 0:
            return jsonify({"message": "Recall updated successfully"}), 200
        elif result == 1:
            return jsonify({"error": "Integrity Error", "details": message}), 400
        elif result == 2:
            return jsonify({"error": "Unexpected Error", "details": message}), 500
    except Exception as e:
          return jsonify({"error": "Unknown", "details": e}), 500

@app.route("/setAffectedStates", methods=["POST"])
def set_states():
    try:
        recall_details = request.json
        current_admin_id = recall_details.get("admin_id")
        recall_number = recall_details.get("recall_num")
        state_number = recall_number.get("state_num")

        result, message = db.set_affected_states(current_admin_id, recall_number, state_number)

        if result == 0:
            return jsonify({"message": "Recall added successfully"}), 200
        elif result == 1:
            return jsonify({"error": "Integrity Error", "details": message}), 400
        elif result == 2:
            return jsonify({"error": "Unexpected Error", "details": message}), 500
    except Exception as e:
          return jsonify({"error": "Unknown", "details": e}), 500
        
        
@app.route("/recalls", methods=["GET"])
def get_recalls():
        try:
            result, message = db.view_all_recalls()
            if result == 1:
                return jsonify({"error": "Not Found", "details": message}), 404
            else:
                return jsonify({"message": "Success", "details": message}), 200
        except Exception as e:
            return jsonify({"error": "Unknown", "details": e}), 500
        
@app.route("/recall_edit", methods=["POST"])
def get_recall_edit_history():
      try:
        recall_details = request.json
        recall_number = recall_details.get("recall_num")
        result, message = db.view_recall_edit_history(recall_number)
        if result == 1:
            return jsonify({"error": "Not Found", "details": message}), 404
        else:
            return jsonify({"message": "Success", "details": message}), 200
      except Exception as e:
          return jsonify({"error": "Unknown", "details": e}), 500
        
@app.route("/companyRecalls", methods=["GET"])
def get_company_rankings():
      try:
        result, message = db.view_company_rankings()
        if result == 1:
            return jsonify({"error": "Not Found", "details": message}), 404
        elif result == 0:
            return jsonify({"message": "Success", "details": message}), 200
      except Exception as e:
          return jsonify({"error": "Unknown", "details": e}), 500
      
@app.route("/add", methods=["POST"])
def add_recall():
    try:
        recall_details = request.json
        recall_number = recall_details.get("recall_num") 
        
        add_recall_payload = (
            recall_number,
            recall_details["product_name"],  
            recall_details.get("category"),
            recall_details.get("closeDate"),
            recall_details.get("qty"),
            recall_details.get("class"),
            recall_details.get("reason"),
            recall_details.get("year"),
            recall_details.get("risklevel"),
            recall_details.get("openDate"),
            recall_details.get("type"),
            recall_details.get("companyID"),
        )
        
        print(request.json)
        
        states = recall_details.get("states", [])  # Provide a default empty list if not found
        admin_id = recall_details.get("admin_id")
        
        result, message = db.add_recall(admin_id, states, add_recall_payload)
        
        if result == 1:
            return jsonify({"error": "Not Found", "details": message}), 404
        elif result == 0:
            return jsonify({"message": "Success", "details": message}), 200
        
    except Exception as e:
        return jsonify({"error": "Unknown", "details": str(e)}), 500


@app.route("/edit", methods=["POST"])
def update_recall():
    try:
        recall_details = request.json
        recall_number = recall_details.get("recall_num")  
        
        # Ensure all fields are correctly accessed
        edit_recall_payload = (
            recall_details["product_name"],  # Direct access, assuming "product_name" is mandatory
            recall_details.get("category"),
            recall_details.get("closeDate"),
            recall_details.get("qty"),
            recall_details.get("class"),
            recall_details.get("reason"),
            recall_details.get("year"),
            recall_details.get("risklevel"),
            recall_details.get("openDate"),
            recall_details.get("type"),
            recall_details.get("companyID"),
        )
        
        print(request.json)
        
        states = recall_details.get("states", [])  # Provide a default empty list if not found
        admin_id = recall_details.get("admin_id")
        
        result, message = db.edit_recall(admin_id,recall_number, states, edit_recall_payload)
        
        if result == 1:
            return jsonify({"error": "Not Found", "details": message}), 404
        elif result == 0:
            return jsonify({"message": "Success", "details": message}), 200
        else:
            print("hello")
    except Exception as e:
        return jsonify({"error": "Unknown", "details": str(e)}), 500
    
@app.route("/editHistory", methods=["POST"])
def get_recall_history():
    try:
        recall_details = request.json
        recall_number = recall_details.get("recall_num") 
     
        result, message = db.view_recall_edit_history(recall_number)
        print(message)
        
        if result == 1:
            return jsonify({"error": "Not Found", "details": message}), 404
        elif result == 0:
            return jsonify({"message": "Success", "details": message}), 200
    except Exception as e:
        return jsonify({"error": "Unknown", "details": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
