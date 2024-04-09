import sys
sys.path.append('../')
from DatabaseManager.dbManager import DBManager
from setupDatabase import initDatabase as init

db_path = "test_db.db"
sql_files = ['../sql/tables.sql', '../sql/triggers.sql', '../sql/insertions.sql']
init(db_path, sql_files)
Manager = DBManager(db_path)

def test_new_user_insert():
    """Checks if the database can insert a new user"""
    result = Manager.insert_user("Larnell", "123", "555-555-5555", "Larnell@email.com")
    print(result)
    assert(result == (0, "Success"))
    
def test_same_user_second_time_insert():
    """Checks if the database will apply its UNIQUE constraint"""
    result = Manager.insert_user("Larnell", "123", "555-555-5555", "Larnell@email.com")
    print(result)
    assert(result == (1, 'Integrity Error: UNIQUE constraint failed: USER.Email'))
    
def test_insert_user_into_subscriber_table():
    """Checks that a user can become a subcriber"""
    result = Manager.insert_subscriber("Larnell@email.com")
    print(result)
    assert(result == (0, "Success"))
    
def test_insert_admin_into_subscriber_table():
    """Checks that admins and subcribers are mutually exclusive"""
    result = Manager.insert_subscriber("Davvy@umich.edu")
    print(result)
    assert(result == (1, 'Integrity Error: This ID is already an admin.'))

def test_insert_nonexisting_user_into_subscriber_table():
    """Checks that the DBMS won't allow you add subscribers that do not exist"""
    result = Manager.insert_subscriber("DioBrando@email.com")
    print(result)
    assert(result == (3, "User does not exist!"))
    
def test_admin_tries_to_sub_to_state():
    """Checks that an adminID cannot be in the IS_SUBSCRIBED table"""
    result = Manager.sub_to_state(3, "Michigan")
    print(result)
    assert(result == (3, 'User not found') )
    
def test_subscriber_tries_to_sub_to_state():
    """Checks that a subscriber can subscribe to IS_SUBSCRIBED table"""
    result = Manager.sub_to_state(1, "Michigan")
    print(result)
    assert(result == (0, "Success"))
    
def test_subscriber_tries_to_sub_to_state_second_time():
    """Checks that an subscriber cannot sub twice for IS_SUBSCRIBED table"""
    result = Manager.sub_to_state(1, "Michigan")
    print(result)
    assert(result == (1, 'Integrity Error: UNIQUE constraint failed: IS_SUBSCRIBED.SubscriberID, IS_SUBSCRIBED.StateNum'))
    
def test_subscriber_tries_to_sub_to_nonexistent_state():
    """Checks that an subscriber cannot sub to a state that does not exist"""
    result = Manager.sub_to_state(1, "Underworld")
    print(result)
    assert(result == (2, 'State not found'))
    
def test_subscriber_fetches_subscribed_states():
    """Checks that an subscriber can fetch their subbed states"""
    result = Manager.get_subscriber_states(1)
    print(result)
    assert(result == [{'StateNum': 26, 'StateName': 'Michigan'}])
    
    
def test_subscriber_tries_to_get_recalls():
     """Checks that a subscriber can get their recall subscription info"""
     
     # We expect the result should be the recalls of both Michigan and California
     # since we subbed to michigan and california for subscriberid 1
     result = Manager.sub_to_state(1, "California")
     result = Manager.get_subscription_recalls(1)
     expected_result = [
         {'StateName': 'Michigan', 
          'RecallNum': '013-2024', 
          'ProductName': '5.5-oz. clear plastic bowl containers with “kroger APPLE WALNUT WITH CHICKEN SALAD KIT FOR ONE” with use by dates of 03/12/24 through 03/22/24, lot codes TFPM059B41, TFPM060B41, TFPM061A41, TFPM062A41, TFPM063B41, TFPM064A41, TFPM064B41, TFPM065A41, TFP', 
          'Category': 'Fully Cooked - Not Shelf Stable', 
          'CloseDate': '', 
          'Qty': 100, 
          'Class': 'Class 1', 
          'Reason': 'Misbranding', 
          'Year': '', 'RiskLevel': 'Low - Class II', 
          'OpenDate': '2024-03-13', 
          'Type': 'Active Recall', 
          'CompanyID': 2, 
          'CompanyTitle': 'Taylor Farms’ Consumer Line'}, 
         
         {'StateName': 'Michigan', 
          'RecallNum': '064-2013', 
          'ProductName': 'Individual, Chinese Style Chicken Sausage.', 
          'Category': 'Products with Secondary Inhibitors - Not Shelf Stable', 
          'CloseDate': '2013-12-04', 
          'Qty': 100, 
          'Class': 'Class 3', 
          'Reason': 'Misbranding', 
          'Year': '2013', 
          'RiskLevel': 'Marginal - Class III', 
          'OpenDate': '2013-11-07', 
          'Type': 'Closed Recall', 
          'CompanyID': 3, 
          'CompanyTitle': 'Chief Operating Officer'}, 
         
          {'StateName': 'Michigan', 
           'RecallNum': '1', 
           'ProductName': 'Test Product', 
           'Category': 'Egg Products', 
           'CloseDate': '2024-03-25', 
           'Qty': 100, 
           'Class': 'Class 1', 
           'Reason': 'Misbranding', 
           'Year': '2024', 
           'RiskLevel': 'High', 
           'OpenDate': '2024-03-20', 
           'Type': 'Outbreak', 
           'CompanyID': 1, 
           'CompanyTitle': 'FakeCompany'}, 
          
          {'StateName': 'California', 
           'RecallNum': '003-2024', 
           'ProductName': '1-lb. plastic tubs labeled as &quot;Sysco Classic Chicken Flavored Base&quot; with lot code 02673 and packaged in a case labeled as &quot;Sysco Classic BEEF BASE CF&quot; with lot code 02673 represented on the label.', 
           'Category': 'Not Heat Treated - Shelf Stable', 
           'CloseDate': '2024-03-01', 
           'Qty': 200, 
           'Class': 'Class 1', 
           'Reason': 'Unreported Allergens', 
           'Year': '2024', 
           'RiskLevel': 'Class I', 
           'OpenDate': '2024-02-01', 
           'Type': 'Closed Recall', 
           'CompanyID': 6, 
           'CompanyTitle': 'Director FSQA &amp; Regulatory Affairs'}, 
          
          {'StateName': 'California', 
           'RecallNum': 'PHA-11172023-01', 
           'ProductName': '• 1.75-oz., 2.75-oz., and 8-oz. packages containing “Pruski’s Market Spicy Beef Jerky”  and a “SELL BY” date ranging from 03/21/24 through 05/09/24 represented on the  back of the packages., • 1.75-oz., 2.75-oz., and 8-oz. packages containing “Pruski’s Market Beef Jerky” and a  “SELL BY” date ranging from 03/21/24 through 05/09/24 represented on the back of  the packages., • 1.75-oz, 2.75-oz., and 8-oz. packages containing “Pruski’s Market Turkey Jerky” and a  “SELL BY” date ranging from 03/21/24 through 05/09/24 represented on the back of  the packages., • 3-oz. packages containing “HOOSER CUSTOM MEATS BEEF JERKY MESQUITE  SMOKED” and a “SELL BY” of 04/23/24 represented on the back of the packages., • Packages purchased by weight at the retail counter, containing “Beef Jerky Regular”,  “Spicy Beef Jerky”, or “Turkey Jerky” with Pack Date ranging from 9/21/23 through  11/9/23.', 
           'Category': 'Heat Treated - Shelf Stable', 
           'CloseDate': '', 
           'Qty': 150, 
           'Class': 'Public Health Alert', 
           'Reason': 'Unreported Allergens', 
           'Year': '', 
           'RiskLevel': 'Public Health Alert', 
           'OpenDate': '2023-11-17', 
           'Type': 'Public Health Alert', 
           'CompanyID': 7, 
           'CompanyTitle': 'Pruski’s Market'}]
     print(result)
     assert(result == expected_result)
     
def test_subscriber_unsubs_from_a_state():
    """Tests that the unsubcription feature works as intended"""
    result = Manager.unsub_to_state(1, "Michigan")
    print(result)
    assert(result == (0, 'Success'))
    
def test_subscriber_unsub_changed_their_recall_feed():
    """Tests how unsubbing affects the results of subscriber retrieved recalls"""
    result = Manager.get_subscription_recalls(1)
    
    #We unsubbed from michigan so we expect to see only california recalls
    expected_result = [
          {'StateName': 'California', 
           'RecallNum': '003-2024', 
           'ProductName': '1-lb. plastic tubs labeled as &quot;Sysco Classic Chicken Flavored Base&quot; with lot code 02673 and packaged in a case labeled as &quot;Sysco Classic BEEF BASE CF&quot; with lot code 02673 represented on the label.', 
           'Category': 'Not Heat Treated - Shelf Stable', 
           'CloseDate': '2024-03-01', 
           'Qty': 200, 
           'Class': 'Class 1', 
           'Reason': 'Unreported Allergens', 
           'Year': '2024', 
           'RiskLevel': 'Class I', 
           'OpenDate': '2024-02-01', 
           'Type': 'Closed Recall', 
           'CompanyID': 6, 
           'CompanyTitle': 'Director FSQA &amp; Regulatory Affairs'}, 
          
          {'StateName': 'California', 
           'RecallNum': 'PHA-11172023-01', 
           'ProductName': '• 1.75-oz., 2.75-oz., and 8-oz. packages containing “Pruski’s Market Spicy Beef Jerky”  and a “SELL BY” date ranging from 03/21/24 through 05/09/24 represented on the  back of the packages., • 1.75-oz., 2.75-oz., and 8-oz. packages containing “Pruski’s Market Beef Jerky” and a  “SELL BY” date ranging from 03/21/24 through 05/09/24 represented on the back of  the packages., • 1.75-oz, 2.75-oz., and 8-oz. packages containing “Pruski’s Market Turkey Jerky” and a  “SELL BY” date ranging from 03/21/24 through 05/09/24 represented on the back of  the packages., • 3-oz. packages containing “HOOSER CUSTOM MEATS BEEF JERKY MESQUITE  SMOKED” and a “SELL BY” of 04/23/24 represented on the back of the packages., • Packages purchased by weight at the retail counter, containing “Beef Jerky Regular”,  “Spicy Beef Jerky”, or “Turkey Jerky” with Pack Date ranging from 9/21/23 through  11/9/23.', 
           'Category': 'Heat Treated - Shelf Stable', 
           'CloseDate': '', 
           'Qty': 150, 
           'Class': 'Public Health Alert', 
           'Reason': 'Unreported Allergens', 
           'Year': '', 
           'RiskLevel': 'Public Health Alert', 
           'OpenDate': '2023-11-17', 
           'Type': 'Public Health Alert', 
           'CompanyID': 7, 
           'CompanyTitle': 'Pruski’s Market'}]
    print(result)
    assert(result == expected_result)
    
def test_admin_add_recall():
    """Admin adds a brand new recall to the database"""
    recall_details = (
        "R12345",                       # RecallNum
        "Example Product Name",         # ProductName
        "Not Heat Treated - Shelf Stable",  # Category
        "2023-12-31",                   # CloseDate
        100,                            # Qty
        "Class 1",                      # Class
        "Mislabeling",                  # Reason
        "2023",                         # Year
        "High",                         # RiskLevel
        "2023-01-01",                   # OpenDate
        "Active Recall",                # Type
        1                               # CompanyID
    )
    result = Manager.add_recall(3, recall_details)
    print(result)
    assert(result == (0, 'Success'))


def test_admin_add_same_recall():
    """Admin attempts to add the same recall two times"""
    recall_details = (
        "R12345",                       # RecallNum
        "Example Product Name",         # ProductName
        "Not Heat Treated - Shelf Stable",  # Category
        "2023-12-31",                   # CloseDate
        100,                            # Qty
        "Class 1",                      # Class
        "Mislabeling",                  # Reason
        "2023",                         # Year
        "High",                         # RiskLevel
        "2023-01-01",                   # OpenDate
        "Active Recall",                # Type
        1                               # CompanyID
    )
    
    result = Manager.add_recall(3, recall_details)
    print(result)
    assert(result == (1, 'Integrity Error: UNIQUE constraint failed: RECALL.RecallNum'))

def test_admin_set_affected_states_for_recall():
    """Admin sets a recall R12345 to affect Texas and California. This sends it to users
    who are subscribed to these statements."""
    state_nums = [28,31]
    result = Manager.set_affected_states(3, "R12345", state_nums)
    print(result)
    assert(result == (0, 'Success'))

def test_recall_affect_multiple_states():
    """Checks if the recently added recalls is updated by the subscriber view to reflect such"""
    Manager.sub_to_state(1, "Texas")
    result = Manager.get_subscription_recalls(1)
    filtered_dict = [d for d in result if d['RecallNum'] == 'R12345']
    
    # Should be the same recall but placed in the feed for the specified states
    expected_result1= {'StateName': 'Texas', 
                       'RecallNum': 'R12345', 
                       'ProductName': 'Example Product Name', 
                       'Category': 'Not Heat Treated - Shelf Stable', 
                       'CloseDate': '2023-12-31', 
                       'Qty': 100, 
                       'Class': 'Class 1', 
                       'Reason': 'Mislabeling', 
                       'Year': '2023', 
                       'RiskLevel': 'High', 
                       'OpenDate': '2023-01-01', 
                       'Type': 'Active Recall', 
                       'CompanyID': 1, 'CompanyTitle': 'FakeCompany'}
    
    expected_result2= {'StateName': 'California', 
                       'RecallNum': 'R12345', 
                       'ProductName': 'Example Product Name', 
                       'Category': 'Not Heat Treated - Shelf Stable', 
                       'CloseDate': '2023-12-31', 
                       'Qty': 100, 
                       'Class': 'Class 1', 
                       'Reason': 'Mislabeling', 
                       'Year': '2023', 
                       'RiskLevel': 'High', 
                       'OpenDate': '2023-01-01', 
                       'Type': 'Active Recall', 
                       'CompanyID': 1, 'CompanyTitle': 'FakeCompany'}
   
    assert(filtered_dict[0] == expected_result1)
    assert(filtered_dict[1] == expected_result2)
    

def test_admin_edit_recall():
    """Checks that an admin can edit a recall"""
    Updates = {
    "ProductName": "Updated Product Name",
    "Reason": "Mislabeling"
    }
    
    result = Manager.edit_recall(4, 'R12345', Updates)
    print(result)
    assert(result == (0, 'Success'))
    
def test_view_all_recalls():
    """Checks that an admin can view all recalls"""    
    result = Manager.view_all_recalls()
    print(result)
    assert(result != (0, 'Not Found'))
    
def test_view_recall_edit_history():
    """Checks that an admin can view a recall's edit history""" 
    result = Manager.view_recall_edit_history('R12345')
    expected_result = [
        ('R12345', 'Updated Product Name', 'Not Heat Treated - Shelf Stable', 100, 'Class 1', 'Mislabeling', '2023', 'High', '2023-01-01', 'Active Recall', 'FakeCompany', '2024-04-08 22:17:21', 3), 
        ('R12345', 'Updated Product Name', 'Not Heat Treated - Shelf Stable', 100, 'Class 1', 'Mislabeling', '2023', 'High', '2023-01-01', 'Active Recall', 'FakeCompany', '2024-04-08 22:17:21', 4)
        ]
    print(result)
    assert(result != expected_result)


    


     
     
