DELIMITER //

CREATE TRIGGER supply_usage_insert_trigger 
AFTER INSERT ON SupplyUsage
FOR EACH ROW
BEGIN
    DECLARE shelter_id_var INT;
    
    SELECT s.shelter_id INTO shelter_id_var
    FROM CareRecords cr
    JOIN Animals a ON cr.animal_id = a.animal_id
    JOIN Shelters s ON a.shelter_id = s.shelter_id
    WHERE cr.record_id = NEW.record_id;

    UPDATE SupplyInventory
    SET quantity = quantity - NEW.quantity_used
    WHERE supply_id = NEW.supply_id 
      AND shelter_id = shelter_id_var;
END;//

CREATE TRIGGER supply_usage_delete_trigger 
BEFORE DELETE ON SupplyUsage
FOR EACH ROW
BEGIN
    DECLARE shelter_id_var INT;
    
    SELECT s.shelter_id INTO shelter_id_var
    FROM CareRecords cr
    JOIN Animals a ON cr.animal_id = a.animal_id
    JOIN Shelters s ON a.shelter_id = s.shelter_id
    WHERE cr.record_id = OLD.record_id;

    UPDATE SupplyInventory
    SET quantity = quantity + OLD.quantity_used
    WHERE supply_id = OLD.supply_id 
      AND shelter_id = shelter_id_var;
END; //

CREATE TRIGGER care_record_delete_supply_usage
BEFORE DELETE ON CareRecords
FOR EACH ROW
BEGIN
	DELETE FROM SupplyUsage WHERE record_id = OLD.record_id;
END; //

DELIMITER ;

