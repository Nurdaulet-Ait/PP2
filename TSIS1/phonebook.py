import csv
import json
import os
from connect import get_connection

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def file_path(filename):
    return os.path.join(BASE_DIR, filename)


def print_rows(rows):
    if not rows:
        print("No results")
        return

    for row in rows:
        print("-" * 90)
        print(" | ".join(str(value) if value is not None else "" for value in row))


def safe_date(value):
    value = (value or "").strip()
    return value if value else None


def safe_phone_type(value):
    value = (value or "mobile").strip().lower()
    if value not in ("home", "work", "mobile"):
        return "mobile"
    return value


def get_group_id(cur, group_name):
    group_name = (group_name or "Other").strip() or "Other"

    cur.execute("""
        INSERT INTO groups(name)
        VALUES (%s)
        ON CONFLICT (name) DO NOTHING
    """, (group_name,))

    cur.execute("SELECT id FROM groups WHERE name = %s", (group_name,))
    return cur.fetchone()[0]


def load_sql_file(filename):
    conn = get_connection()
    cur = conn.cursor()

    try:
        with open(file_path(filename), "r", encoding="utf-8") as file:
            cur.execute(file.read())
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()


def init_database():
    load_sql_file("schema.sql")
    load_sql_file("procedures.sql")
    print("Database schema, functions, and procedures were created successfully")


def save_contact(cur, name, email, birthday, group_name, phone=None, phone_type="mobile", overwrite=True):
    group_id = get_group_id(cur, group_name)

    if overwrite:
        cur.execute("""
            INSERT INTO contacts(name, email, birthday, group_id)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (name)
            DO UPDATE SET
                email = EXCLUDED.email,
                birthday = EXCLUDED.birthday,
                group_id = EXCLUDED.group_id
            RETURNING id
        """, (name, email or None, safe_date(birthday), group_id))
    else:
        cur.execute("""
            INSERT INTO contacts(name, email, birthday, group_id)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (name) DO NOTHING
            RETURNING id
        """, (name, email or None, safe_date(birthday), group_id))

    result = cur.fetchone()

    if result is None:
        cur.execute("SELECT id FROM contacts WHERE name = %s", (name,))
        result = cur.fetchone()

    contact_id = result[0]

    if phone:
        cur.execute("""
            INSERT INTO phones(contact_id, phone, type)
            VALUES (%s, %s, %s)
            ON CONFLICT (contact_id, phone)
            DO UPDATE SET type = EXCLUDED.type
        """, (contact_id, phone, safe_phone_type(phone_type)))

    return contact_id


def add_contact_from_console():
    name = input("Name: ").strip()
    email = input("Email: ").strip()
    birthday = input("Birthday YYYY-MM-DD or empty: ").strip()
    group_name = input("Group [Other]: ").strip() or "Other"
    phone = input("Phone: ").strip()
    phone_type = input("Phone type home/work/mobile [mobile]: ").strip() or "mobile"

    if not name:
        print("Name is required")
        return

    conn = get_connection()
    cur = conn.cursor()

    try:
        save_contact(cur, name, email, birthday, group_name, phone, phone_type)
        conn.commit()
        print("Contact saved")
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()


def import_from_csv():
    filename = input("CSV file name [contacts.csv]: ").strip() or "contacts.csv"
    path = filename if os.path.isabs(filename) else file_path(filename)

    conn = get_connection()
    cur = conn.cursor()

    try:
        with open(path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                save_contact(
                    cur,
                    row["name"].strip(),
                    row.get("email", "").strip(),
                    row.get("birthday", "").strip(),
                    row.get("group", "Other").strip(),
                    row.get("phone", "").strip(),
                    row.get("phone_type", "mobile").strip(),
                    overwrite=True
                )
        conn.commit()
        print("CSV imported successfully")
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()


def export_to_json():
    filename = input("Output JSON file name [contacts.json]: ").strip() or "contacts.json"
    path = filename if os.path.isabs(filename) else file_path(filename)

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.id, c.name, c.email, c.birthday, g.name, c.created_at
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        ORDER BY c.name
    """)

    data = []

    for contact_id, name, email, birthday, group_name, created_at in cur.fetchall():
        cur.execute("""
            SELECT phone, type
            FROM phones
            WHERE contact_id = %s
            ORDER BY id
        """, (contact_id,))

        phones = [
            {"phone": phone, "type": phone_type}
            for phone, phone_type in cur.fetchall()
        ]

        data.append({
            "name": name,
            "email": email,
            "birthday": str(birthday) if birthday else None,
            "group": group_name,
            "created_at": str(created_at),
            "phones": phones
        })

    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    cur.close()
    conn.close()
    print("Exported to", path)


def import_from_json():
    filename = input("JSON file name [contacts.json]: ").strip() or "contacts.json"
    path = filename if os.path.isabs(filename) else file_path(filename)

    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    conn = get_connection()
    cur = conn.cursor()

    try:
        for item in data:
            name = item["name"].strip()

            cur.execute("SELECT id FROM contacts WHERE name = %s", (name,))
            duplicate = cur.fetchone()

            if duplicate:
                answer = input(f"{name} already exists. skip / overwrite? ").strip().lower()

                if answer == "skip":
                    continue

                if answer != "overwrite":
                    print("Unknown answer. Skipped.")
                    continue

                cur.execute("DELETE FROM phones WHERE contact_id = %s", (duplicate[0],))

            contact_id = save_contact(
                cur,
                name,
                item.get("email", ""),
                item.get("birthday"),
                item.get("group", "Other"),
                overwrite=True
            )

            for phone_item in item.get("phones", []):
                cur.execute("""
                    INSERT INTO phones(contact_id, phone, type)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (contact_id, phone)
                    DO UPDATE SET type = EXCLUDED.type
                """, (
                    contact_id,
                    phone_item.get("phone"),
                    safe_phone_type(phone_item.get("type"))
                ))

        conn.commit()
        print("JSON imported successfully")
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()


def show_all_contacts():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            c.id,
            c.name,
            c.email,
            c.birthday,
            g.name AS group_name,
            COALESCE(string_agg(p.phone || ' (' || p.type || ')', ', ' ORDER BY p.type), 'No phones') AS phones,
            c.created_at
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        GROUP BY c.id, c.name, c.email, c.birthday, g.name, c.created_at
        ORDER BY c.name
    """)

    print_rows(cur.fetchall())
    cur.close()
    conn.close()


def filter_by_group():
    group_name = input("Group name: ").strip()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.id, c.name, c.email, c.birthday, g.name AS group_name
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        WHERE g.name ILIKE %s
        ORDER BY c.name
    """, (f"%{group_name}%",))

    print_rows(cur.fetchall())
    cur.close()
    conn.close()


def search_by_email():
    query = input("Email search text: ").strip()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, name, email, birthday
        FROM contacts
        WHERE email ILIKE %s
        ORDER BY name
    """, (f"%{query}%",))

    print_rows(cur.fetchall())
    cur.close()
    conn.close()


def search_with_function():
    query = input("Search text: ").strip()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM search_contacts(%s)", (query,))
    print_rows(cur.fetchall())

    cur.close()
    conn.close()


def sort_contacts():
    print("1. Sort by name")
    print("2. Sort by birthday")
    print("3. Sort by date added")

    choice = input("Choose: ").strip()

    order_options = {
        "1": "c.name",
        "2": "c.birthday NULLS LAST, c.name",
        "3": "c.created_at, c.name"
    }

    order_by = order_options.get(choice)

    if not order_by:
        print("Wrong choice")
        return

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(f"""
        SELECT c.id, c.name, c.email, c.birthday, g.name AS group_name, c.created_at
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        ORDER BY {order_by}
    """)

    print_rows(cur.fetchall())
    cur.close()
    conn.close()


def paginated_navigation():
    try:
        limit = int(input("Page size: ").strip())
    except ValueError:
        print("Page size must be a number")
        return

    offset = 0

    while True:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM get_contacts_page(%s, %s)", (limit, offset))
        rows = cur.fetchall()

        cur.close()
        conn.close()

        print("\nPage offset:", offset)
        print_rows(rows)

        command = input("next / prev / quit: ").strip().lower()

        if command == "next":
            offset += limit
        elif command == "prev":
            offset = max(0, offset - limit)
        elif command == "quit":
            break
        else:
            print("Unknown command")


def add_phone_using_procedure():
    name = input("Contact name: ").strip()
    phone = input("New phone: ").strip()
    phone_type = input("Type home/work/mobile: ").strip()

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, phone_type))
        conn.commit()
        print("Phone added")
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()


def move_to_group_using_procedure():
    name = input("Contact name: ").strip()
    group_name = input("New group: ").strip()

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("CALL move_to_group(%s, %s)", (name, group_name))
        conn.commit()
        print("Contact moved")
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()


def delete_contact():
    name = input("Contact name: ").strip()

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("DELETE FROM contacts WHERE name = %s", (name,))
        conn.commit()
        print("Contact deleted")
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()


def show_menu():
    print("""
PHONEBOOK TSIS1 MENU

1. Create schema + load procedures
2. Import from CSV
3. Add contact from console
4. Show all contacts
5. Filter by group
6. Search by email
7. Search all fields using search_contacts function
8. Sort contacts
9. Paginated navigation
10. Export to JSON
11. Import from JSON
12. Add phone using procedure
13. Move contact to group using procedure
14. Delete contact
0. Exit
""")


def main():
    actions = {
        "1": init_database,
        "2": import_from_csv,
        "3": add_contact_from_console,
        "4": show_all_contacts,
        "5": filter_by_group,
        "6": search_by_email,
        "7": search_with_function,
        "8": sort_contacts,
        "9": paginated_navigation,
        "10": export_to_json,
        "11": import_from_json,
        "12": add_phone_using_procedure,
        "13": move_to_group_using_procedure,
        "14": delete_contact,
    }

    while True:
        show_menu()
        choice = input("Choose: ").strip()

        if choice == "0":
            break

        action = actions.get(choice)

        if action is None:
            print("Wrong choice")
            continue

        try:
            action()
        except Exception as error:
            print("ERROR:", error)
            print("Tip: first run option 1. Check config.py password and database name.")


if __name__ == "__main__":
    main()
