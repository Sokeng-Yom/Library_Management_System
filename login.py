import json
from tkinter import Frame, Label, Entry, Button, messagebox
from library_management import LibraryManagement
import os
class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("500x400")

        self.current_user = None
        self.load_users()

        self.login_frame = Frame(self.root)
        self.login_frame.pack(fill="both", expand=True)

        self.create_login_frame()

    def load_users(self):
        if os.path.exists('users.json'):
            with open('users.json', 'r') as f:
                self.users = json.load(f)
        else:
            self.users = {}

    def save_users(self):
        with open('users.json', 'w') as f:
            json.dump(self.users, f)

    def create_login_frame(self):
        for widget in self.login_frame.winfo_children():
            widget.destroy()

        lbltitle = Label(self.login_frame, text="Login", font=("Times New Roman", 20, "bold"))
        lbltitle.pack(pady=20)

        lblUser = Label(self.login_frame, text="Username:", font=("Times New Roman", 12))
        lblUser.pack(pady=5)
        self.username_login = Entry(self.login_frame, font=("Times New Roman", 12))
        self.username_login.pack(pady=5)

        lblPass = Label(self.login_frame, text="Password:", font=("Times New Roman", 12))
        lblPass.pack(pady=5)
        self.password_login = Entry(self.login_frame, show="*", font=("Times New Roman", 12))
        self.password_login.pack(pady=5)

        btnLogin = Button(self.login_frame, text="Login", command=self.login, font=("Times New Roman", 12))
        btnLogin.pack(pady=20)

        lblSignUp = Label(self.login_frame, text="Don't have an account? Sign Up", fg="blue", cursor="hand2", font=("Times New Roman", 10))
        lblSignUp.pack(pady=10)
        lblSignUp.bind("<Button-1>", lambda e: self.create_signup_frame())

    def create_signup_frame(self):
        for widget in self.login_frame.winfo_children():
            widget.destroy()

        lbltitle = Label(self.login_frame, text="Sign Up", font=("Times New Roman", 20, "bold"))
        lbltitle.pack(pady=20)

        lblUser = Label(self.login_frame, text="Username:", font=("Times New Roman", 12))
        lblUser.pack(pady=5)
        self.username_signup = Entry(self.login_frame, font=("Times New Roman", 12))
        self.username_signup.pack(pady=5)

        lblPass = Label(self.login_frame, text="Password:", font=("Times New Roman", 12))
        lblPass.pack(pady=5)
        self.password_signup = Entry(self.login_frame, show="*", font=("Times New Roman", 12))
        self.password_signup.pack(pady=5)

        btnSignUp = Button(self.login_frame, text="Sign Up", command=self.signup, font=("Times New Roman", 12))
        btnSignUp.pack(pady=20)

    def signup(self):
        username = self.username_signup.get()
        password = self.password_signup.get()

        if username in self.users:
            messagebox.showerror("Error", "Username already exists!")
        elif not username or not password:
            messagebox.showerror("Error", "Please enter both username and password!")
        else:
            self.users[username] = password
            self.save_users()
            messagebox.showinfo("Success", "Sign Up successful!")
            self.current_user = username
            self.login_frame.destroy()
            self.open_library_management()

    def login(self):
        username = self.username_login.get()
        password = self.password_login.get()

        if username in self.users and self.users[username] == password:
            self.current_user = username
            self.login_frame.destroy()
            self.open_library_management()
        else:
            messagebox.showerror("Error", "Invalid username or password!")

    def open_library_management(self):
        self.login_frame.pack_forget()
        from library_management import LibraryManagement
        LibraryManagement(self.root, self.current_user)