import sqlite3
from datetime import datetime

class DBManager:
    def __init__(self, db_path):
        self.db_path = db_path
        
    def connect(self):
        """Connects to the specified database"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
        except Exception as e:
            print(f"Failed to connect to the database: {e}")
        
    def close(self):
        """Closes the connection to the database"""
        try:
            if self.conn:
                self.conn.close()
                self.conn = None
                self.cursor = None
        except Exception as e:
            print(f"Failed to close the database connection: {e}")
    
    def handle_signin(self, email, password):
        """Check if a user exists and determine their role.
         Returns a tuple of 0 on subscriber, 1 on admin, 2 if not exists, and 3 if unexpected error
        """
        try:
            self.connect()
            # Check if the user exists with the given email and password
            self.cursor.execute("SELECT ID FROM USER WHERE Email = ? AND Password = ?", (email, password))
            user = self.cursor.fetchone()
            
            user_id = user[0]
            # Check if the user is an admin
            self.cursor.execute("SELECT AdminID FROM ADMIN WHERE AdminID = ?", (user_id,))
            if self.cursor.fetchone():
                return (1, "Admin", user_id)  

            # Check if the user is a subscriber
            self.cursor.execute("SELECT SubscriberID FROM SUBSCRIBER WHERE SubscriberID = ?", (user_id,))
            if self.cursor.fetchone():
                return (0, 'Sub', user_id)  
            
            return (2, "User does not exist!", None)
                        
        except Exception as e:
            return (3, f"Unexpected Error: {e}")
        finally:
            self.close()
        
    def insert_user(self,name,password, phonenum,email):
        """Inserts a new user into the USER table.
        Returns a tuple of 0 on success, 1 on integrity error, 2 on unexpected error
        """
        try:
            self.connect()
            self.cursor.execute("INSERT INTO USER (Name, Password, PhoneNum, Email) VALUES (?, ?, ?, ?)", 
                                (name, password, phonenum, email))
            self.conn.commit()
            return (0, "Success")
        except sqlite3.IntegrityError as s:
            return (1, f"Integrity Error: {s}")
        except Exception as e:
            return (2, f"Unexpected Error: {e}")
        finally:
            self.close()
            
    def insert_subscriber(self,email):
        """Insert a user into the SUBSCRIBER table, checking if they exist and are not an admin.
        Returns 0 on success, 1 on integrity error, 2 on unexpected error, and 3 if user does not exist
        """
        try:
            self.connect()
            # Check if the user exists and is not an admin
            self.cursor.execute("SELECT ID FROM USER WHERE Email = ?", (email,))
            user_id = self.cursor.fetchone()
            if user_id:
                # Insert the user as a subscriber
                self.cursor.execute("INSERT INTO SUBSCRIBER (SubscriberID) VALUES (?)", (user_id[0],))
                self.conn.commit()
                return (0, "Success")  
            else:
                 return 3, "User does not exist!"
        except sqlite3.IntegrityError as s:
            return (1, f"Integrity Error: {s}")
        except Exception as e:
           return (2, f"Unexpected Error: {e}")
        finally:
            self.close()
            
    def sub_to_state(self, subscriber_id, state_name):
        """Allows a subscriber to subscribe to a state.
        Returns 0 on success, 1 on integrity error, 2 if state not found, and 3 for unexpected error.
        """
        try:
            self.connect()
            
            # Get state number
            self.cursor.execute("SELECT StateNum FROM STATE WHERE Name = ?", (state_name,))
            state_num = self.cursor.fetchone()
            
            if not state_num:
                return (2, "State not found")  
            
            # Subscribe the user to the state
            self.cursor.execute("INSERT INTO IS_SUBSCRIBED (SubscriberID, StateNum) VALUES (?, ?)", (subscriber_id, state_num[0]))
            self.conn.commit()
            return (0, "Success")  # Success
        
        except sqlite3.IntegrityError as s:
            return (1, f"Integrity Error: {s}")
        except Exception as e:
            return (3,f"Unexpected error: {e}")
        finally:
            self.close()
    
    def unsub_to_state(self, subscriber_id, state_name):
        """Allows a subscriber to unsubscribe from a state.
        Returns 0 on success, 1 on integrity error, 2 if state not found, 3 if subscriber not found, and 4 if unexpected error.
        """
        try:
            self.connect()
            
            # Get state number
            self.cursor.execute("SELECT StateNum FROM STATE WHERE Name = ?", (state_name,))
            state_num = self.cursor.fetchone()
            
            if not state_num:
                return (2, "State not found") 
            
            # Unsubscribe the user to the state
            self.cursor.execute("DELETE FROM IS_SUBSCRIBED WHERE SubscriberID = ? AND StateNum = ?", (subscriber_id, state_num[0]))
            self.conn.commit()
            return (0, "Success")  # Success
        
        except sqlite3.IntegrityError as s:
                return (1, f"Integrity Error: {s}")
            
        except Exception as e:
            return (3,f"Unexpected error: {e}")
        finally:
            self.close()
            
    def get_subscriber_states(self, subscriber_id):
        """Fetch the states a user is subscribed to.
          Returns a list of dictionaries with recall details.
        """
        states = []
        try:
            self.connect()
            query = """
               SELECT sub.StateNum, st.Name
               FROM IS_SUBSCRIBED sub
               JOIN STATE st ON sub.StateNum = st.StateNum
               WHERE sub.SubscriberID = ?
            """
            self.cursor.execute(query, (subscriber_id,))
            rows = self.cursor.fetchall()
            for row in rows:
                states.append({
                    "StateNum": row[0],
                    "StateName": row[1],
                })
            return states
        except Exception as e:
            print(f"Unexpected error: {e}")
            return []  # Return an empty list in case of error
        finally:
            self.close()
        
    def get_subscription_recalls(self, subscriber_id):
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
        
    ##ddd
    def add_recall(self, admin_id, recall_details):
        """
        Adds a recall record to the RECALL table.
        """
        try:
            self.connect()
            
            # Insert new recall entry
            self.cursor.execute(
                "INSERT INTO RECALL (RecallNum, ProductName, Category, CloseDate, Qty, Class, Reason, Year, RiskLevel, OpenDate, Type, CompanyID) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                recall_details)
            
            # Automatically log this action
            modification_date = datetime.now()
            edit_result = self.log_admin_edit_history(admin_id, recall_details[0], modification_date) 
            if edit_result[0] != 0:
                    return edit_result
            
            
            self.conn.commit()
            return (0, "Success")
        except sqlite3.IntegrityError as e:
            return (1, f"Integrity Error: {e}")
        except Exception as e:
            return (2, f"Unexpected Error: {e}")
        finally:
            self.close()

    def view_recall(self, recallnum):
        """
        Retrieves details of a specific recall by its number.
        """
        try:
            self.connect()
            self.cursor.execute("SELECT * FROM RECALL WHERE RecallNum = ?", (recallnum,))
            recall = self.cursor.fetchone()
            
            if recall is None:
                return (1, "Not Found")
            else:
             return recall  
        finally:
            self.close()

    def edit_recall(self, admin_id, recall_num, updates):
        """
        Updates recall information. 'updates' should be a dictionary with column names as keys and new values as values.
        Also logs the edit action by an admin.
        """
        try:
            self.connect()
            # Construct the SET part of the SQL command
            set_clause = ", ".join([f"{key} = ?" for key in updates.keys()])
            sql_command = f"UPDATE RECALL SET {set_clause} WHERE RecallNum = ?"
            self.cursor.execute(sql_command, list(updates.values()) + [recall_num])
            self.conn.commit()
            
            # Log the admin's edit action with the current datetime
            modification_date = datetime.now()
            edit_result = self.log_admin_edit_history(admin_id, recall_num, modification_date) 
            if edit_result[0] != 0:
                 return edit_result
            
            return (0, "Success")
        except sqlite3.IntegrityError as e:
            return (1, f"Integrity Error: {e}")
        except Exception as e:
            return (2, f"Unexpected Error: {e}")
        finally:
            self.close()

    def set_affected_states(self, admin_id,recall_num, state_nums):
        """
        Sets the states affected by a recall. Removes previous entries and sets new ones.
        """
        try:
            self.connect()
            # Delete old entries
            self.cursor.execute("DELETE FROM AFFECTS WHERE RecallNum = ?", (recall_num,))
            # Insert new entries
            for state_num in state_nums:
                self.cursor.execute("INSERT INTO AFFECTS (StateNum, RecallNum) VALUES (?, ?)", (state_num, recall_num))
                
                
            modification_date = datetime.now()
            edit_result = self.log_admin_edit_history(admin_id, recall_num, modification_date) 
            if edit_result[0] != 0:
                 return edit_result
            
            self.conn.commit()
            return (0, "Success")
        except sqlite3.IntegrityError as e:
            return (1, f"Integrity Error: {e}")
        except Exception as e:
            return (2, f"Unexpected Error: {e}")
        finally:
            self.close()

    def log_admin_edit_history(self, admin_id, recall_num, modification_date):
        """
        Logs or updates the history of admin edits to recalls with the latest modification time.
        The modification_date parameter expects a datetime object.
        """
        try:
            # Convert datetime object to string in SQLite datetime format
            formatted_date = modification_date.strftime("%Y-%m-%d %H:%M:%S")
            # INSERT OR REPLACE based on the unique constraint (ID, RecallNum)
            self.cursor.execute('INSERT OR REPLACE INTO MANAGES (ID, RecallNum, "Modification Date") VALUES (?, ?, ?)', 
                                (admin_id, recall_num, formatted_date))
            self.conn.commit()
            return (0, "Success")
        except sqlite3.IntegrityError as e:
            return (1, f"Integrity Error: {e}")
        except Exception as e:
            return (2, f"Unexpected Error: {e}")