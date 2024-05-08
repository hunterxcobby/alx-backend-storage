-- Write a SQL script that creates a trigger
-- trigger decreases the quantity of an item after adding a new order.
-- Quantity in the table items can be negative.

-- Create trigger to decrease item quantity after adding a new order
CREATE TRIGGER decrease_item_quantity AFTER INSERT ON orders
FOR EACH ROW
-- Update the quantity of the item in the items table
UPDATE items
SET quantity = quantity - NEW.number
WHERE name = NEW.item_name;

