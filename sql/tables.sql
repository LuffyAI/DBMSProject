CREATE TABLE USER 
( 
  ID INTEGER PRIMARY KEY AUTOINCREMENT,
  Name		CHAR(50)		NOT NULL,
  Password  Varchar(256)    NOT NULL,
  PhoneNum	VARCHAR(20)		NOT NULL,
  Email		VARCHAR(30)		NOT NULL,
  UNIQUE(Email)
);
 
CREATE TABLE SUBSCRIBER
(
  SubscriberID            INT NOT NULL,
  PRIMARY KEY(SubscriberID),
  FOREIGN KEY(SubscriberID) REFERENCES [USER](ID)
);
  
CREATE TABLE ADMIN
(
  AdminID          INT NOT NULL,
  PRIMARY KEY(AdminID),
  FOREIGN KEY(AdminID) REFERENCES [USER](ID)
);

CREATE TABLE IS_SUBSCRIBED
( SubscriberID INT NOT NULL,
  StateNum INT NOT NULL,
  PRIMARY KEY(SubscriberID, StateNum),
  FOREIGN KEY(SubscriberID) REFERENCES SUBSCRIBER(SubscriberID),
  FOREIGN KEY(StateNum) REFERENCES State(StateNum)
);

CREATE TABLE STATE
 ( StateNum	INT	NOT NULL,
    Name	CHAR(20) NOT NULL,
  PRIMARY KEY(StateNum)
 );

 
 CREATE TABLE COMPANY
  (ID				INT	 NOT NULL,
  TotalRecalls			INT		NOT NULL,
  Contact			VARCHAR(30)		NOT NULL,
  Title				VARCHAR(50)		NOT NULL,
  PRIMARY KEY(ID));


CREATE TABLE RECALL (
    RecallNum VARCHAR(20) NOT NULL,
    ProductName VARCHAR(200) NOT NULL,
    Category VARCHAR(100) CHECK (Category IN ('Egg Products', 'Fully Cooked - Not Shelf Stable', 'Heat Treated - Not Fully Cooked - Not Shelf Stable', 'Heat Treated - Shelf Stable', 'Not Heat Treated - Shelf Stable', 'Products with Secondary Inhibitors - Not Shelf Stable', 'Raw - Intact', 'Raw - Non-Intact', 'Slaughter', 'Thermally Processed - Commercially Sterile', 'Unknown')) NOT NULL,
    CloseDate DATE ,
    Qty INT NOT NULL,
    Class VARCHAR(20) CHECK (Class IN ('Class 1', 'Class 2', 'Class 3', 'Public Health Alert')) NOT NULL,
    Reason VARCHAR(100) CHECK (Reason IN ('Import Violation', 'Insanitary Conditions', 'Misbranding', 'Mislabeling', 'Processing Defect', 'Produced Without Benefit of Inspection', 'Product Contamination', 'Unfit for Human Consumption', 'Unreported Allergens')) NOT NULL,
    Year  VARCHAR(20),
    RiskLevel VARCHAR(30) NOT NULL,
    OpenDate DATE NOT NULL,
    Type VARCHAR(20) CHECK (Type IN ('Outbreak', 'Public Health Alert', 'Active Recall', 'Closed Recall')) NOT NULL,
    CompanyID INT NOT NULL,
    PRIMARY KEY (RecallNum),
 	FOREIGN KEY (CompanyID) REFERENCES COMPANY (ID));

  CREATE TABLE AFFECTS
  ( StateNum				INT		NOT NULL,
    RecallNum			VARCHAR(20)		NOT NULL,
  PRIMARY KEY(StateNum, RecallNum),
  FOREIGN KEY(StateNum) REFERENCES STATE(StateNum),
  FOREIGN KEY(RecallNum) REFERENCES RECALL(RecallNum)
  );

CREATE TABLE MANAGES (
    ID INT NOT NULL,
    RecallNum INT NOT NULL,
    [Modification Date] DATE NOT NULL,
    PRIMARY KEY (ID, RecallNum),
    FOREIGN KEY (ID) REFERENCES [USER] (ID),
    FOREIGN KEY (RecallNum) REFERENCES RECALL (RecallNum)
);

