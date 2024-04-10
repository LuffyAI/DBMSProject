INSERT INTO USER (Name, Password, PhoneNum, Email)
VALUES ("Larnell Moore", "123", "888-888-8888", "larnell@umich.edu");

INSERT INTO USER ( Name, Password, PhoneNum, Email)
VALUES ("Drew", "123", "777-777-7777", "Drew@umich.edu");

INSERT INTO USER (Name, Password, PhoneNum, Email)
VALUES ("Davvy", "123","666-666-6666", "Davvy@umich.edu");

INSERT INTO USER (Name, Password, PhoneNum, Email)
VALUES ("Maddie", "123", "555-555-5555", "Maddie@umich.edu");

INSERT INTO SUBSCRIBER (SubscriberID)
VALUES (1);

INSERT INTO SUBSCRIBER (SubscriberID)
VALUES (2);

INSERT INTO Admin (AdminID)
VALUES (3);

INSERT INTO Admin (AdminID)
VALUES (4);

INSERT INTO State (StateNum, Name)
VALUES (26, "Michigan");

INSERT INTO State (StateNum, Name)
VALUES (28, "Texas");

INSERT INTO State (StateNum, Name)
VALUES (31, "California");

INSERT INTO COMPANY (ID, TotalRecalls, Contact, Title)
  VALUES(1, 0, 'fakecompany@gmail.com', 'FakeCompany');

INSERT INTO COMPANY (ID, TotalRecalls, Contact, Title)
  VALUES(2, 0, "855-455-0098", "Taylor Farms’ Consumer Line");

INSERT INTO COMPANY (ID, TotalRecalls, Contact, Title)
  VALUES(3, 0, "(510) 351-1988", "Chief Operating Officer" );

INSERT INTO COMPANY (ID, TotalRecalls, Contact, Title)
  VALUES(4, 0, "duncanjr@macgregors.com", "General Manager, Macgregors Meat &amp; Seafood Ltd");
  
  INSERT INTO COMPANY (ID, TotalRecalls, Contact, Title)
  VALUES(5, 0, "Laura.Burns2@Tyson.com", "Vice President of External Communications");
  
INSERT INTO COMPANY (ID, TotalRecalls, Contact, Title)
  VALUES(6, 0, "johnkuethe@vaneefoods.com" ,"Director FSQA &amp; Regulatory Affairs");
  
INSERT INTO COMPANY (ID, TotalRecalls, Contact, Title)
  VALUES(7, 0, "pruskismarket@yahoo.com" ,"Pruski’s Market");
  
  INSERT INTO RECALL (RecallNum, ProductName, Category, CloseDate, Qty, Class, Reason, Year, RiskLevel, OpenDate, Type, CompanyID)
VALUES ("1", 'Test Product', 'Egg Products', '2024-03-25', 100, 'Class 1', 'Misbranding', "2024", 'High', '2024-03-20', 'Outbreak', 1);

INSERT INTO RECALL (RecallNum, ProductName, Category, CloseDate, Qty, Class, Reason, Year, RiskLevel, OpenDate, Type, CompanyID)
VALUES ("013-2024", "5.5-oz. clear plastic bowl containers with “kroger APPLE WALNUT WITH CHICKEN SALAD KIT FOR ONE” with use by dates of 03/12/24 through 03/22/24, lot codes TFPM059B41, TFPM060B41, TFPM061A41, TFPM062A41, TFPM063B41, TFPM064A41, TFPM064B41, TFPM065A41, TFP"
        , "Fully Cooked - Not Shelf Stable", "", 100, 'Class 1', "Misbranding", "", "Low - Class II", '2024-03-13', 'Active Recall', 2);

INSERT INTO RECALL (RecallNum, ProductName, Category, CloseDate, Qty, Class, Reason, Year, RiskLevel, OpenDate, Type, CompanyID)
VALUES ("064-2013", "Individual, Chinese Style Chicken Sausage." , "Products with Secondary Inhibitors - Not Shelf Stable", "2013-12-04", 100, "Class 3", 
        "Misbranding", "2013", "Marginal - Class III", "2013-11-07", "Closed Recall", 3);


INSERT INTO RECALL (RecallNum, ProductName, Category, CloseDate, Qty, Class, Reason, Year, RiskLevel, OpenDate, Type, CompanyID)
VALUES ("004-2024", "1.5-lb. cartons containing &quot;44TH Street Slow Cooked BABY BACK RIBS MAPLEWOOD SMOKED SAUCE&quot; with Julian dates 3453 and 0154 printed on the side of the immediate package. The product is packed in cases marked with Cert. No. Cert 043436, Production Date 3453, 1.5-lb. cartons containing &quot;44TH Street Glazed, Slow Cooked BABY BACK RIBS HONEY GARLIC SAUCE&quot; with Julian dates 1453 and 1593 printed on the side of the immediate package. The product is packed in cases marked with Cert. No. Cert 043436, Production Date ", 
         "Fully Cooked - Not Shelf Stable", "2024-02-22", 100, 'Class 1', "Misbranding", "2024", "High - Class I", '2024-02-02', "Closed Recall", 4);

INSERT INTO RECALL (RecallNum, ProductName, Category, CloseDate, Qty, Class, Reason, Year, RiskLevel, OpenDate, Type, CompanyID)
VALUES ("057-2023", "29-oz. Plastic bag packages containing “Tyson FULLY COOKED FUN NUGGETS BREADED SHAPED CHICKEN PATTIES” with a Best If Used By date of SEP 04, 2024, and lot codes 2483BRV0207, 2483BRV0208, 2483BRV0209 and 2483BRV0210." 
        , "Fully Cooked - Not Shelf Stable", "2024-02-06", 100, 'Class 1', "Product Contamination", "2024", "High - Class I", "2023-11-04", "Closed Recall", 5);


INSERT INTO RECALL (RecallNum, ProductName, Category, CloseDate, Qty, Class, Reason, Year, RiskLevel, OpenDate, Type, CompanyID)
VALUES ("003-2024", "1-lb. plastic tubs labeled as &quot;Sysco Classic Chicken Flavored Base&quot; with lot code 02673 and packaged in a case labeled as &quot;Sysco Classic BEEF BASE CF&quot; with lot code 02673 represented on the label.",
        "Not Heat Treated - Shelf Stable", "2024-03-01", 200,
       "Class 1", "Unreported Allergens", "2024", "Class I", "2024-02-01", "Closed Recall", 6);

INSERT INTO RECALL (RecallNum, ProductName, Category, CloseDate, Qty, Class, Reason, Year, RiskLevel, OpenDate, Type, CompanyID)
VALUES ("PHA-11172023-01", "• 1.75-oz., 2.75-oz., and 8-oz. packages containing “Pruski’s Market Spicy Beef Jerky”  and a “SELL BY” date ranging from 03/21/24 through 05/09/24 represented on the  back of the packages., • 1.75-oz., 2.75-oz., and 8-oz. packages containing “Pruski’s Market Beef Jerky” and a  “SELL BY” date ranging from 03/21/24 through 05/09/24 represented on the back of  the packages., • 1.75-oz, 2.75-oz., and 8-oz. packages containing “Pruski’s Market Turkey Jerky” and a  “SELL BY” date ranging from 03/21/24 through 05/09/24 represented on the back of  the packages., • 3-oz. packages containing “HOOSER CUSTOM MEATS BEEF JERKY MESQUITE  SMOKED” and a “SELL BY” of 04/23/24 represented on the back of the packages., • Packages purchased by weight at the retail counter, containing “Beef Jerky Regular”,  “Spicy Beef Jerky”, or “Turkey Jerky” with Pack Date ranging from 9/21/23 through  11/9/23.",
       "Heat Treated - Shelf Stable", "", 150, "Public Health Alert", "Unreported Allergens", "", "Public Health Alert", 
       "2023-11-17", "Public Health Alert", 7);

INSERT INTO MANAGES (ID, RecallNum, [Modification Date])
VALUES(3, 1, "2024-04-04 01:58:05");

INSERT INTO AFFECTS (StateNum, RecallNum)
VALUES(26, "1");
INSERT INTO AFFECTS (StateNum, RecallNum)
VALUES(26, "013-2024");
INSERT INTO AFFECTS (StateNum, RecallNum)
VALUES(26, "064-2013");

INSERT INTO AFFECTS (StateNum, RecallNum)
VALUES(28, "004-2024");
INSERT INTO AFFECTS (StateNum, RecallNum)
VALUES(28, "057-2023");

INSERT INTO AFFECTS (StateNum, RecallNum)
VALUES(31, "003-2024");
INSERT INTO AFFECTS (StateNum, RecallNum)
VALUES(31, "PHA-11172023-01");

