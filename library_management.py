import csv
from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime, timedelta
import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class LibraryManagement:
    def __init__(self, root, current_user):
        self.root = root
        self.current_user = current_user
        self.root.title("Library Management System")
        self.root.configure(bg="#e0f7fa")

        # Title Label
        lbltitle = Label(self.root, text="LIBRARY MANAGEMENT SYSTEM", bg="#00838f", fg="white", bd=10, 
                         relief=RIDGE, font=("Arial", 28, "bold"), padx=10, pady=10)
        lbltitle.pack(side=TOP, fill=X)

        # Main Frame
        self.main_frame = Frame(self.root, bd=8, relief=RIDGE, padx=15, bg="#e0f7fa")
        self.main_frame.pack(fill=BOTH, expand=True)

        # Library Membership Information Frame
        DataFrameLeft = LabelFrame(self.main_frame, text="Library Membership Information", bg="#e0f7fa", 
                                   fg="#00695c", bd=8, relief=RIDGE, font=("Arial", 16, "bold"), padx=10, pady=10)
        DataFrameLeft.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Member Type
        lblMember = Label(DataFrameLeft, bg="#e0f7fa", text="Member Type", font=("Arial", 16, "bold"), padx=2, pady=6)
        lblMember.grid(row=0, column=0, sticky=W)
        self.comMember = ttk.Combobox(DataFrameLeft, font=("Arial", 16, "bold"), width=22)
        self.comMember["value"] = ("Admin Staff", "Student", "Lecturer")
        self.comMember.grid(row=0, column=1)

        # Card ID
        lblCard_ID = Label(DataFrameLeft, bg="#e0f7fa", text="Card ID", font=("Arial", 16, "bold"), padx=2, pady=6)
        lblCard_ID.grid(row=1, column=0, sticky=W)
        self.txtCard_ID = Entry(DataFrameLeft, font=("Arial", 15, "bold"), width=22)
        self.txtCard_ID.grid(row=1, column=1, padx=2, pady=6)

        # Other Member Details
        self.entry_fields = {}
        details = [
            ("First Name:", "FirstName"),
            ("Last Name:", "LastName"),
            ("Email:", "Email"),
            ("Address:", "Address"),
            ("Mobile:", "Mobile")
        ]
        for i, (label_text, var_name) in enumerate(details):
            lbl = Label(DataFrameLeft, text=label_text, font=("Arial", 12, "bold"), padx=2, pady=4, bg="#e0f7fa")
            lbl.grid(row=i + 2, column=0, sticky=W)
            txt = Entry(DataFrameLeft, font=("Arial", 12), width=22)
            txt.grid(row=i + 2, column=1)
            self.entry_fields[var_name] = txt

        # Book Details
        book_details = [
            ("Book ID:", "BookID"),
            ("Book Title:", "BookTitle"),
            ("Author:", "Author"),
            ("Date Borrowed:", "DateBorrowed"),
            ("Date Due:", "DateDue")
        ]
        self.book_entry_fields = {}
        for i, (label_text, var_name) in enumerate(book_details):
            lbl = Label(DataFrameLeft, text=label_text, font=("Arial", 12, "bold"), padx=2, pady=4, bg="#e0f7fa")
            lbl.grid(row=i + 2, column=2, sticky=W)
            if var_name == "DateBorrowed":
                self.book_entry_fields[var_name] = DateEntry(DataFrameLeft, font=("Arial", 12), width=22)
            else:
                txt = Entry(DataFrameLeft, font=("Arial", 12), width=22)
                self.book_entry_fields[var_name] = txt
            self.book_entry_fields[var_name].grid(row=i + 2, column=3)

        self.book_entry_fields['DateBorrowed'].bind("<<DateEntrySelected>>", self.calculate_due_date)

        # Book Details Frame
        DataFrameRight = LabelFrame(self.main_frame, text="Book Details", bg="#e0f7fa", fg="#00695c", 
                                    bd=8, relief=RIDGE, font=("Arial", 16, "bold"), padx=10, pady=10)
        DataFrameRight.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        listScrollbar = Scrollbar(DataFrameRight)
        listScrollbar.grid(row=0, column=1, sticky="ns")

        self.listBox = Listbox(DataFrameRight, font=("Arial", 12), width=32, height=16)
        self.listBox.grid(row=0, column=0, padx=4, sticky="nsew")
        listScrollbar.config(command=self.listBox.yview)
        self.listBox.config(yscrollcommand=listScrollbar.set)

        self.books_info = []  # List to hold tuples of (BookID, BookTitle, Author)
        self.load_books_from_csv('Books.csv')  # Update with your actual file path

        for book in self.books_info:
            self.listBox.insert(END, book[1])  # Add book title to the Listbox

        self.listBox.bind('<<ListboxSelect>>', self.on_book_select)

        # Search Frame for Book Title and Book ID
        self.search_combined_var = StringVar()
        search_combined_frame = Frame(DataFrameRight, bg="#e0f7fa")
        search_combined_frame.grid(row=1, column=0, columnspan=2, pady=10)

        search_combined_entry = Entry(search_combined_frame, textvariable=self.search_combined_var, font=("Arial", 12), width=25)
        search_combined_entry.grid(row=0, column=0, padx=5)

        search_combined_button = Button(search_combined_frame, text="Search by Title or ID", command=self.search_book_combined, font=("Arial", 12, "bold"), bg="#00796b", fg="white")
        search_combined_button.grid(row=0, column=1, padx=5)

        # Button Frame
        framebutton = Frame(self.root, bd=8, relief=RIDGE, padx=15, bg="#e0f7fa")
        framebutton.pack(fill=X, padx=10, pady=10)

        buttons = ["Add Data", "Show Data", "Edit Data", "Delete", "Reset", "Exit"]
        for i, btn_text in enumerate(buttons):
            button = Button(framebutton, text=btn_text, font=("Arial", 12, "bold"), width=10, bg="#00796b", fg="white")
            button.grid(row=0, column=i, padx=5)
            if btn_text == "Add Data":
                button.config(command=self.add_data)
            elif btn_text == "Show Data":
                button.config(command=self.show_data)
            elif btn_text == "Edit Data":
                button.config(command=self.edit_data)
            elif btn_text == "Delete":
                button.config(command=self.delete_data)
            elif btn_text == "Reset":
                button.config(command=self.reset_data)
            elif btn_text == "Exit":
                button.config(command=self.on_closing)

        # Details Frame
        framedetails = Frame(self.root, bd=8, relief=RIDGE, padx=15, bg="#e0f7fa")
        framedetails.pack(fill=BOTH, expand=True, padx=10, pady=10)

        Table_frame = Frame(framedetails, bd=6, relief=RIDGE, bg="#e0f7fa")
        Table_frame.pack(fill=BOTH, expand=True)

        xscroll = ttk.Scrollbar(Table_frame, orient=HORIZONTAL)
        yscroll = ttk.Scrollbar(Table_frame, orient=VERTICAL)

        self.library_table = ttk.Treeview(Table_frame, columns=("membertype", "card_id", "firstname", "lastname", 
                                                                "email", "address", "mobile", "bookid", 
                                                                "booktitle", "author", "dateborrowed", "datedue"), 
                                           xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)

        xscroll.pack(side=BOTTOM, fill=X)
        yscroll.pack(side=RIGHT, fill=Y)

        xscroll.config(command=self.library_table.xview)
        yscroll.config(command=self.library_table.yview)

        # Set column headings and widths
        column_widths = {
            "membertype": 100,
            "card_id": 80,
            "firstname": 100,
            "lastname": 100,
            "email": 150,
            "address": 150,
            "mobile": 100,
            "bookid": 80,
            "booktitle": 150,
            "author": 100,
            "dateborrowed": 100,
            "datedue": 100
        }

        for col in self.library_table["columns"]:
            self.library_table.heading(col, text=col.capitalize())
            self.library_table.column(col, width=column_widths[col])

        self.library_table["show"] = "headings"
        self.library_table.pack(fill=BOTH, expand=True)

        self.load_data()  # Load previously saved data

    def calculate_due_date(self, event):
        borrowed_date_str = self.book_entry_fields['DateBorrowed'].get()
        if borrowed_date_str:
            borrowed_date = datetime.strptime(borrowed_date_str, '%m/%d/%y')
            due_date = borrowed_date + timedelta(days=14)
            self.book_entry_fields['DateDue'].delete(0, END)
            self.book_entry_fields['DateDue'].insert(0, due_date.strftime('%m/%d/%y'))

    def on_book_select(self, event):
        selected_index = self.listBox.curselection()
        if selected_index:
            selected_title = self.listBox.get(selected_index)
            for book in self.books_info:
                if book[1] == selected_title:  # Check if book title matches
                    # Populate the Book ID, Title, and Author fields
                    self.book_entry_fields['BookID'].delete(0, END)
                    self.book_entry_fields['BookID'].insert(0, book[0])  # Book ID
                    self.book_entry_fields['BookTitle'].delete(0, END)
                    self.book_entry_fields['BookTitle'].insert(0, book[1])  # Book Title
                    self.book_entry_fields['Author'].delete(0, END)
                    self.book_entry_fields['Author'].insert(0, book[2])  # Author
                    break

    def search_book_combined(self):
        search_term = self.search_combined_var.get().strip()
        self.listBox.delete(0, END)  # Clear current list
        found = False
        
        for book in self.books_info:
            if search_term.lower() in book[1].lower() or search_term == book[0]:  # Search by book title or BookID
                self.listBox.insert(END, book[1])  # Add book title to the Listbox
                found = True
        
        if not found:
            messagebox.showinfo("Search Result", "No book found with the given Title or Book ID.")

    def send_email(self, recipient_email, subject, body):
        sender_email = "sokengyom3ng@gmail.com"  # Replace with your email
        sender_password = "hqvq efbx pyca fudx"        # Replace with your email password or app password

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(msg)
                print("Email sent successfully!")
        except Exception as e:
            print(f"Failed to send email: {e}")

    def add_data(self):
        member_type = self.comMember.get()
        card_id = self.txtCard_ID.get()
        data = {key: entry.get() for key, entry in self.entry_fields.items()}
        book_data = {key: entry.get() for key, entry in self.book_entry_fields.items()}

        recipient_email = data.get('Email')

        if member_type and card_id and all(data.values()) and all(book_data.values()):
            # Ensure the tuple matches the Treeview column order
            row = (member_type, card_id, data['FirstName'], data['LastName'], 
                recipient_email, data['Address'], data['Mobile'], 
                book_data['BookID'], book_data['BookTitle'], book_data['Author'], 
                book_data['DateBorrowed'], book_data['DateDue'])

            self.library_table.insert('', 'end', values=row)
            self.reset_data()  # Reset fields after adding data
            messagebox.showinfo("Success", "Data added successfully.")

            email_body = f"""
            Dear {data['FirstName']} {data['LastName']},

            Thank you for choosing our library! We are pleased to inform you that the following book has been successfully reserved in your name:

            **Transaction Details:**
            - **Borrower Name:** {data['FirstName']} {data['LastName']}
            - **Card ID:** {card_id}
            - **Book Title:** {book_data['BookTitle']}
            - **Book ID:** {book_data['BookID']}
            - **Author:** {book_data['Author']}
            - **Date Borrowed:** {book_data['DateBorrowed']}
            - **Due Date:** {book_data['DateDue']}

            We hope you enjoy your reading. If you have any questions or require further assistance, please feel free to contact us.

            Thank you for being a valued member of our library!

            Best regards,
            Library Management Team
            """

            # Send email using the email from the form
            self.send_email(recipient_email, "Library Book Reservation", email_body)
            self.save_data()  # Save data to the file
        else:
            messagebox.showerror("Error", "Please fill all fields.")

    def show_data(self):
        selected_item = self.library_table.selection()
        if selected_item:
            item_data = self.library_table.item(selected_item, 'values')
            data_window = Toplevel(self.root)
            data_window.title("Selected Data")

            for i, (col_name, value) in enumerate(zip(self.library_table["columns"], item_data)):
                lbl = Label(data_window, text=f"{col_name.capitalize()}: {value}", font=("Arial", 12))
                lbl.pack(pady=5)

            close_button = Button(data_window, text="Close", command=data_window.destroy, bg="#00796b", fg="white")
            close_button.pack(pady=10)
        else:
            messagebox.showerror("Error", "Please select a row to view details.")

    def edit_data(self):
        selected_item = self.library_table.selection()
        if selected_item:
            item_data = self.library_table.item(selected_item, 'values')
            edit_window = Toplevel(self.root)
            edit_window.title("Edit Data")

            entries = {}
            for i, (col_name, value) in enumerate(zip(self.library_table["columns"], item_data)):
                lbl = Label(edit_window, text=f"{col_name.capitalize()}:", font=("Arial", 12))
                lbl.grid(row=i, column=0, sticky=W, pady=5)

                entry = Entry(edit_window, font=("Arial", 12), width=30)
                entry.grid(row=i, column=1, pady=5)
                entry.insert(0, value)
                entries[col_name] = entry

            def save_changes():
                new_data = tuple(entry.get() for entry in entries.values())
                self.library_table.item(selected_item, values=new_data)
                edit_window.destroy()
                self.save_data()

                email_body = f"""
                Dear {new_data[2]} {new_data[3]},

                Your book borrowing details have been successfully updated. Here are the new details:

                **Updated Borrowing Information:**
                - **Member Type:** {new_data[0]}
                - **Card ID:** {new_data[1]}
                - **First Name:** {new_data[2]}
                - **Last Name:** {new_data[3]}
                - **Email:** {new_data[4]}
                - **Address:** {new_data[5]}
                - **Mobile:** {new_data[6]}
                - **Book ID:** {new_data[7]}
                - **Book Title:** {new_data[8]}
                - **Author:** {new_data[9]}
                - **Date Borrowed:** {new_data[10]}
                - **Due Date:** {new_data[11]}

                If you have any questions or need further assistance, please feel free to contact us.

                Thank you for being a valued member of our library!

                Best regards,
                Library Management Team
                """

                recipient_email = new_data[4]  # Assuming the email is in the 5th column
                self.send_email(recipient_email, "Library Membership Updated", email_body)

            save_button = Button(edit_window, text="Save", command=save_changes, bg="#00796b", fg="white")
            save_button.grid(row=len(item_data), column=0, columnspan=2, pady=10)
        else:
            messagebox.showerror("Error", "Please select a row to edit.")

    def delete_data(self):
        selected_item = self.library_table.selection()
        if selected_item:
            self.library_table.delete(selected_item)
            messagebox.showinfo("Success", "Data deleted successfully.")
            self.save_data()
        else:
            messagebox.showerror("Error", "Please select a row to delete.")

    def reset_data(self):
        self.comMember.set('')
        self.txtCard_ID.delete(0, END)
        for entry in self.entry_fields.values():
            entry.delete(0, END)
        for entry in self.book_entry_fields.values():
            entry.delete(0, END)
        self.listBox.delete(0, END)
        self.search_combined_var.set('')

    def load_books_from_csv(self, filename):
        if os.path.exists(filename):
            with open(filename, mode='r') as file:
                reader = csv.reader(file)
                self.books_info = [tuple(row) for row in reader]

    def load_data(self):
        if os.path.exists("members.json"):
            with open("members.json", "r") as file:
                        data = json.load(file)
            for entry in data:
                self.library_table.insert('', 'end', values=entry)

    def save_data(self):
        data = []
        for row in self.library_table.get_children():
            data.append(self.library_table.item(row)['values'])
        with open("members.json", "w") as file:
            json.dump(data, file)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()