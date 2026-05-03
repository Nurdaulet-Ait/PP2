from connect import get_connection


def setup_database():
    conn = get_connection()
    cur = conn.cursor()

    with open("functions.sql", "r", encoding="utf-8") as file:
        cur.execute(file.read())

    with open("procedures.sql", "r", encoding="utf-8") as file:
        cur.execute(file.read())

    conn.commit()
    cur.close()
    conn.close()
    print("Database setup completed.")


def show_all():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM contacts ORDER BY id")
    rows = cur.fetchall()

    if not rows:
        print("No contacts found.")
    else:
        for row in rows:
            print(row)

    cur.close()
    conn.close()


def add_or_update_contact():
    name = input("Name: ")
    surname = input("Surname: ")
    phone = input("Phone: ")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CALL upsert_contact(%s, %s, %s)", (name, surname, phone))
    conn.commit()
    cur.close()
    conn.close()
    print("Contact inserted or updated.")


def search_contact():
    pattern = input("Search pattern: ")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM search_contacts(%s)", (pattern,))
    rows = cur.fetchall()

    if not rows:
        print("Nothing found.")
    else:
        for row in rows:
            print(row)

    cur.close()
    conn.close()


def pagination():
    limit_count = int(input("Limit: "))
    offset_count = int(input("Offset: "))

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (limit_count, offset_count))
    rows = cur.fetchall()

    if not rows:
        print("No contacts on this page.")
    else:
        for row in rows:
            print(row)

    cur.close()
    conn.close()


def delete_contact():
    value = input("Enter name or phone to delete: ")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CALL delete_contact_by_name_or_phone(%s)", (value,))
    conn.commit()
    cur.close()
    conn.close()
    print("Delete completed.")


def insert_many_contacts():
    names = []
    surnames = []
    phones = []

    count = int(input("How many contacts do you want to insert? "))

    for i in range(count):
        print(f"Contact {i + 1}")
        names.append(input("Name: "))
        surnames.append(input("Surname: "))
        phones.append(input("Phone: "))

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("CALL insert_many_contacts(%s, %s, %s)", (names, surnames, phones))
    cur.execute("SELECT * FROM incorrect_contacts")
    incorrect = cur.fetchall()

    conn.commit()
    cur.close()
    conn.close()

    if incorrect:
        print("Incorrect phone data:")
        for row in incorrect:
            print(row)
    else:
        print("All contacts inserted successfully.")


def menu():
    while True:
        print("""
PhoneBook Practice 8
1. Setup database
2. Show all contacts
3. Add or update contact
4. Search by pattern
5. Show contacts with pagination
6. Delete by name or phone
7. Insert many contacts
0. Exit
""")
        choice = input("Choose: ")

        if choice == "1":
            setup_database()
        elif choice == "2":
            show_all()
        elif choice == "3":
            add_or_update_contact()
        elif choice == "4":
            search_contact()
        elif choice == "5":
            pagination()
        elif choice == "6":
            delete_contact()
        elif choice == "7":
            insert_many_contacts()
        elif choice == "0":
            break
        else:
            print("Wrong choice.")


if __name__ == "__main__":
    menu()
