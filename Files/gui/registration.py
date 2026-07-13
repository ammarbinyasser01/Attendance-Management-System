import os
import sys
import customtkinter as ctk
from tkinter import messagebox

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from face.register_face import register_face
from database.database import (
    initialize_database,
    register_user,
    user_exists
)

initialize_database()


class RegistrationPage(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Attendance Management System")
        self.geometry("700x650")
        self.resizable(False, False)

        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.face_registered = False

        title = ctk.CTkLabel(
            self,
            text="Attendance Management System",
            font=("Arial", 28, "bold")
        )
        title.pack(pady=(25, 10))

        subtitle = ctk.CTkLabel(
            self,
            text="Registration",
            font=("Arial", 22)
        )
        subtitle.pack(pady=10)

        self.username = ctk.CTkEntry(
            self,
            width=350,
            placeholder_text="Username"
        )
        self.username.pack(pady=10)

        self.password = ctk.CTkEntry(
            self,
            width=350,
            placeholder_text="Password",
            show="*"
        )
        self.password.pack(pady=10)

        self.confirm_password = ctk.CTkEntry(
            self,
            width=350,
            placeholder_text="Confirm Password",
            show="*"
        )
        self.confirm_password.pack(pady=10)

        self.role = ctk.CTkOptionMenu(
            self,
            values=["Teacher", "Student"],
            width=350
        )
        self.role.pack(pady=10)

        self.face_button = ctk.CTkButton(
            self,
            text="Register Face",
            width=250,
            command=self.capture_face
        )
        self.face_button.pack(pady=(20, 10))

        self.face_status = ctk.CTkLabel(
            self,
            text="Face Not Registered",
            text_color="red",
            font=("Arial", 14)
        )
        self.face_status.pack()

        button_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        button_frame.pack(pady=40)

        self.login_button = ctk.CTkButton(
            button_frame,
            text="Login",
            width=150,
            command=self.open_login
        )
        self.login_button.grid(row=0, column=0, padx=15)

        self.register_button = ctk.CTkButton(
            button_frame,
            text="Register",
            width=150,
            command=self.register_user_account
        )
        self.register_button.grid(row=0, column=1, padx=15)

    # =====================================

    def capture_face(self):

        username = self.username.get().strip()

        if username == "":

            messagebox.showerror(
                "Error",
                "Enter Username First."
            )

            return

        success = register_face(username)

        if success:

            self.face_registered = True

            self.face_status.configure(
                text="✓ Face Registered Successfully",
                text_color="green"
            )

        else:

            self.face_registered = False

            self.face_status.configure(
                text="Face Not Registered",
                text_color="red"
            )

    # =====================================

    def register_user_account(self):

        username = self.username.get().strip()

        password = self.password.get().strip()

        confirm = self.confirm_password.get().strip()

        role = self.role.get()

        if username == "" or password == "" or confirm == "":

            messagebox.showerror(
                "Error",
                "Fill all fields."
            )

            return

        if password != confirm:

            messagebox.showerror(
                "Error",
                "Passwords do not match."
            )

            return

        if not self.face_registered:

            messagebox.showerror(
                "Error",
                "Register your face first."
            )

            return

        if user_exists(username):

            messagebox.showerror(
                "Error",
                "Username already exists."
            )

            return

        try:

            register_user(
                username,
                password,
                role
            )

            messagebox.showinfo(
                "Success",
                "Registration Successful."
            )

            self.destroy()

            from gui.login import LoginPage

            app = LoginPage()

            app.mainloop()

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )

    # =====================================

    def open_login(self):

        self.destroy()

        from gui.login import LoginPage

        app = LoginPage()

        app.mainloop()


if __name__ == "__main__":

    app = RegistrationPage()

    app.mainloop()