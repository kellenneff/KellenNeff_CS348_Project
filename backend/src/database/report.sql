DELIMITER //
CREATE PROCEDURE GenerateReport(
    IN startDate DATE,
    IN endDate DATE,
    IN shelterString TEXT,
    IN animalString TEXT,
    IN supplyString TEXT,
    IN staffString TEXT
)
BEGIN
    
	DROP TEMPORARY TABLE IF EXISTS FilteredResults;
    DROP TEMPORARY TABLE IF EXISTS UnfilteredResults;
    DROP TEMPORARY TABLE IF EXISTS StatsResults;
    
    CREATE TEMPORARY TABLE FilteredResults AS
    SELECT cr.record_id, a.animal_id, a.name AS animal_name, a.shelter_id,
            sh.name AS shelter_name, s.staff_id, s.name AS staff_name,
            cr.date AS record_date, cr.notes, cs.supply_id, cs.name AS supply_name,
            su.quantity_used
    FROM CareRecords cr
    JOIN Animals a ON cr.animal_id = a.animal_id
    JOIN Staff s ON cr.staff_id = s.staff_id
    JOIN Shelters sh ON a.shelter_id = sh.shelter_id
    LEFT JOIN SupplyUsage su ON cr.record_id = su.record_id
    LEFT JOIN CareSupplies cs ON su.supply_id = cs.supply_id;
    
    CREATE TEMPORARY TABLE UnFilteredResults AS
    SELECT * 
    FROM FilteredResults;
    
    
    IF startDate IS NOT NULL THEN
        DELETE FROM FilteredResults
        WHERE record_date < startDate;
    END IF;
    
    IF endDate IS NOT NULL THEN
        DELETE FROM FilteredResults
        WHERE record_date > endDate;
    END IF;
    
    IF animalString IS NOT NULL AND animalString != '' THEN
        DELETE FROM FilteredResults
        WHERE NOT FIND_IN_SET(animal_id, animalString);
    END IF;
    
    IF staffString IS NOT NULL AND staffString != '' THEN
        DELETE FROM FilteredResults
        WHERE NOT FIND_IN_SET(staff_id, staffString);
    END IF;
    
    IF shelterString IS NOT NULL AND shelterString != '' THEN
        DELETE FROM FilteredResults
        WHERE NOT FIND_IN_SET(shelter_id, shelterString);
    END IF;
    
    IF supplyString IS NOT NULL AND supplyString != '' THEN
        DELETE FROM FilteredResults
        WHERE NOT FIND_IN_SET(supply_id, supplyString);
    END IF;
    
    CREATE TEMPORARY TABLE StatsResults (
        stat_name VARCHAR(100),
        stat_value VARCHAR(255),
        stat_count DECIMAL(10,2)
    ) ENGINE=MEMORY;
    
    INSERT INTO StatsResults
    SELECT 
        'Most Used Supply' as stat_name,
        supply_name as stat_value,
        SUM(quantity_used) as stat_count
    FROM FilteredResults
    WHERE supply_id IS NOT NULL
    GROUP BY supply_id, supply_name
    ORDER BY SUM(quantity_used) DESC
    LIMIT 1;
    
    INSERT INTO StatsResults
    SELECT 
        'Most Frequent Supply' as stat_name,
        supply_name as stat_value,
        COUNT(DISTINCT record_id) as stat_count
    FROM FilteredResults
    WHERE supply_id IS NOT NULL
    GROUP BY supply_id, supply_name
    ORDER BY COUNT(DISTINCT record_id) DESC
    LIMIT 1;
    
    INSERT INTO StatsResults
    SELECT 
        'Average Supply Quantity' as stat_name,
        ROUND(AVG(quantity_used), 2) as stat_value,
        COUNT(DISTINCT record_id) as sample_size
    FROM FilteredResults
    WHERE quantity_used IS NOT NULL;
    
    INSERT INTO StatsResults
    SELECT 
        'Most Frequent Staff' as stat_name,
        staff_name as stat_value,
        COUNT(DISTINCT record_id) as stat_count
    FROM FilteredResults
    GROUP BY staff_id, staff_name
    ORDER BY COUNT(DISTINCT record_id) DESC
    LIMIT 1;
    
    INSERT INTO StatsResults
    SELECT 
        'Most Frequent Animal' as stat_name,
        animal_name as stat_value,
        COUNT(DISTINCT record_id) as stat_count
    FROM FilteredResults
    GROUP BY animal_id, animal_name
    ORDER BY COUNT(DISTINCT record_id) DESC
    LIMIT 1;
    
    SELECT * FROM StatsResults;
    
    SELECT * FROM UnfilteredResults ur
    WHERE ur.record_id in (
		SELECT fr.record_id FROM FilteredResults fr
    );
END //
DELIMITER ;