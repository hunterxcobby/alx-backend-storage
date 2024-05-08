-- SQL script that creates a stored procedure AddBonus that adds a new correction for a student.
-- Requirements:
-- Procedure AddBonus is taking 3 inputs (in this order):
-- user_id, a users.id value (you can assume user_id is linked to an existing users)
-- project_name, a new or already exists projects -
-- if no projects.name found in the table, you should create it
-- score, the score value for the correction

-- Create stored procedure AddBonus
DELIMITER $$

CREATE PROCEDURE AddBonus(
    IN p_user_id INT,
    IN p_project_name VARCHAR(255),
    IN p_score INT
)
BEGIN
    DECLARE project_id INT;

    -- Check if the project already exists
    SELECT id INTO project_id
    FROM projects
    WHERE name = p_project_name;

    -- If the project doesn't exist, create it
    IF project_id IS NULL THEN
        INSERT INTO projects (name) VALUES (p_project_name);
        SET project_id = LAST_INSERT_ID();
    END IF;

    -- Add the correction for the student
    INSERT INTO corrections (user_id, project_id, score)
    VALUES (p_user_id, project_id, p_score);
    
END $$

DELIMITER ;

