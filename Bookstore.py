import sqlite3

# Connect to the database
conn = sqlite3.connect('ebookstore.db')
cursor = conn.cursor()

# Check if the table 'ebooks' already exists
cursor.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='ebooks' ''')

# If the table already exists
if cursor.fetchone()[0] > 0:
    # Print the existing table
    cursor.execute('SELECT * FROM ebooks')
    rows = cursor.fetchall()

else:
    # Create the table
    cursor.execute('''CREATE TABLE ebooks (ID INTEGER PRIMARY KEY, Title TEXT, Author TEXT, Qty INTEGER)''')
    # Insert the rows
    cursor.execute('''INSERT INTO ebooks (ID, Title, Author, Qty) VALUES (3001, 
    A Tale of Two Cities, Charles Dickens, 30)''')
    cursor.execute('''INSERT INTO ebooks (ID, Title, Author, Qty) VALUES (3002, 
    Harry Potter and the Philosopher's Stone, J.K. Rowling, 40)''')
    cursor.execute('''INSERT INTO ebooks (ID, Title, Author, Qty) VALUES (3003, 
    The Lion, the Witch, and the Wardrobe, C.S. Lewis, 25)''')
    cursor.execute('''INSERT INTO ebooks (ID, Title, Author, Qty) VALUES (3004, 
    The Lord of the Rings, J.R.R Tolkien, 37)''')
    cursor.execute('''INSERT INTO ebooks (ID, Title, Author, Qty) VALUES (3005, 
    Alice in Wonderland, Lewis Carroll, 12)''')

    # Save the changes
    conn.commit()

def main_menu():
    print("Welcome to KBH Books!")
    print("Please select one of the following options:")
    print("1. Enter book")
    print("2. Update book")
    print("3. Delete book")
    print("4. Search books")
    print("0. Exit")
    choice = input("Enter your choice: ")
    return choice


def enter_book():
    try:
        # Prompt the user for book information
        id = input("Enter the ID of the book: ")
        title = input("Enter the title of the book: ")
        author = input("Enter the author of the book: ")
        qty = input("Enter the quantity of the book: ")

        # Insert the book into the database
        cursor.execute('''INSERT INTO ebooks (ID, Title,Author, Qty) VALUES (?, ?, ?, ?)''', (id, title, author, qty))

        # Save the changes
        conn.commit()

        print("Book added successfully.")
    except Exception as e:
        # Roll back any changes if an error occurs
        conn.rollback()
        print("Error:", e)
        print("Book not added.")


def update_book():
    try:
        # Prompt the user for the book's ID
        id = input("Enter the ID of the book to update: ")

        # Select the book from the database
        cursor.execute('''SELECT * FROM ebooks WHERE ID=?''', (id,))
        book = cursor.fetchone()

        if book is not None:
            # Print the book's information
            print("ID:", book[0])
            print("Title:", book[1])
            print("Author:", book[2])
            print("Quantity:", book[3])

            # Prompt the user for the updated quantity
            qty = input("Enter the updated quantity: ")

            # Update the book in the database
            cursor.execute('''UPDATE ebooks SET Qty=? WHERE ID=?''', (qty, id))

            # Save the changes
            conn.commit()

            print("Book updated successfully.")
        else:
            print("Book not found.")
    except Exception as e:
        # Roll back any changes if an error occurs
        conn.rollback()
        print("Error:", e)
        print("Book not updated.")


def delete_book():
    try:
        # Prompt the user for the book's ID
        id = input("Enter the ID of the book to delete: ")

        # Select the book from the database
        cursor.execute('''SELECT * FROM ebooks WHERE ID=?''', (id,))
        book = cursor.fetchone()

        if book is not None:
            # Print the book's information
            print("ID:", book[0])
            print("Title:", book[1])
            print("Author:", book[2])
            print("Quantity:", book[3])

            # Prompt the user to confirm the deletion
            confirm = input("Are you sure you want to delete this book? (Y/N)")
            if confirm.upper() == "Y":
                # Delete the book from the database
                cursor.execute('''DELETE FROM ebooks WHERE ID=?''', (id,))

                # Save the changes
                conn.commit()

                print("Book deleted successfully.")
            else:
                print("Book not deleted.")
        else:
            print("Book not found.")
    except Exception as e:
        # Roll back any changes if an error occurs
        conn.rollback()
        print("Error:", e)
        print("Book not deleted.")


def search_books():
    try:
        # Prompt the user for a search query
        query = input("Enter an ID or title to search for: ")

        # Search the database for matching books
        cursor.execute('''SELECT * FROM ebooks WHERE ID=? OR Title=?''', (query, query))
        books = cursor.fetchall()

        if len(books) > 0:
            # Print the information for each book
            for book in books:
                print("ID:", book[0])
                print("Title:", book[1])
                print("Author:", book[2])
                print("Quantity:", book[3])
        else:
            print("No books found.")
    except Exception as e:
        print("Error:", e)
        print("No books found.")


while True:
    choice = main_menu()
    if choice == "1":
        enter_book()
    elif choice == "2":
        update_book()
    elif choice == "3":
        delete_book()
    elif choice == "4":
        search_books()
    elif choice == "0":
        break
    else:
        print("Invalid choice. Try again.")

# Close the database connection
conn.close()
