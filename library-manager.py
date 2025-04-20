import streamlit as st
import json
import os

class BookCollection:
    def __init__(self):
        self.book_list = []
        self.storage_file = "books_data.json"
        self.read_from_file()

    def read_from_file(self):
        try:
            with open(self.storage_file, "r") as file:
                self.book_list = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.book_list = []

    def save_to_file(self):
        with open(self.storage_file, "w") as file:
            json.dump(self.book_list, file, indent=4)

    def add_book(self, title, author, year, genre, read):
        new_book = {
            "title": title,
            "author": author,
            "year": year,
            "genre": genre,
            "read": read,
        }
        self.book_list.append(new_book)
        self.save_to_file()

    def delete_book(self, title):
        self.book_list = [book for book in self.book_list if book["title"].lower() != title.lower()]
        self.save_to_file()

    def search_books(self, search_text):
        return [book for book in self.book_list if search_text in book["title"].lower() or search_text in book["author"].lower()]

    def update_book(self, original_title, updated_book):
        for i, book in enumerate(self.book_list):
            if book["title"].lower() == original_title.lower():
                self.book_list[i] = updated_book
                self.save_to_file()
                return True
        return False

    def reading_progress(self):
        total = len(self.book_list)
        read = sum(1 for book in self.book_list if book["read"])
        return read, total

book_manager = BookCollection()
st.title("📚 Personal Library Manager")

menu = ["Add Book", "View All Books", "Search Book", "Update Book", "Delete Book", "Reading Progress"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Add Book":
    st.subheader("Add a New Book")
    title = st.text_input("Book Title")
    author = st.text_input("Author")
    year = st.text_input("Publication Year")
    genre = st.text_input("Genre")
    read = st.checkbox("Have you read this book?")

    if st.button("Add Book"):
        if title and author and year and genre:
            book_manager.add_book(title, author, year, genre, read)
            st.success("Book added successfully!")
        else:
            st.error("Please fill all fields.")

elif choice == "View All Books":
    st.subheader("Your Book Collection")
    if not book_manager.book_list:
        st.info("Your collection is empty.")
    else:
        for i, book in enumerate(book_manager.book_list, 1):
            st.markdown(f"**{i}. {book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - {'Read' if book['read'] else 'Unread'}")

elif choice == "Search Book":
    st.subheader("Search Book")
    search_term = st.text_input("Enter title or author to search").lower()
    if search_term:
        results = book_manager.search_books(search_term)
        if results:
            for book in results:
                st.write(f"{book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {'Read' if book['read'] else 'Unread'}")
        else:
            st.warning("No matching books found.")

elif choice == "Update Book":
    st.subheader("Update Book Details")
    titles = [book["title"] for book in book_manager.book_list]
    book_to_edit = st.selectbox("Select Book to Edit", titles)

    if book_to_edit:
        book = next((b for b in book_manager.book_list if b["title"] == book_to_edit), None)
        if book:
            title = st.text_input("Book Title", value=book["title"])
            author = st.text_input("Author", value=book["author"])
            year = st.text_input("Year", value=book["year"])
            genre = st.text_input("Genre", value=book["genre"])
            read = st.checkbox("Read", value=book["read"])

            if st.button("Update Book"):
                updated_book = {"title": title, "author": author, "year": year, "genre": genre, "read": read}
                if book_manager.update_book(book_to_edit, updated_book):
                    st.success("Book updated successfully!")

elif choice == "Delete Book":
    st.subheader("Delete a Book")
    titles = [book["title"] for book in book_manager.book_list]
    book_to_delete = st.selectbox("Select Book to Delete", titles)
    if st.button("Delete Book"):
        book_manager.delete_book(book_to_delete)
        st.success("Book deleted successfully!")

elif choice == "Reading Progress":
    st.subheader("Reading Progress")
    read, total = book_manager.reading_progress()
    if total > 0:
        percent = (read / total) * 100
        st.write(f"You have read {read} out of {total} books. ({percent:.2f}% complete)")
        st.progress(int(percent))
    else:
        st.info("No books in your collection yet.")
