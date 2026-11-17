import json
import os
from abc import ABC, abstractmethod

import pandas as pd
import streamlit as st

# ---------------------------------------------------------------- config
st.set_page_config(page_title="Library Manager", page_icon="📚", layout="wide")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "library_data.json")


# ---------------------------------------------------------------- data layer
def load_data():
    data = {"students": [], "books": []}
    if os.path.exists(DATABASE):
        try:
            with open(DATABASE, "r") as f:
                content = f.read().strip()
                if content:
                    data = json.loads(content)
        except json.JSONDecodeError:
            st.error("Your JSON file contains invalid data.")
    data.setdefault("students", [])
    data.setdefault("books", [])
    return data


def save(data):
    with open(DATABASE, "w") as f:
        json.dump(data, f, indent=4)


# ---------------------------------------------------------------- OOP layer (same design as your original code)
class General(ABC):
    def __init__(self, data):
        self.data = data

    @abstractmethod
    def get_roles(self):
        pass

    @abstractmethod
    def register(self, **kwargs):
        pass

    @staticmethod
    def validate_email(email):
        return "@" in email and "." in email


class Persons(General):
    def get_roles(self):
        return "Person"

    def register(self, name, age, email, roll_no):
        if not name.strip() or not roll_no.strip():
            return False, "Name and roll number are required."
        if age <= 0:
            return False, "Invalid age."
        if not General.validate_email(email):
            return False, "Invalid email address."
        if any(s["roll_no"] == roll_no for s in self.data["students"]):
            return False, "Student already exists."
        self.data["students"].append(
            {"name": name.strip(), "age": age, "email": email.strip(),
             "roll_no": roll_no.strip(), "Books": []}
        )
        save(self.data)
        return True, "Student registered successfully!"

    def find(self, roll_no):
        return next((s for s in self.data["students"] if s["roll_no"] == roll_no), None)

    def add_book(self, roll_no, book_id):
        student = self.find(roll_no)
        if student is None:
            return False, "Student not found."
        book = next((b for b in self.data["books"] if b["Book_Id"] == book_id), None)
        if book is None:
            return False, "Book not found."
        if not book["available"]:
            return False, "Book is already issued."
        book["available"] = False
        student["Books"].append(book_id)
        save(self.data)
        return True, f"'{book['name']}' issued to {student['name']}."

    def return_book(self, roll_no, book_id):
        student = self.find(roll_no)
        if student is None:
            return False, "Student not found."
        if book_id not in student["Books"]:
            return False, "This student has not issued this book."
        for book in self.data["books"]:
            if book["Book_Id"] == book_id:
                book["available"] = True
                student["Books"].remove(book_id)
                save(self.data)
                return True, f"'{book['name']}' returned successfully!"
        return False, "Book not found."


class Book(General):
    def get_roles(self):
        return "Book"

    def register(self, name, author, subject, book_id):
        if not name.strip() or not book_id.strip():
            return False, "Book name and Book ID are required."
        if any(b["Book_Id"] == book_id for b in self.data["books"]):
            return False, "Book already exists."
        self.data["books"].append(
            {"name": name.strip(), "author_name": author.strip(),
             "subject": subject.strip(), "Book_Id": book_id.strip(), "available": True}
        )
        save(self.data)
        return True, f"Book '{name}' registered successfully!"

    def find(self, book_id):
        return next((b for b in self.data["books"] if b["Book_Id"] == book_id), None)

    def edit_book(self, book_id, name, author, subject):
        book = self.find(book_id)
        if book is None:
            return False, "Book not found."
        if name.strip():
            book["name"] = name.strip()
        if author.strip():
            book["author_name"] = author.strip()
        if subject.strip():
            book["subject"] = subject.strip()
        save(self.data)
        return True, "Book updated successfully!"

    def delete_book(self, book_id):
        book = self.find(book_id)
        if book is None:
            return False, "Book not found."
        if not book["available"]:
            return False, "Cannot delete a book that is currently issued."
        self.data["books"].remove(book)
        save(self.data)
        return True, "Book deleted successfully!"


# ---------------------------------------------------------------- styling
st.markdown(
    """
    <style>
    .block-container {padding-top: 2rem;}
    .hero {
        background: linear-gradient(135deg, #0ea5e9 0%, #6366f1 50%, #a855f7 100%);
        padding: 1.8rem 2rem; border-radius: 18px; color: white; margin-bottom: 1.5rem;
    }
    .hero h1 {margin: 0; font-size: 2rem; color: white;}
    .hero p {margin: .3rem 0 0; opacity: .9;}
    div[data-testid="stMetric"] {
        background: rgba(99, 102, 241, 0.08);
        border: 1px solid rgba(99, 102, 241, 0.25);
        padding: 1rem 1.2rem; border-radius: 14px;
    }
    .card {
        border: 1px solid rgba(128,128,128,.25); border-radius: 16px;
        padding: 1.2rem 1.4rem; margin-bottom: 1rem;
        background: rgba(128,128,128,.05);
    }
    .badge {
        display: inline-block; padding: .15rem .7rem; border-radius: 999px;
        background: #6366f1; color: white; font-size: .8rem; margin-right: .4rem;
    }
    .badge-green {background: #16a34a;}
    .badge-red {background: #dc2626;}
    </style>
    """,
    unsafe_allow_html=True,
)


def hero(title, subtitle):
    st.markdown(f'<div class="hero"><h1>{title}</h1><p>{subtitle}</p></div>', unsafe_allow_html=True)


def show_df(df, container=st):
    try:
        container.dataframe(df, hide_index=True, width="stretch")
    except Exception:
        container.dataframe(df, hide_index=True)


def rerun():
    if hasattr(st, "rerun"):
        st.rerun()
    else:
        st.experimental_rerun()


def result(ok, msg):
    (st.success if ok else st.error)(msg)


# ---------------------------------------------------------------- app state
data = load_data()
person = Persons(data)
book = Book(data)

student_options = {f"{s['name']} ({s['roll_no']})": s["roll_no"] for s in data["students"]}
book_options = {f"{b['name']} ({b['Book_Id']})": b["Book_Id"] for b in data["books"]}


def book_name(book_id):
    b = book.find(book_id)
    return b["name"] if b else f"(deleted book {book_id})"


with st.sidebar:
    st.markdown("## 📚 Library Manager")
    page = st.radio(
        "Navigate",
        ["📊 Dashboard", "🧑‍🎓 Register Person", "📖 Register Book",
         "📤 Issue Book", "📥 Return Book", "🔍 Person Details",
         "📚 Book Catalog", "✏️ Edit Book", "🗑️ Delete Book"],
        label_visibility="collapsed",
    )
    st.divider()
    st.caption(f"👥 {len(data['students'])} members · 📘 {len(data['books'])} books")


# ---------------------------------------------------------------- pages
if page == "📊 Dashboard":
    hero("Dashboard", "A quick overview of your library")
    total = len(data["books"])
    available = sum(1 for b in data["books"] if b["available"])
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Members", len(data["students"]))
    c2.metric("Total Books", total)
    c3.metric("Available", available)
    c4.metric("Issued", total - available)

    left, right = st.columns(2)
    with left:
        st.markdown("### 📘 Books by Subject")
        if data["books"]:
            sdf = pd.DataFrame(data["books"])
            sdf["subject"] = sdf["subject"].replace("", "Unspecified")
            st.bar_chart(sdf["subject"].value_counts())
        else:
            st.info("No books registered yet.")
    with right:
        st.markdown("### 📤 Currently Issued")
        rows = [
            {"Book": book_name(bid), "Book ID": bid, "Issued To": s["name"], "Roll No": s["roll_no"]}
            for s in data["students"] for bid in s["Books"]
        ]
        if rows:
            show_df(pd.DataFrame(rows))
        else:
            st.info("No books are issued right now.")

elif page == "🧑‍🎓 Register Person":
    hero("Register Person", "Add a new library member")
    with st.form("person_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        name = c1.text_input("Full name")
        roll_no = c2.text_input("Roll number")
        email = c1.text_input("Email")
        age = c2.number_input("Age", min_value=1, max_value=100, value=18, step=1)
        submitted = st.form_submit_button("Register", type="primary")
    if submitted:
        ok, msg = person.register(name, int(age), email, roll_no)
        result(ok, msg)
        if ok:
            st.balloons()

elif page == "📖 Register Book":
    hero("Register Book", "Add a new book to the library")
    with st.form("book_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        name = c1.text_input("Book name")
        author = c2.text_input("Author name")
        subject = c1.text_input("Subject")
        book_id = c2.text_input("Book ID")
        submitted = st.form_submit_button("Register Book", type="primary")
    if submitted:
        ok, msg = book.register(name, author, subject, book_id)
        result(ok, msg)

elif page == "📤 Issue Book":
    hero("Issue Book", "Lend an available book to a member")
    available_books = {k: v for k, v in book_options.items() if book.find(v)["available"]}
    if not data["students"]:
        st.warning("Register a member first.")
    elif not available_books:
        st.warning("No books are available to issue.")
    else:
        with st.form("issue_form"):
            s_choice = st.selectbox("Member", list(student_options.keys()))
            b_choice = st.selectbox("Book", list(available_books.keys()))
            submitted = st.form_submit_button("Issue Book", type="primary")
        if submitted:
            ok, msg = person.add_book(student_options[s_choice], available_books[b_choice])
            result(ok, msg)

elif page == "📥 Return Book":
    hero("Return Book", "Take a book back from a member")
    holders = {k: v for k, v in student_options.items() if person.find(v)["Books"]}
    if not holders:
        st.info("No member currently has an issued book.")
    else:
        s_choice = st.selectbox("Member", list(holders.keys()))
        student = person.find(holders[s_choice])
        issued = {f"{book_name(b)} ({b})": b for b in student["Books"]}
        b_choice = st.selectbox("Book to return", list(issued.keys()))
        if st.button("Return Book", type="primary"):
            ok, msg = person.return_book(student["roll_no"], issued[b_choice])
            result(ok, msg)

elif page == "🔍 Person Details":
    hero("Person Details", "Look up a member and the books they hold")
    if not data["students"]:
        st.warning("No members registered yet.")
    else:
        choice = st.selectbox("Select member", list(student_options.keys()))
        s = person.find(student_options[choice])
        if s:
            st.markdown(
                f"""<div class="card">
                <h3 style="margin-top:0">{s['name']}</h3>
                <span class="badge">Roll: {s['roll_no']}</span>
                <span class="badge">Age: {s['age']}</span>
                <span class="badge">{s['email']}</span>
                </div>""",
                unsafe_allow_html=True,
            )
            st.metric("Books Issued", len(s["Books"]))
            if s["Books"]:
                rows = []
                for bid in s["Books"]:
                    b = book.find(bid)
                    rows.append({
                        "Book ID": bid,
                        "Name": b["name"] if b else "(deleted)",
                        "Author": b["author_name"] if b else "-",
                    })
                show_df(pd.DataFrame(rows))
            else:
                st.info("This member has no books issued.")

elif page == "📚 Book Catalog":
    hero("Book Catalog", "Browse and search all books")
    if not data["books"]:
        st.warning("No books registered yet.")
    else:
        c1, c2 = st.columns([3, 1])
        search = c1.text_input("🔎 Search by name, author, subject or ID")
        status = c2.selectbox("Status", ["All", "Available", "Issued"])
        q = search.lower()
        rows = []
        for b in data["books"]:
            if q and not any(q in str(b[k]).lower() for k in ("name", "author_name", "subject", "Book_Id")):
                continue
            if status == "Available" and not b["available"]:
                continue
            if status == "Issued" and b["available"]:
                continue
            rows.append({
                "Book ID": b["Book_Id"], "Name": b["name"], "Author": b["author_name"],
                "Subject": b["subject"], "Status": "✅ Available" if b["available"] else "📤 Issued",
            })
        if rows:
            show_df(pd.DataFrame(rows))
        else:
            st.info("No books match your search.")

elif page == "✏️ Edit Book":
    hero("Edit Book", "Update a book's details. Leave a field empty to keep the old value.")
    if not data["books"]:
        st.warning("No books registered yet.")
    else:
        choice = st.selectbox("Select book", list(book_options.keys()))
        b = book.find(book_options[choice])
        st.caption(f"Current: **{b['name']}** by {b['author_name']} · {b['subject']}")
        with st.form("edit_form"):
            name = st.text_input("New book name")
            author = st.text_input("New author name")
            subject = st.text_input("New subject")
            submitted = st.form_submit_button("Save Changes", type="primary")
        if submitted:
            ok, msg = book.edit_book(b["Book_Id"], name, author, subject)
            result(ok, msg)

elif page == "🗑️ Delete Book":
    hero("Delete Book", "Remove a book from the library")
    if not data["books"]:
        st.warning("No books registered yet.")
    else:
        choice = st.selectbox("Select book", list(book_options.keys()))
        b = book.find(book_options[choice])
        if not b["available"]:
            st.error("This book is currently issued and cannot be deleted.")
        else:
            st.warning(f"You are about to delete **{b['name']}**. This cannot be undone.")
            if st.button("Delete Book", type="primary"):
                ok, msg = book.delete_book(b["Book_Id"])
                result(ok, msg)
                if ok:
                    rerun()
