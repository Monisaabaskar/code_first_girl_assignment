-- Create the database
CREATE DATABASE IF NOT EXISTS split_expense_application;

-- Use the database
USE split_expense_application;

-- Create Users table 
CREATE TABLE IF NOT EXISTS users (
	user_id INT AUTO_INCREMENT,
	user_name VARCHAR(20) NOT NULL UNIQUE,
	email_address VARCHAR(100) NOT NULL UNIQUE,
	CONSTRAINT pk_user_id PRIMARY KEY(user_id) -- primary key
);

-- Create Expenses table - expense made by the users
CREATE TABLE IF NOT EXISTS expenses (
	expense_id INT PRIMARY KEY AUTO_INCREMENT,
	item_description VARCHAR(255) NOT NULL,
	total_amount DECIMAL(8,2) NOT NULL,
	expense_date DATE NOT NULL,
	lender_id INT NOT NULL,
	CONSTRAINT
		fk_lender_id FOREIGN KEY(lender_id) REFERENCES users(user_id) -- forign key
);

-- Create expense_groups table - different groups
CREATE TABLE IF NOT EXISTS expense_groups (
	group_id INT PRIMARY KEY AUTO_INCREMENT, 
	group_name VARCHAR(100) NOT NULL UNIQUE          
);

-- Create Group_Membership table (user belongs to which groups)
CREATE TABLE IF NOT EXISTS group_membership ( 
	id INT PRIMARY KEY AUTO_INCREMENT,
	user_id INT NOT NULL,
	group_id INT NOT NULL,
	CONSTRAINT
		FOREIGN KEY(user_id) REFERENCES users(user_id),
		FOREIGN KEY(group_id) REFERENCES expense_groups(group_id)
);

-- Create payment_shares table - It hold share amount of the people in different groups
CREATE TABLE IF NOT EXISTS payment_shares  (
	share_id INT PRIMARY KEY AUTO_INCREMENT,
    expense_id INT NOT NULL,
	lender_id INT NOT NULL,
	borrower_id INT NOT NULL,
	group_id INT NOT NULL,
	share_amount DECIMAL(8,2) NOT NULL,
	settled BOOLEAN DEFAULT 0,
	CONSTRAINT
		FOREIGN KEY(expense_id) REFERENCES expenses(expense_id),
		FOREIGN KEY(lender_id) REFERENCES users(user_id),
		FOREIGN KEY(borrower_id) REFERENCES users(user_id),
		FOREIGN KEY(group_id) REFERENCES expense_groups(group_id)
);


--  procedure to add a user
DELIMITER //
CREATE PROCEDURE add_user (      -- Declare a proc name to CREATE a new STORED PROCEDURE
	IN user_name VARCHAR(20),
	IN email_address VARCHAR(100))
BEGIN
	INSERT INTO users (user_name, email_address) VALUES(user_name, email_address);
END //
DELIMITER ;

-- Procedure to add a group
DELIMITER //
CREATE PROCEDURE add_group(
	IN group_name VARCHAR(100)
)
BEGIN
	INSERT INTO expense_groups (group_name) VALUES(group_name);
END //
DELIMITER ;

-- Procedure to add a user to a group
DELIMITER //
CREATE PROCEDURE add_user_to_group (
	IN _user_name VARCHAR(20),
	IN _group_name VARCHAR(100)
)
BEGIN
	DECLARE _user_id INT;
    DECLARE _group_id INT;
    
	(SELECT user_id INTO _user_id FROM users WHERE user_name = _user_name);
	(SELECT group_id INTO _group_id FROM expense_groups WHERE group_name = _group_name);
    
	INSERT INTO group_membership (user_id, group_id) 
				VALUES(_user_id, _group_id);
END //
DELIMITER ;

-- Procedure to split expense equally among group members
DELIMITER //
CREATE PROCEDURE split_expense_equally (
	IN lender_name VARCHAR(20),
    IN _total_amount DECIMAL(8,2),
    IN _group_name VARCHAR(100),
    IN _item_description VARCHAR(255),
    IN _expense_date DATE
)
BEGIN
	--  todo check if user belongs to group,
	DECLARE lender_id INT;
    DECLARE _group_id INT;
    DECLARE share_per_head DECIMAL(8,2);
    DECLARE group_member_count INT;
    DECLARE loop_index INT;
    DECLARE current_borrower INT;
    DECLARE last_expense_id INT;
    
    SET lender_id = (SELECT user_id FROM users WHERE user_name = lender_name);
    SET _group_id = (SELECT group_id FROM expense_groups WHERE group_name = _group_name);
    SET group_member_count = (SELECT COUNT(*) FROM group_membership WHERE group_id = _group_id);
	SET share_per_head = _total_amount / group_member_count;
    
	INSERT INTO expenses (item_description, total_amount, expense_date, lender_id) 
		   VALUES(_item_description, _total_amount, _expense_date, lender_id);
    SET last_expense_id = LAST_INSERT_ID();
                
	INSERT INTO payment_shares (expense_id, lender_id, borrower_id, group_id, share_amount)
		   SELECT last_expense_id, lender_id, borrowers.user_id, _group_id, share_per_head
		   FROM (SELECT user_id FROM group_membership 
				 WHERE group_id = _group_id AND user_id <> lender_id) AS borrowers;
END //
DELIMITER ;

-- To which groups the user belongs to.
DELIMITER //
CREATE PROCEDURE user_group_membership (
	IN user_name VARCHAR(20)
)    
BEGIN
    SELECT g.group_name
    FROM users u
    JOIN group_membership gm ON u.user_id = gm.user_id
    JOIN expense_groups g ON gm.group_id = g.group_id
    WHERE u.user_name = user_name;
END //
DELIMITER ;


-- Procedure to summarize group debts
DELIMITER //
CREATE PROCEDURE group_debt_summary(
	IN _group_name VARCHAR(255)
)
BEGIN
    DECLARE _group_id INT;

    -- Step 1: Retrieve the group ID from the group name
    SELECT group_id INTO _group_id
    FROM expense_groups
    WHERE group_name = _group_name
    LIMIT 1;

    CREATE TEMPORARY TABLE IF NOT EXISTS temp_debts AS
    SELECT
        borrower_id AS person_1,
        lender_id AS person_2,
        SUM(share_amount) AS net_amount
    FROM payment_shares
    WHERE group_id = _group_id
    GROUP BY borrower_id, lender_id;

    CREATE TEMPORARY TABLE IF NOT EXISTS temp_net_debts AS
    SELECT
        person_1,
        person_2,
        SUM(net_amount) AS net_amount
    FROM (
        SELECT borrower_id AS person_1, lender_id AS person_2, SUM(share_amount) AS net_amount
        FROM payment_shares
        WHERE group_id = _group_id
        GROUP BY borrower_id, lender_id

        UNION ALL

        SELECT lender_id AS person_1, borrower_id AS person_2, -SUM(share_amount) AS net_amount
        FROM payment_shares
        WHERE group_id = _group_id
        GROUP BY lender_id, borrower_id
    ) AS combined
    GROUP BY person_1, person_2
    HAVING net_amount <> 0;

    SELECT
        u1.user_name AS user_1,
        u2.user_name AS user_2,
        temp_net_debts.net_amount
    FROM temp_net_debts
    JOIN users u1 ON temp_net_debts.person_1 = u1.user_id
    JOIN users u2 ON temp_net_debts.person_2 = u2.user_id
    WHERE temp_net_debts.person_1 < temp_net_debts.person_2
    ORDER BY u1.user_name, u2.user_name;

    DROP TEMPORARY TABLE IF EXISTS temp_debts;
    DROP TEMPORARY TABLE IF EXISTS temp_net_debts;
END // 
DELIMITER ;

-- Procedure to delete an expense
DELIMITER //
CREATE PROCEDURE delete_expense(
	IN expense_id INT
)
BEGIN
	DELETE FROM expenses WHERE expense_id = expense_id;
    DELETE FROM shares WHERE expense_id = expense_id;
END// 
DELIMITER ;

-- DEMO Queries
-- Adding users
CALL add_user("john_smith", "john_smith@example.com");
-- CALL add_user("emily_johnson", "emily_johnson@example.com");
-- CALL add_user("michael_williams", "michael_williams@example.com");
-- CALL add_user("sarah_brown", "sarah_brown@example.com");
-- CALL add_user("david_jones", "david_jones@example.com");

-- Adding groups
CALL add_group("berlin_jun");
-- CALL add_group("hamburg_jun");

-- Adding users to groups
CALL add_user_to_group("john_smith", "berlin_jun");
-- CALL add_user_to_group("emily_johnson", "berlin_jun");
-- CALL add_user_to_group("michael_williams", "berlin_jun");
-- CALL add_user_to_group("john_smith", "hamburg_jun");
-- CALL add_user_to_group("sarah_brown", "hamburg_jun");
-- CALL add_user_to_group("david_jones", "hamburg_jun");

-- Checking user group membership
CALL user_group_membership("david_jones");
-- CALL user_group_membership("john_smith");

-- Splitting expenses equally
CALL split_expense_equally ("john_smith", 45, "berlin_jun", "backwerk", '2024-06-15');
-- CALL split_expense_equally ("emily_johnson", 60, "berlin_jun", "lunch", '2024-06-15');
CALL split_expense_equally ("john_smith", 45, "berlin_jun", "kamps", '2024-06-15');

-- Summarizing group debts
CALL group_debt_summary("berlin_jun");

-- Deleting an expense
CALL delete_expense(1);

-- Summarizing group debts again
CALL group_debt_summary("berlin_jun");
-- CALL group_debt_summary("hamburg_jun");

-- Selecting data from tables
SELECT * from users;
SELECT * from expense_groups;
(SELECT * FROM group_membership);
(SELECT * FROM expenses);
(SELECT * FROM payment_shares);

