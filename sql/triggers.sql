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

CREATE TRIGGER BeforeInsertIS_SUBSCRIBED
BEFORE INSERT ON IS_SUBSCRIBED
FOR EACH ROW
BEGIN
    SELECT RAISE(ABORT, 'SubscriberID does not exist in SUBSCRIBER table.')
    WHERE NOT EXISTS (
        SELECT 1 FROM SUBSCRIBER WHERE SubscriberID = NEW.SubscriberID
    );
END;

CREATE TRIGGER VerifyBeforeDeleteIS_SUBSCRIBED
BEFORE DELETE ON IS_SUBSCRIBED
FOR EACH ROW
BEGIN
    SELECT RAISE(ABORT, 'Cannot delete non-existing SubscriberID from IS_SUBSCRIBED.')
    WHERE NOT EXISTS (
        SELECT 1 FROM IS_SUBSCRIBED WHERE SubscriberID = OLD.SubscriberID
    );
END;
