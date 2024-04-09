import unittest
import requests
import sys
sys.path.append('../')
from DatabaseManager.dbManager import DBManager
from setupDatabase import initDatabase as init
import subprocess
import os
import time
from requests.exceptions import JSONDecodeError

# Creates a new database for the API
db_path = "test_API.db"
sql_files = ['../sql/tables.sql', '../sql/triggers.sql', '../sql/insertions.sql']
init(db_path, sql_files)

# Set as an environment variable
os.environ['DATABASE_URL'] = db_path

# Turns on the Flask Web Server automatically to access the endpoints
python_executable = sys.executable
script_path = "../backend/server.py"
process = subprocess.Popen([python_executable, script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
time.sleep(3)


class TestAPIEndpoints(unittest.TestCase):
    BASE_URL = "http://localhost:5000"  # Update this if your API is hosted elsewhere


    def test_successful_login(self):
        """Tests the successful login payload"""
        url = f"{self.BASE_URL}/login"
        credentials = {
            "email": "Davvy@umich.edu",
            "password": "123"
        }
        response = requests.post(url, json=credentials)
        response_data = response.json()
        print(response_data)
        self.assertIn(response.status_code, [200, 201])
        self.assertIn("Token", response_data)
        self.assertEqual(response_data.get("ID"), 3, "The ID should be 3")

    def test_unsuccessful_login(self):
        """Tests the unsuccessful login payload"""
        url = f"{self.BASE_URL}/login"
        credentials = {
            "email": "123@umich.edu",
            "password": "123"
        }
        response = requests.post(url, json=credentials)
        self.assertEqual(response.status_code, 404)
        expected_message = "User does not exist!"
        self.assertEqual(response.json().get("message"), expected_message)

    def test_successful_signup(self):
        url = f"{self.BASE_URL}/signup"
        user_data = {
            "name": "Luis",
            "password": "321",
            "phonenum": "123-456-7890",
            "email": "luisjr@umich.com"
        }
        response = requests.post(url, json=user_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Signup successful", response.json()['message'])

    def test_unsuccessful_signup(self):
        url = f"{self.BASE_URL}/signup"
        user_data = {
            "name": "Luis",
            "password": "321",
            "phonenum": "",
            "email": "luisjr@umich.com"
        }
        response = requests.post(url, json=user_data)
        response_data = response.json()
        print(response_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Missing user details', response.json()['error'])

    def test_successful_subscribe(self):
        """Sends an existing user to subscribe to an existing state"""
        url = f"{self.BASE_URL}/subscribe"
        subscription_data = {
            "subscriber_id": 1,  # Assuming this ID exists in database
            "state_name": "California"
        }
        response = requests.post(url, json=subscription_data)
        response_data = response.json()
        print(response_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data.get('message'), 'Success', "Error message does not match 'Success'")

    def test_unsuccessful_subscribe_nonexistent_ID(self):
        """Sends a non-exsistent user to subscribe to a valid state"""
        url = f"{self.BASE_URL}/subscribe"
        subscription_data = {
            "subscriber_id": 100,  # Assuming this ID doesn't exist in database
            "state_name": "California"
        }
        response = requests.post(url, json=subscription_data)
        response_data = response.json()
        print(response_data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_data.get('error'), 'User not found', "Error message does not match 'User not found'")

    def test_successful_unsubscribe(self):
        url = f"{self.BASE_URL}/unsubscribe"
        subscription_data = {
            "subscriber_id": 1,
            "state_name": "California"
        }
        response = requests.post(url, json=subscription_data)
        response_data = response.json()
        print(response_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data.get('message'), 'Success', "Error message does not match 'Success'")

    def test_unsuccessful_subscription_details(self):
        url = f"{self.BASE_URL}/subscription_details"
        recall_data = {"subscriber_id": 100}
        response = requests.post(url, json=recall_data)
        
        self.assertEqual(response.status_code, 404, "Expected status code 404 for an unsuccessful request")

        try:
            # Attempt to parse the JSON response
            response_data = response.json()
            print(response_data)
            # If there is a JSON response, check if the message is correct
            self.assertEqual(response_data.get('message'), 'Subscriber ID was not found', "Error message does not match 'Subscriber ID was not found'")
        except JSONDecodeError:
            # If there is a JSON decode error, it means there's no JSON response body
            # You might choose to pass this as it's expected behavior for a 404 response in some cases
            # Or use self.fail("Expected JSON response not received") to explicitly fail the test if no JSON response is received
            pass

    def test_successful_subscription_details(self):
        url = f"{self.BASE_URL}/subscription_details"
        recall_data = {
            "subscriber_id": 1
        }
        
        response = requests.post(url, json=recall_data)
        response_data = response.json()
        print(response_data)
        self.assertEqual(response.status_code, 200)

        # Adjust your expected output to match the exact structure of the response_data['recalls']
        expected_output = [{'Category': 'Not Heat Treated - Shelf Stable', 
                            'Class': 'Class 1', 
                            'CloseDate': '2024-03-01', 
                            'CompanyID': 6, 
                            'CompanyTitle': 'Director FSQA &amp; Regulatory Affairs', 
                            'OpenDate': '2024-02-01', 
                            'ProductName': '1-lb. plastic tubs labeled as &quot;Sysco Classic Chicken Flavored Base&quot; with lot code 02673 and packaged in a case labeled as &quot;Sysco Classic BEEF BASE CF&quot; with lot code 02673 represented on the label.', 
                            'Qty': 200, 
                            'Reason': 'Unreported Allergens', 
                            'RecallNum': '003-2024', 
                            'RiskLevel': 'Class I', 
                            'StateName': 'California', 
                            'Type': 'Closed Recall', 
                            'Year': '2024'}, 
                           {'Category': 'Heat Treated - Shelf Stable', 
                            'Class': 'Public Health Alert', 
                            'CloseDate': '', 
                            'CompanyID': 7, 
                            'CompanyTitle': 'Pruski’s Market', 
                            'OpenDate': '2023-11-17', 
                            'ProductName': '• 1.75-oz., 2.75-oz., and 8-oz. packages containing “Pruski’s Market Spicy Beef Jerky”  and a “SELL BY” date ranging from 03/21/24 through 05/09/24 represented on the  back of the packages., • 1.75-oz., 2.75-oz., and 8-oz. packages containing “Pruski’s Market Beef Jerky” and a  “SELL BY” date ranging from 03/21/24 through 05/09/24 represented on the back of  the packages., • 1.75-oz, 2.75-oz., and 8-oz. packages containing “Pruski’s Market Turkey Jerky” and a  “SELL BY” date ranging from 03/21/24 through 05/09/24 represented on the back of  the packages., • 3-oz. packages containing “HOOSER CUSTOM MEATS BEEF JERKY MESQUITE  SMOKED” and a “SELL BY” of 04/23/24 represented on the back of the packages., • Packages purchased by weight at the retail counter, containing “Beef Jerky Regular”,  “Spicy Beef Jerky”, or “Turkey Jerky” with Pack Date ranging from 9/21/23 through  11/9/23.', 
                            'Qty': 150, 
                            'Reason': 'Unreported Allergens', 
                            'RecallNum': 'PHA-11172023-01', 
                            'RiskLevel': 'Public Health Alert', 
                            'StateName': 'California', 
                            'Type': 'Public Health Alert', 
                            'Year': ''}]
        self.assertEqual(response_data.get('recalls'), expected_output)

    def test_unsuccessful_subscription_details(self):
        url = f"{self.BASE_URL}/subscription_details"
        recall_data = {
            "subscriber_id": 100
        }
        response = requests.post(url, json=recall_data)
        response_data = response.json()
        print(response_data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_data.get('message'), 'Subscriber ID was not found', "Error message does not match 'Subscriber ID was not found'")
        
    def test_getCompanyRankings(self):
        url = f"{self.BASE_URL}/companyRecalls"
        response = requests.get(url)
        response_data = response.json() 
        print(response_data)
        expected_output = [['FakeCompany', 1],
                           ['Taylor Farms’ Consumer Line', 1], 
                           ['Chief Operating Officer', 1], 
                           ['General Manager, Macgregors Meat &amp; Seafood Ltd', 1], 
                           ['Vice President of External Communications', 1], 
                           ['Director FSQA &amp; Regulatory Affairs', 1], 
                           ['Pruski’s Market', 1]]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data.get('details'), expected_output)

    def test_successful_add_recall(self):
        url = f"{self.BASE_URL}/add/recall"
        user_data = {
            "admin_id": 4
        }
        response = requests.post(url, json=user_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json())

    def test_unsuccessful_add_recall(self):
        url = f"{self.BASE_URL}/add/recall"
        user_data = {
            "admin_id": 100     # not in admin table
        }
        response = requests.post(url, json=user_data)
        print(response)
        self.assertEqual(response.status_code, 400)
        self.assertIn("message", response.json())

    def test_successful_view_recall(self):
        url = f"{self.BASE_URL}/view/recall"
        recall_data = {
            "recall_num": "004-2024"
        }
        response = requests.get(url, json=recall_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json())

    def test_unsuccessful_view_recall(self):
        url = f"{self.BASE_URL}/view/recall"
        recall_data = {
            "recall_num": "111-2015"    # not a valid recall num
        }
        response = requests.get(url, json=recall_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("message", response.json())


    def test_successful_edit_recall(self):
        url = f"{self.BASE_URL}/edit/recall"
        recall_data = {
            "admin_id": 4,
            "recall_num": "004-2024",
            # Replace ColumnName and NewValue with actual column name and new value from recall table
            "updates": {"RecallNum": "2"}
        }
        response = requests.post(url, json=recall_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json())

    def test_successful_set_affected_states(self):
        url = f"{self.BASE_URL}/setAffectedStates"
        recall_data = {
            "admin_id": 4,
            "recall_num": "004-2024",
            "state_num": 28
        }
        response = requests.post(url, json=recall_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json())
      
   


if __name__ == "__main__":
    unittest.main()
    # Unsets environment variable
    del os.environ['DATABASE_URL']
