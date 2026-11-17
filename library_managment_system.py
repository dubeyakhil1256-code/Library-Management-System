import os
import json
from pathlib import Path
from abc import ABC, abstractmethod
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Keep the SAME filename as your original project
database = os.path.join(BASE_DIR, "library_data.json")
data = {"students": [], "books": []}
if Path(database).exists():
    try:
        with open(database, "r") as f:
            content = f.read().strip()
            if content:
                data = json.loads(content)
    except json.JSONDecodeError:
        print("Your JSON file contains invalid data.")
data.setdefault("students", [])
data.setdefault("books", [])
def save():
    with open(database, "w") as f:
        json.dump(data, f, indent=4)
# ---------------- ABSTRACT CLASS ----------------
class General(ABC):

    @abstractmethod
    def get_roles(self):
        pass

    @abstractmethod
    def register(self):
        pass

    @abstractmethod
    def show_details(self):
        pass

    @staticmethod
    def validate_email(email):
        return "@" in email and "." in email
    
# ---------------- PERSON CLASS ----------------
class Persons(General):
#----------THIS IS THE ROLES FUNCTION TO BE USED--------------
    def get_roles(self):
        return "Person"
    
#------------THIS IS THE REGISTER PERSON FUNCTION ----------------
    
    def register(self):
        name = input("Tell your name: ")

#--------- TRY AND EXCEPT ALSO USED IN THE CODE
        try:
            age = int(input("Tell your age: "))
            if age <= 0:
                print("Invalid age")
                return
        except ValueError:
            print("Age must be a number")
            return
        email = input("Tell your email: ")
        Lib_Id = input("Tell your roll number: ")

#------------- VALIDATE THE EMAIL ID ----------------
        
        if not General.validate_email(email):
            print("Invalid email")
            return
        for i in data["students"]:
            if i["roll_no"] == Lib_Id:
                print("Student already exists")
                return
        new_student = {
            "name": name,
            "age": age,
            "email": email,
            "roll_no": Lib_Id,
            "Books": []
        }

# ---------------APPEND THE DATA TAKEN FROM THE USER TO THE JSON FILE-----------

        data["students"].append(new_student)
        save()
        print("Student registered successfully!")
        print(data["students"])

#-------------- SHOW DETAILS FUNCTION FOR THE USER---------------
    
    def show_details(self):
        Lib_Id = input("Enter your roll number: ")
        print("DEBUG DATA:", data["students"])
        for s in data["students"]:
            if s["roll_no"] == Lib_Id:
                print("Student Found!")
                print(f"Name: {s['name']}")
                print(f"Age: {s['age']}")
                print(f"Email: {s['email']}")
                print(f"Roll Number: {s['roll_no']}")
                print(f"Books: {s['Books']}")
                return
        print("Student not found.")

#------------ADD BOOK FUCNTION TO ADD A BOOK IN THE JSON-----------
    
    def add_book(self):
        Lib_Id = input("Tell the roll number: ")
        Book_Id = input("Enter Book ID: ")
        student = None
        book = None
        for i in data["students"]:
            if i["roll_no"] == Lib_Id:
                student = i
                break
        if student is None:
            print("Student not found.")
            return
        for b in data["books"]:
            if b["Book_Id"] == Book_Id:
                book = b
                break
        if book is None:
            print("Book not found.")
            return
        if not book["available"]:
            print("Book is already issued.")
            return
        book["available"] = False
        student["Books"].append(Book_Id)
        save()
        print("Book issued successfully!")

#--------RETURN BOOK FUNCTION TO RETRUN A BOOK FROM THE USER TO THE LIBRARY
    
    def return_book(self):
        Lib_Id = input("Enter student roll number: ")
        Book_Id = input("Enter Book ID: ")
        for student in data["students"]:
            if student["roll_no"] == Lib_Id:
                if Book_Id not in student["Books"]:
                    print("This student has not issued this book.")
                    return
                for book in data["books"]:
                    if book["Book_Id"] == Book_Id:
                        book["available"] = True
                        student["Books"].remove(Book_Id)
                        save()
                        print("Book returned successfully!")
                        return
        print("Student not found.")

# <------------------BOOKS CLASS STARTS HERE-------------------->
class Book(General):
    def get_roles(self):
        return "Book"
    def register(self):
        name = input("Tell the book name: ")
        author_Name = input("Tell the author name: ")
        subject = input("Tell the subject: ")
        Book_Id = input("Tell the book ID: ")
        for i in data["books"]:
            if i["Book_Id"] == Book_Id:
                print("Book already exists.")
                return
        data["books"].append({
            "name": name,
            "author_name": author_Name,
            "subject": subject,
            "Book_Id": Book_Id,
            "available": True
        })
        save()
        print(f"Book {name} registered successfully!")

# ---------SHOWS THE BOOK DETAILS HERE-------

    def show_details(self):
        Book_Id = input("Tell me your Book ID: ")
        for t in data["books"]:
            if t["Book_Id"] == Book_Id:
                print(f"\nName: {t['name']}")
                print(f"Author: {t['author_name']}")
                print(f"Subject: {t['subject']}")
                print(f"Book ID: {t['Book_Id']}")
                if t["available"]:
                    print("Status: Available")
                else:
                    print("Status: Issued")
                return
        print("Book not found.")

        #------------- TO EDIT A BOOK FUNCTION IS HERE--------------
    
    def edit_book(self):
        Book_Id = input("Enter Book ID to edit: ")
        for i in data["books"]:
            if i["Book_Id"] == Book_Id:
                print("Leave a field empty to keep its old value.")
                name = input("New book name: ")
                author = input("New author name: ")
                subject = input("New subject: ")
                if name:
                    i["name"] = name
                if author:
                    i["author_name"] = author
                if subject:
                    i["subject"] = subject
                save()
                print("Book updated successfully!")
                return
        print("Book not found.")

    #------------ TO DELELTE A BOOK A FUCNTION IS HERE------------
    
    def delete_book(self):
        Book_Id = input("Enter Book ID to delete: ")
        for i in data["books"]:
            if i["Book_Id"] == Book_Id:
                if not i["available"]:
                    print("Cannot delete a book that is currently issued.")
                    return
                data["books"].remove(i)
                save()
                print("Book deleted successfully!")
                return
        print("Book not found.")
stud = Persons()
book = Book()
while True:
    print("\n========== LIBRARY MANAGEMENT SYSTEM ==========")
    print("1. Register a Person")
    print("2. Register a Book")
    print("3. Issue a Book")
    print("4. Return a Book")
    print("5. Show Person Details")
    print("6. Show Book Details")
    print("7. Edit Book")
    print("8. Delete Book")
    print("9. Exit")
    try:
        choice = int(input("\nPlease tell your choice: "))
    except ValueError:
        print("Please enter a valid number.")
        continue
    if choice == 1:
        stud.register()
    elif choice == 2:
        book.register()
    elif choice == 3:
        stud.add_book()
    elif choice == 4:
        stud.return_book()
    elif choice == 5:
        stud.show_details()
    elif choice == 6:
        book.show_details()
    elif choice == 7:
        book.edit_book()
    elif choice == 8:
        book.delete_book()
    elif choice == 9:
        print("Thank you for using the Library Management System!")
        break
    else:
        print("Invalid choice. Try again.")
