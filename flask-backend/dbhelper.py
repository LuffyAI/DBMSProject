import sqlite3
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path

    def connect(self):
        """Establish a connection to the database."""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()

    def insert_user(self, name, password, phonenum, email):
        """Insert a new user into the USER table.
        
        Returns 0 on success, 1 on integrity error, 2 on unexpected error.
        """
        try:
            self.connect()
            self.cursor.execute("INSERT INTO USER (Name, Password, PhoneNum, Email) VALUES (?, ?, ?, ?)", 
                                (name, password, phonenum, email))
            self.conn.commit()
            return 0  # Success
        except sqlite3.IntegrityError:
            return 1  # User already exists
        except Exception as e:
            print(f"Unexpected error: {e}")
            return 2  # Unexpected error
        finally:
            self.close()

    def insert_subscriber(self, email):
        """Insert a user into the SUBSCRIBER table, checking if they exist and are not an admin.
        
        Returns 0 on success, 1 if user does not exist or is an admin, 2 on integrity error, 3 on unexpected error.
        """
        try:
            self.connect()
            # Check if the user exists and is not an admin
            self.cursor.execute("SELECT ID FROM USER WHERE Email = ? AND ID NOT IN (SELECT AdminID FROM ADMIN)", (email,))
            user_id = self.cursor.fetchone()
            if user_id:
                # Insert the user as a subscriber
                self.cursor.execute("INSERT INTO SUBSCRIBER (SubscriberID) VALUES (?)", (user_id[0],))
                self.conn.commit()
                return 0  # Success
            else:
                return 1  # User does not exist or is already an admin
        except sqlite3.IntegrityError:
            return 2  # SQL integrity error
        except Exception as e:
            print(f"Unexpected error: {e}")
            return 3  # Unexpected error
        finally:
            self.close()
            
    def sign_in_user(self, email, password):
        """Check if a user exists and determine their role.
        
        Returns a tuple:
        - First element: 0 (success), 1 (user not found), 2 (unexpected error)
        - Second element: 'admin', 'subscriber', or None (based on the user's role or failure)
        """
        try:
            self.connect()
            # Check if the user exists with the given email and password
            self.cursor.execute("SELECT ID FROM USER WHERE Email = ? AND Password = ?", (email, password))
            user = self.cursor.fetchone()
            if not user:
                return 1, None  # User not found

            user_id = user[0]
            # Check if the user is an admin
            self.cursor.execute("SELECT AdminID FROM ADMIN WHERE AdminID = ?", (user_id,))
            if self.cursor.fetchone():
                return 0, 'admin'  # User is an admin

            # Check if the user is a subscriber
            self.cursor.execute("SELECT SubscriberID FROM SUBSCRIBER WHERE SubscriberID = ?", (user_id,))
            if self.cursor.fetchone():
                return 0, 'subscriber'  # User is a subscriber

            return 0, None  # User exists but is neither an admin nor a subscriber
        except Exception as e:
            print(f"Unexpected error: {e}")
            return 2, None  # Unexpected error
        finally:
            self.close()
    def subscribe_to_state(self, user_id, state_name):
        """Allows a subscriber to subscribe to a state.
        
        Returns 0 on success, 1 if state not found, 2 if already subscribed, 3 for unexpected error.
        """
        try:
            self.connect()
            # Get state number
            self.cursor.execute("SELECT StateNum FROM STATE WHERE Name = ?", (state_name,))
            state_num = self.cursor.fetchone()
            if not state_num:
                return 1  # State not found

            # Check if already subscribed
            self.cursor.execute("SELECT * FROM IS_SUBSCRIBED WHERE SubscriberID = ? AND StateNum = ?", (user_id, state_num[0]))
            if self.cursor.fetchone():
                return 2  # Already subscribed

            # Subscribe the user to the state
            self.cursor.execute("INSERT INTO IS_SUBSCRIBED (SubscriberID, StateNum) VALUES (?, ?)", (user_id, state_num[0]))
            self.conn.commit()
            return 0  # Success
        except Exception as e:
            print(f"Unexpected error: {e}")
            return 3  # Unexpected error
        finally:
            self.close()

    def unsubscribe_from_state(self, user_id, state_name):
        """Allows a subscriber to unsubscribe from a state.
        
        Returns 0 on success, 1 if state not found, 2 if not subscribed, 3 for unexpected error.
        """
        try:
            self.connect()
            # Get state number
            self.cursor.execute("SELECT StateNum FROM STATE WHERE Name = ?", (state_name,))
            state_num = self.cursor.fetchone()
            print(state_num)
            if not state_num:
                return 1  # State not found

            # Check if not subscribed
            self.cursor.execute("SELECT * FROM IS_SUBSCRIBED WHERE SubscriberID = ? AND StateNum = ?", (user_id, state_num[0]))
            if not self.cursor.fetchone():
                return 2  # Not subscribed

            # Unsubscribe the user from the state
            self.cursor.execute("DELETE FROM IS_SUBSCRIBED WHERE SubscriberID = ? AND StateNum = ?", (user_id, state_num[0]))
            self.conn.commit()
            return 0  # Success
        except Exception as e:
            print(f"Unexpected error: {e}")
            return 3  # Unexpected error
        finally:
            self.close()
            
    def get_user_subscription_recalls(self, subscriber_id):
        """Fetch recall information for the states a user is subscribed to.
        
        Returns a list of dictionaries with recall details.
        """
        recalls = []
        try:
            self.connect()
            query = """
                SELECT S.Name AS StateName, R.RecallNum, R.ProductName, R.Category, 
                       R.CloseDate, R.Qty, R.Class, R.Reason, R.Year, R.RiskLevel, 
                       R.OpenDate, R.Type, C.ID AS CompanyID, C.Title AS CompanyTitle
                FROM IS_SUBSCRIBED ISUB
                JOIN STATE S ON ISUB.StateNum = S.StateNum
                JOIN AFFECTS A ON S.StateNum = A.StateNum
                JOIN RECALL R ON A.RecallNum = R.RecallNum
                JOIN COMPANY C ON R.CompanyID = C.ID
                WHERE ISUB.SubscriberID = ?
            """
            self.cursor.execute(query, (subscriber_id,))
            rows = self.cursor.fetchall()
            for row in rows:
                recalls.append({
                    "StateName": row[0],
                    "RecallNum": row[1],
                    "ProductName": row[2],
                    "Category": row[3],
                    "CloseDate": row[4],
                    "Qty": row[5],
                    "Class": row[6],
                    "Reason": row[7],
                    "Year": row[8],
                    "RiskLevel": row[9],
                    "OpenDate": row[10],
                    "Type": row[11],
                    "CompanyID": row[12],
                    "CompanyTitle": row[13]
                })
            return recalls
        except Exception as e:
            print(f"Unexpected error: {e}")
            return []  # Return an empty list in case of error
        finally:
            self.close()
            
    def add_recall(self, admin_id, recall_details):
        """
        Adds a new recall. Requires an existing company.
        recall_details is a dictionary containing all necessary recall information,
        including 'ProductName', 'Category', etc., and 'CompanyID'.
        """
        try:
            self.connect()
            # Check if company exists
            self.cursor.execute("SELECT ID FROM COMPANY WHERE ID = ?", (recall_details['CompanyID'],))
            if not self.cursor.fetchone():
                return "Company does not exist."

            columns = ', '.join(recall_details.keys())
            placeholders = ', '.join(['?'] * len(recall_details))
            query = f"INSERT INTO RECALL ({columns}) VALUES ({placeholders})"
            self.cursor.execute(query, tuple(recall_details.values()))
            
            # Log this action
            self.log_action(admin_id, recall_details['RecallNum'], datetime.now())
            
            self.conn.commit()
            return "Recall added successfully."
        except sqlite3.IntegrityError:
            return "Recall already exists."
        except Exception as e:
            print(f"Unexpected error: {e}")
            return "Failed to add recall."
        finally:
            self.close()
            
    def view_recall(self, recall_num):
        """
        Returns recall details for a given recall number.
        """
        try:
            self.connect()
            self.cursor.execute("SELECT * FROM RECALL WHERE RecallNum = ?", (recall_num,))
            recall = self.cursor.fetchone()
            if recall:
                return recall
            return "Recall not found."
        except Exception as e:
            print(f"Unexpected error: {e}")
            return "Failed to retrieve recall."
        finally:
            self.close()
            
    def edit_recall(self, admin_id, recall_num, updates):
        """
        Edits details for an existing recall. 'updates' is a dictionary of columns to update.
        """
        try:
            self.connect()
            update_clause = ', '.join([f"{k} = ?" for k in updates.keys()])
            query = f"UPDATE RECALL SET {update_clause} WHERE RecallNum = ?"
            self.cursor.execute(query, tuple(updates.values()) + (recall_num,))
            
            # Log this action
            self.log_action(admin_id, recall_num, datetime.now())
            
            self.conn.commit()
            return "Recall updated successfully."
        except Exception as e:
            print(f"Unexpected error: {e}")
            return "Failed to update recall."
        finally:
            self.close()
            
    def set_affected_states(self, admin_id, recall_num, state_nums):
        """
        Sets which states are affected by a given recall. 'state_nums' is a list of state numbers.
        """
        try:
            self.connect()
            # Clear existing states for this recall
            self.cursor.execute("DELETE FROM AFFECTS WHERE RecallNum = ?", (recall_num,))
            for state_num in state_nums:
                # Ensure state exists
                self.cursor.execute("SELECT StateNum FROM STATE WHERE StateNum = ?", (state_num,))
                if self.cursor.fetchone():
                    self.cursor.execute("INSERT INTO AFFECTS (StateNum, RecallNum) VALUES (?, ?)", (state_num, recall_num))
                else:
                    return f"State {state_num} does not exist."

            # Log this action
            self.log_action(admin_id, recall_num, datetime.now())
            
            self.conn.commit()
            return "Affected states updated successfully."
        except Exception as e:
            print(f"Unexpected error: {e}")
            return "Failed to update affected states."
        finally:
            self.close()
            
    def log_action(self, admin_id, recall_num, modification_date):
        """
        Logs or updates an action taken by an admin on a recall. If an action log exists, it updates the
        modification date; otherwise, it inserts a new log entry.
        """
        try:
            # Check if a log entry already exists
            self.cursor.execute("SELECT * FROM MANAGES WHERE ID = ? AND RecallNum = ?", (admin_id, recall_num))
            existing_log = self.cursor.fetchone()

            if existing_log:
                # Update the existing log entry with the new modification date
                self.cursor.execute("UPDATE MANAGES SET [Modification Date] = ? WHERE ID = ? AND RecallNum = ?", 
                                    (modification_date, admin_id, recall_num))
            else:
                # Insert a new log entry
                self.cursor.execute("INSERT INTO MANAGES (ID, RecallNum, [Modification Date]) VALUES (?, ?, ?)", 
                                    (admin_id, recall_num, modification_date))
        except Exception as e:
            print(f"Error logging action: {e}")


            
            

db_manager = DatabaseManager('RecallDb.db')
db_manager.connect()

# Test adding a recall
recall_details = {
    'RecallNum': '5558',
    'ProductName': 'Product 1',
    'Category': 'Egg Products',
    'CloseDate': '2023-12-31',
    'Qty': 100,
    'Class': 'Class 1',
    'Reason': 'Misbranding',
    'Year': '2023',
    'RiskLevel': 'High',
    'OpenDate': '2023-01-01',
    'Type': 'Active Recall',
    'CompanyID': 1
}

print(db_manager.add_recall(admin_id=3, recall_details=recall_details))
print(db_manager.view_recall('5558'))
updates = {'Qty': 200, 'RiskLevel': 'Medium'}
print(db_manager.edit_recall(admin_id=3, recall_num='5558', updates=updates))
print(db_manager.view_recall('5558'))
print(db_manager.set_affected_states(admin_id=3, recall_num='5558', state_nums=[31]))
db_manager.close()

