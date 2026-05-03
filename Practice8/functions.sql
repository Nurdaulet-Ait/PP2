CREATE TABLE IF NOT EXISTS contacts (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    surname VARCHAR(100),
    phone VARCHAR(20) UNIQUE NOT NULL
);

CREATE OR REPLACE FUNCTION search_contacts(pattern TEXT)
RETURNS TABLE(id INT, name VARCHAR, surname VARCHAR, phone VARCHAR)
AS $$
BEGIN
    RETURN QUERY
    SELECT c.id, c.name, c.surname, c.phone
    FROM contacts c
    WHERE c.name ILIKE '%' || pattern || '%'
       OR c.surname ILIKE '%' || pattern || '%'
       OR c.phone ILIKE '%' || pattern || '%';
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_contacts_paginated(limit_count INT, offset_count INT)
RETURNS TABLE(id INT, name VARCHAR, surname VARCHAR, phone VARCHAR)
AS $$
BEGIN
    RETURN QUERY
    SELECT c.id, c.name, c.surname, c.phone
    FROM contacts c
    ORDER BY c.id
    LIMIT limit_count OFFSET offset_count;
END;
$$ LANGUAGE plpgsql;
