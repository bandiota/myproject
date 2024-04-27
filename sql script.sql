DELIMITER //
DROP TRIGGER IF EXISTS after_stockmgmgt_stock_update//
CREATE TRIGGER after_stockmgmgt_stock_update AFTER UPDATE ON stockmgmgt_stock FOR EACH ROW
BEGIN
	IF new.issue_quantity = 0 
		THEN INSERT INTO stockmgmgt_stockhistory(
			id, 
			last_updated, 
            category_id,
			item_name,
            issue_quantity,
			quantity, 
			receive_quantity, 
			receive_by) 
		VALUES(
			new.id, 
			new.last_updated, 
            new.category_id,
			new.item_name, 
            new.issue_quantity,
			new.quantity, 
			new.receive_quantity, 
			new.receive_by);

	ELSEIF new.receive_quantity = 0 
		THEN INSERT INTO stockmgmgt_stockhistory(
			id, 
			last_updated,
            category_id,
			item_name, 
            receive_quantity, 
			issue_quantity, 
			issue_to, 
			issue_by, 
			quantity) 
		VALUES(
			new.id, 
			new.last_updated, 
            new.category_id,
			new.item_name,
            new.receive_quantity,
			new.issue_quantity, 
			new.issue_to, 
			new.issue_by, 
			new.quantity);
	END IF;
END//
DELIMITER ;