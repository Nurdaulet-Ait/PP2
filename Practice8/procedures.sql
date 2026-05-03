CREATE OR REPLACE PROCEDURE upsert_contact(
    p_name VARCHAR,
    p_surname VARCHAR,
    p_phone VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM contacts WHERE phone = p_phone) THEN
        UPDATE contacts
        SET name = p_name,
            surname = p_surname
        WHERE phone = p_phone;
    ELSE
        INSERT INTO contacts(name, surname, phone)
        VALUES (p_name, p_surname, p_phone);
    END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE delete_contact_by_name_or_phone(p_value VARCHAR)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM contacts
    WHERE name = p_value OR phone = p_value;
END;
$$;

CREATE OR REPLACE PROCEDURE insert_many_contacts(
    p_names VARCHAR[],
    p_surnames VARCHAR[],
    p_phones VARCHAR[]
)
LANGUAGE plpgsql
AS $$
DECLARE
    i INT;
BEGIN
    CREATE TEMP TABLE IF NOT EXISTS incorrect_contacts (
        name VARCHAR,
        surname VARCHAR,
        phone VARCHAR
    ) ON COMMIT DROP;

    FOR i IN 1..array_length(p_names, 1) LOOP
        IF p_phones[i] ~ '^87[0-9]{9}$' OR p_phones[i] ~ '^\+77[0-9]{9}$' THEN
            CALL upsert_contact(p_names[i], p_surnames[i], p_phones[i]);
        ELSE
            INSERT INTO incorrect_contacts(name, surname, phone)
            VALUES (p_names[i], p_surnames[i], p_phones[i]);
        END IF;
    END LOOP;
END;
$$;
