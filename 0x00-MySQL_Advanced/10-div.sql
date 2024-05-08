-- Script that creates a function SafeDiv that divides
-- (and returns) the first by the second number or returns
-- 0 if the second number is equal to 0.

-- Create function SafeDiv
DELIMITER $$

CREATE FUNCTION SafeDiv(
        a INT,
        b INT
)
RETURNS FLOAT
DETERMINISTIC
BEGIN
    -- check if b is equal to 0
        IF b = 0 THEN
	    RETURN 0; -- return 0 if b is 0
        END IF;

        RETURN a / b; -- divide a by b if b is not 0
END $$

DELIMITER ;

