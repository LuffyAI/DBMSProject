import sqlite3
from datetime import datetime

class DBManager:
    def __init__(self, db_path):
        self.db_path = db_path
        print(db_path)
        
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
            
            # If no user is found, return (2, "User does not exist!", None)
            if user is None:
             return (2, "User does not exist!", None)
            
            user_id = user[0]
            
            # Check if the user is an admin
            self.cursor.execute("SELECT AdminID FROM ADMIN WHERE AdminID = ?", (user_id,))
            if self.cursor.fetchone():
                return (1, "Admin", user_id)  

            # Check if the user is a subscriber
            self.cursor.execute("SELECT SubscriberID FROM SUBSCRIBER WHERE SubscriberID = ?", (user_id,))
            if self.cursor.fetchone():
                return (0, 'Sub', user_id)  
                        
        except Exception as e:
            return (3, f"Unexpected Error: {e}", None)
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
        Returns 0 on success, 1 on integrity error, 2 if state not found, 3 if subsriber not found, and 4 for unexpected error.
        """
        try:
            self.connect()
            
            # Get state number
            self.cursor.execute("SELECT StateNum FROM STATE WHERE Name = ?", (state_name,))
            state_num = self.cursor.fetchone()
            
            if not state_num:
                return (2, "State not found")  
            
            self.cursor.execute("SELECT SubscriberID FROM SUBSCRIBER WHERE SubscriberID = ?", (subscriber_id,))
            user = self.cursor.fetchone()
            
            if not user:
                return (3, "User not found")  
            
            
            # Subscribe the user to the state
            self.cursor.execute("INSERT INTO IS_SUBSCRIBED (SubscriberID, StateNum) VALUES (?, ?)", (subscriber_id, state_num[0]))
            self.conn.commit()
            return (0, "Success")  # Success
        
        except sqlite3.IntegrityError as s:
            return (1, f"Integrity Error: {s}")
        except Exception as e:
            return (4,f"Unexpected error: {e}")
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
            
            self.cursor.execute("SELECT SubscriberID FROM SUBSCRIBER WHERE SubscriberID = ?", (subscriber_id,))
            user = self.cursor.fetchone()
            
            if not user:
                return (3, "User not found")  
            
            # Unsubscribe the user to the state
            self.cursor.execute("DELETE FROM IS_SUBSCRIBED WHERE SubscriberID = ? AND StateNum = ?", (subscriber_id, state_num[0]))
            self.conn.commit()
            return (0, "Success")  # Success
        
        except sqlite3.IntegrityError as s:
                return (1, f"Integrity Error: {s}")
            
        except Exception as e:
            return (4,f"Unexpected error: {e}")
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
    def add_recall(self, admin_id, states, recall_details):
        """
        Adds a recall record to the RECALL table and associates the recall with affected states.
        """
        try:
            self.connect()
            
            # Assuming recall_details is a tuple and the last element is the company title
            company_title = recall_details[-1]
            
            # Use placeholders for safe SQL queries
            self.cursor.execute("SELECT ID FROM COMPANY WHERE Title = ?", (company_title,))
            company_row = self.cursor.fetchone()
            
            if company_row is None:
                print(f"Company with title {company_title} not found.")
                return (1, "Company not found")
            
            companyID = company_row[0]
            print(f"CompanyID: {companyID}")
            
            # Replace company title with companyID in recall_details
            recall_details_list = list(recall_details)
            recall_details_list[-1] = companyID
            recall_details = tuple(recall_details_list)
            
            # Insert new recall entry into RECALL table
            self.cursor.execute(
                "INSERT INTO RECALL (RecallNum, ProductName, Category, CloseDate, Qty, Class, Reason, Year, RiskLevel, OpenDate, Type, CompanyID) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                recall_details)
            
            print("yes")
            # Get the RecallNum from recall_details
            recall_num = recall_details[0]
           
            
            # For each state in the provided states array, find its StateNum and insert into AFFECTS table
            for state_name in states:
                self.cursor.execute("SELECT StateNum FROM STATE WHERE Name = ?", (state_name,))
                state_num = self.cursor.fetchone()
                if state_num:
                    self.cursor.execute(
                        "INSERT INTO AFFECTS (StateNum, RecallNum) VALUES (?, ?)", 
                        (state_num[0], recall_num))
            
            # Automatically log this action
            modification_date = datetime.now()
            edit_result = self.log_admin_edit_history(admin_id, recall_num, modification_date) 
            if edit_result[0] != 0:
                    return edit_result
            
            self.conn.commit()
            return (0, "Success")
        except sqlite3.IntegrityError as e:
            print(e)
            return (1, f"Integrity Error: {e}")
        except Exception as e:
            print(e)
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
            
    def view_all_recalls(self):
        """
        Grabs the recall information + company, and then fetches states affected by the recall.
        """
        try:
            self.connect()
            # Fetch the basic recall information and company name
            self.cursor.execute("""
            SELECT 
                R.RecallNum, R.ProductName, R.Category, R.Qty, R.Class, R.Reason, 
                R.Year, R.RiskLevel, R.OpenDate, R.Type, C.Title AS CompanyName,
                (SELECT MAX(M.[Modification Date]) FROM MANAGES M WHERE M.RecallNum = R.RecallNum) AS LastModificationDate
            FROM RECALL R
            JOIN COMPANY C ON R.CompanyID = C.ID
            """)
            recalls = self.cursor.fetchall()
            
            if not recalls:
                return (1, "Not Found")
            
            # For each recall, fetch the affected states
            recalls_with_states = []
            for recall in recalls:
                recallNum = recall[0]  # Assuming RecallNum is the first column
                self.cursor.execute("""
                SELECT GROUP_CONCAT(S.Name, ', ')
                FROM AFFECTS A
                JOIN STATE S ON A.StateNum = S.StateNum
                WHERE A.RecallNum = ?
                GROUP BY A.RecallNum
                """, (recallNum,))
                affected_states = self.cursor.fetchone()[0]
                if affected_states is None:
                    affected_states = 'Not set yet'
                
                # Combine the recall info with the affected states into a new tuple
                recall_with_states = recall + (affected_states,)
                recalls_with_states.append(recall_with_states)
                
            return (0, recalls_with_states)
        finally:
            self.close()
            
    def view_company_rankings(self):
        """
        Views the ranking of companies based on the total number of recalls, ordered from highest to lowest.
        """
        try:
            self.connect()
            self.cursor.execute("""
            SELECT
            Title, TotalRecalls
            FROM COMPANY
            ORDER BY TotalRecalls DESC
            """)
            rankings = self.cursor.fetchall()
            print(rankings, "hello")

            if not rankings:
                return (1, "No company rankings found.")
            else:
                return (0, rankings)
        finally:
            self.close()
            
    def view_recall_edit_history(self, recall_number):
        """
        Grabs the edit history of a specific recall along with the admins responsible for each edit.
        """
        try:
            self.connect()
            self.cursor.execute("""
            SELECT
                R.RecallNum, R.ProductName, R.Category, R.Qty, R.Class, R.Reason,
                R.Year, R.RiskLevel, R.OpenDate, R.Type, C.Title AS CompanyName,
                M.[Modification Date], M.ID AS AdminID
            FROM RECALL R
            JOIN COMPANY C ON R.CompanyID = C.ID
            JOIN MANAGES M ON R.RecallNum = M.RecallNum
            WHERE R.RecallNum = ?
            ORDER BY M.[Modification Date] DESC
            """, (recall_number,))
            edits = self.cursor.fetchall()

            if not edits:
                return (1, "Not Found")
            else:
                return edits
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
            
    def get_affected_states(self, recall_num):
        """
        Retrieves the states affected by a recall.
        """
        affected_states = []
        try:
            self.connect()
            # Select affected states
            self.cursor.execute("""
            SELECT S.Name 
            FROM AFFECTS A
            JOIN STATE S ON A.StateNum = S.StateNum
            WHERE A.RecallNum = ?""", (recall_num,))
            
            affected_states = [state[0] for state in self.cursor.fetchall()]
            
            if not affected_states:
                return (1, "No affected states found for this recall number.")
            
            return (0, affected_states)
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