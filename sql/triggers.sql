CREATE TRIGGER is_admin_a_subscriber
BEFORE INSERT ON SUBSCRIBER
FOR EACH ROW
BEGIN
  SELECT RAISE(ABORT, 'This ID is already an admin.')
  WHERE EXISTS (SELECT 1 FROM ADMIN WHERE AdminID = NEW.SubscriberID);
END;

CREATE TRIGGER is_subscriber_an_admin
BEFORE INSERT ON ADMIN
FOR EACH ROW
BEGIN
  SELECT RAISE(ABORT, 'This ID is already a subscriber.')
  WHERE EXISTS (SELECT 1 FROM SUBSCRIBER WHERE SubscriberID = NEW.AdminID);
END;

CREATE TRIGGER IncrementTotalRecalls
AFTER INSERT ON RECALL
FOR EACH ROW
BEGIN
    UPDATE COMPANY
    SET TotalRecalls = TotalRecalls + 1
    WHERE ID = NEW.CompanyID;
END;

CREATE TRIGGER DecrementTotalRecalls
AFTER DELETE ON RECALL
FOR EACH ROW
BEGIN
    UPDATE COMPANY
    SET TotalRecalls = TotalRecalls - 1
    WHERE ID = OLD.CompanyID;
END;

CREATE TRIGGER UpdateTotalRecalls
AFTER UPDATE OF CompanyID ON RECALL
FOR EACH ROW
WHEN OLD.CompanyID != NEW.CompanyID
BEGIN
    -- Decrement the total recalls count for the old company
    UPDATE COMPANY
    SET TotalRecalls = TotalRecalls - 1
    WHERE ID = OLD.CompanyID;

    -- Increment the total recalls count for the new company
    UPDATE COMPANY
    SET TotalRecalls = TotalRecalls + 1
    WHERE ID = NEW.CompanyID;
END;


CREATE TRIGGER CheckCompanyExistsBeforeRecallInsert
BEFORE INSERT ON RECALL
FOR EACH ROW
BEGIN
    SELECT RAISE(ABORT, 'No corresponding company exists.')
    WHERE NOT EXISTS (SELECT 1 FROM COMPANY WHERE ID = NEW.CompanyID);
END;