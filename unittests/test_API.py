import unittest
import requests

class TestAPIEndpoints(unittest.TestCase):
    BASE_URL = "http://localhost:5000"  # Update this if your API is hosted elsewhere


    def test_successful_login(self):
        url = f"{self.BASE_URL}/login"
        credentials = {
            "email": "Davvy@umich.edu",
            "password": "123"
        }
        response = requests.post(url, json=credentials)
        self.assertIn(response.status_code, [200, 201])
        self.assertIn("Token", response.json())

    def test_unsuccessful_login(self):
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
        self.assertEqual(response.status_code, 400)
        self.assertIn("Signup unsuccessful", response.json()['message'])

    def test_successful_subscribe(self):
        url = f"{self.BASE_URL}/subscribe"
        subscription_data = {
            "subscriber_id": 1,  # Assuming this ID exists in database
            "state_name": "California"
        }
        response = requests.post(url, json=subscription_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json())

    def test_unsuccessful_subscribe(self):
        url = f"{self.BASE_URL}/subscribe"
        subscription_data = {
            "subscriber_id": 100,  # Assuming this ID doesn't exist in database
            "state_name": "California"
        }
        response = requests.post(url, json=subscription_data)
        self.assertEqual(response.status_code, 409)
        self.assertIn("message", response.json())

    def test_successful_unsubscribe(self):
        url = f"{self.BASE_URL}/unsubscribe"
        subscription_data = {
            "subscriber_id": 1,
            "state_name": "California"
        }
        response = requests.post(url, json=subscription_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json())

    def test_unsuccessful_unsubscribe(self):
        url = f"{self.BASE_URL}/unsubscribe"
        subscription_data = {
            "subscriber_id": 100,
            "state_name": "California"
        }
        response = requests.post(url, json=subscription_data)
        self.assertEqual(response.status_code, 404)
        self.assertIn("message", response.json())

    def test_successful_subscription_details(self):
        url = f"{self.BASE_URL}/subscription/details"
        recall_data = {
            "subscriber_id": 1
        }
        response = requests.get(url, json=recall_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json())

    def test_unsuccessful_subscription_details(self):
        url = f"{self.BASE_URL}/subscription/details"
        recall_data = {
            "subscriber_id": 100
        }
        response = requests.get(url, json=recall_data)
        self.assertEqual(response.status_code, 404)
        self.assertIn("message", response.json())

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
        url = f"{self.BASE_URL}/set-affected-states"
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
