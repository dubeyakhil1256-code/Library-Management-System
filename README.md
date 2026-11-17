# 📚 Library Management System

A console-based Library Management System built using **Python and Object-Oriented Programming (OOP)**. This project allows users to manage students, books, and book transactions through a simple menu-driven interface.

## 🚀 Features

- **Student Registration:** Register students with their name, age, email, and roll number.
- **Book Registration:** Add books with details such as title, author, subject, and unique Book ID.
- **Issue Books:** Issue available books to registered students.
- **Return Books:** Return previously issued books and update their availability.
- **Student Details:** View registered student information and their issued books.
- **Book Details:** Check book information and availability status.
- **Edit Books:** Update existing book information.
- **Delete Books:** Remove books that are not currently issued.
- **Data Persistence:** Store and retrieve records using JSON files, so data remains available after restarting the program.

## 🛠️ Technologies Used

- **Python 3**
- **Object-Oriented Programming**
- **JSON** – For storing and managing data.
- **File Handling** – For reading and writing records.
- **ABC Module** – For implementing abstract classes.
- **OS and Pathlib** – For file path management.

## 📂 Project Structure

```text
Library-Management-System/
│
├── library_app.py
├── library_managment_system.json
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/dubeyakhil1256-code/Library-Management-System.git
```

### 2. Navigate to the project directory

```bash
cd Library-Management-System
```

### 3. Run the application

```bash
python3 library_app.py
```

## 📋 Available Operations

The application provides the following menu options:

| Option | Operation |
|---|---|
| 1 | Register a Person |
| 2 | Register a Book |
| 3 | Issue a Book |
| 4 | Return a Book |
| 5 | Show Person Details |
| 6 | Show Book Details |
| 7 | Edit Book |
| 8 | Delete Book |
| 9 | Exit |

## 🧠 OOP Concepts Implemented

This project demonstrates practical implementation of:

- Classes and Objects
- Constructors (`__init__`)
- Instance Methods
- Inheritance
- Abstract Base Classes (`ABC`)
- Abstract Methods
- Static Methods
- Encapsulation through class design
- Object Interaction

## 💾 Data Storage

The application uses a JSON file to maintain student and book records.

The data is automatically updated whenever a registration, issue, return, edit, or delete operation is performed.

## 🎯 Learning Objectives

This project was developed to strengthen practical understanding of Python programming, particularly:

- Applying OOP concepts to a real-world problem.
- Working with multiple interacting classes.
- Handling user input and exceptions.
- Implementing file handling and persistent storage.
- Building a menu-driven application.

## 🔮 Future Improvements

- Add an administrator login system.
- Implement book search functionality.
- Add due dates and late return fines.
- Maintain transaction history.
- Introduce a graphical user interface (GUI).
- Add more advanced data validation.

## 👨‍💻 Author

**Akhil Dubey**

[GitHub Profile](https://github.com/dubeyakhil1256-code)

---

*Built as a Python learning project to explore Object-Oriented Programming and file handling.*
