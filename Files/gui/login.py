import os
import sys
import customtkinter as ctk
from tkinter import messagebox

# Project Root
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from database.database import connect_database


class LoginPage(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Attendance Management System")
        self.geometry("700x650")
        self.resizable(False, False)

        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        # ==========================
        # Title
        # ==========================

        title = ctk.CTkLabel(
            self,
            text="Attendance Management System",
            font=("Arial", 28, "bold")
        )
        title.pack(pady=(25, 10))

        subtitle = ctk.CTkLabel(
            self,
            text="Login",
            font=("Arial", 22)
        )
        subtitle.pack(pady=10)

        # ==========================
        # Username
        # ==========================

        self.username = ctk.CTkEntry(
            self,
            width=350,
            placeholder_text="Username"
        )
        self.username.pack(pady=10)

        # ==========================
        # Password
        # ==========================

        self.password = ctk.CTkEntry(
            self,
            width=350,
            placeholder_text="Password",
            show="*"
        )
        self.password.pack(pady=10)

        # ==========================
        # Role
        # ==========================

        self.role = ctk.CTkOptionMenu(
            self,
            values=["Teacher", "Student"],
            width=350
        )
        self.role.pack(pady=10)

        # ==========================
        # Bottom Buttons
        # ==========================

        button_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        button_frame.pack(pady=40)

        self.back_button = ctk.CTkButton(
            button_frame,
            text="Back",
            width=130,
            command=self.go_back
        )

        self.back_button.grid(row=0, column=0, padx=10)

        self.login_button = ctk.CTkButton(
            button_frame,
            text="Login",
            width=130,
            command=self.login
        )

        self.login_button.grid(row=0, column=1, padx=10)

        self.forgot_button = ctk.CTkButton(
            button_frame,
            text="Forgot Password",
            width=160,
            command=self.forgot_password
        )

        self.forgot_button.grid(row=0, column=2, padx=10)

    # ==========================================
    # LOGIN
    # ==========================================

    def login(self):

        username = self.username.get().strip()

        password = self.password.get().strip()

        role = self.role.get()

        if username == "" or password == "":

            messagebox.showerror(
                "Error",
                "Fill all fields."
            )

            return

        connection, cursor = connect_database()

        cursor.execute("""
        SELECT *
        FROM users
        WHERE username=?
        AND password=?
        AND role=?
        """,
        (
            username,
            password,
            role
        ))

        user = cursor.fetchone()

        connection.close()

        if user is None:

            messagebox.showerror(
                "Login Failed",
                "Invalid Username or Password."
            )

            return

        messagebox.showinfo(
            "Success",
            f"Welcome {username}"
        )

        if role == "Teacher":

            self.destroy()
            from gui.teacher_dashboard import TeacherDashboard
            app = TeacherDashboard(username)

            app.mainloop()

        else:
             self.destroy()
            
             from gui.student_dashboard import StudentDashboard
        
             app = StudentDashboard(username)
            
             app.mainloop()

    # ==========================================
    # BACK BUTTON
    # ==========================================

    def go_back(self):

        self.destroy()

        from gui.registration import RegistrationPage

        app = RegistrationPage()

        app.mainloop()

    # ==========================================
    # FORGOT PASSWORD
    # ==========================================

    def forgot_password(self):

        from gui.forgot_password import ForgotPassword
        window = ForgotPassword()
        window.mainloop()


if __name__ == "__main__":

    app = LoginPage()

    app.mainloop()