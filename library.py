import json
from datetime import datetime, timedelta

DATA_FILE = "data.json"
FINE_PER_DAY = 5  # fine amount per day


def load_data():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"books": {}, "issued_books": {}}


def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)


def add_book(data):
    book_id = input("Enter Book ID: ")
    title = input("Enter Book Title: ")
    author = input("Enter Author Name: ")

    data["books"][book_id] = {
        "title": title,
        "author": author,
        "available": True
    }
    save_data(data)
    print("Book added successfully!")


def remove_book(data):
    book_id = input("Enter Book ID to remove: ")
    if book_id in data["books"]:
        del data["books"][book_id]
        save_data(data)
        print("Book removed successfully!")
    else:
        print("Book not found!")


def issue_book(data):
    book_id = input("Enter Book ID: ")
    student_name = input("Enter Student Name: ")

    if book_id in data["books"] and data["books"][book_id]["available"]:
        issue_date = datetime.now()
        due_date = issue_date + timedelta(days=14)

        data["books"][book_id]["available"] = False
        data["issued_books"][book_id] = {
            "student": student_name,
            "issue_date": issue_date.strftime("%Y-%m-%d"),
            "due_date": due_date.strftime("%Y-%m-%d")
        }
        save_data(data)
        print("Book issued successfully!")
    else:
        print("Book not available or not found!")


def return_book(data):
    book_id = input("Enter Book ID: ")

    if book_id in data["issued_books"]:
        due_date = datetime.strptime(
            data["issued_books"][book_id]["due_date"], "%Y-%m-%d"
        )
        return_date = datetime.now()

        fine = 0
        if return_date > due_date:
            days_late = (return_date - due_date).days
            fine = days_late * FINE_PER_DAY

        data["books"][book_id]["available"] = True
        del data["issued_books"][book_id]
        save_data(data)

        print("Book returned successfully!")
        print(f"Fine: ₹{fine}")
    else:
        print("This book was not issued!")


def display_books(data):
    print("\nAvailable Books:")
    for book_id, info in data["books"].items():
        status = "Available" if info["available"] else "Issued"
        print(f"{book_id} | {info['title']} | {info['author']} | {status}")


def main():
    data = load_data()

    while True:
        print("\n--- Library Management System ---")
        print("1. Add Book")
        print("2. Remove Book")
        print("3. Issue Book")
        print("4. Return Book")
        print("5. Display Books")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_book(data)
        elif choice == "2":
            remove_book(data)
        elif choice == "3":
            issue_book(data)
        elif choice == "4":
            return_book(data)
        elif choice == "5":
            display_books(data)
        elif choice == "6":
            print("Exiting system...")
            break
        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()
