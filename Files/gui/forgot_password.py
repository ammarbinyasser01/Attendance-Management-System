import os
import sys
import customtkinter as ctk
from tkinter import messagebox

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from face.recognize_face import recognize_face
from database.database import (
    user_exists,
    update_password
)


class ForgotPassword(ctk.CTk):

    def __init__(self):

        super().__init__()

        self.title("Forgot Password")

        self.geometry("500x450")

        self.resizable(False, False)

        self.verified = False

        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        ctk.CTkLabel(
            self,
            text="Forgot Password",
            font=("Arial", 28, "bold")
        ).pack(pady=(30,20))

        self.username = ctk.CTkEntry(
            self,
            width=320,
            placeholder_text="Username"
        )

        self.username.pack(pady=10)

        self.verify_btn = ctk.CTkButton(
            self,
            text="Verify Face",
            width=220,
            command=self.verify_face
        )

        self.verify_btn.pack(pady=20)

        self.password = ctk.CTkEntry(
            self,
            width=320,
            placeholder_text="New Password",
            show="*"
        )

        self.password.pack(pady=10)

        self.confirm = ctk.CTkEntry(
            self,
            width=320,
            placeholder_text="Confirm Password",
            show="*"
        )

        self.confirm.pack(pady=10)

        self.reset_btn = ctk.CTkButton(
            self,
            text="Reset Password",
            width=220,
            command=self.reset_password
        )

        self.reset_btn.pack(pady=25)

    # ==========================================
    # VERIFY FACE
    # ==========================================

    def verify_face(self):

        username = self.username.get().strip()

        if username == "":

            messagebox.showerror(
                "Error",
                "Enter username first."
            )

            return

        if not user_exists(username):

            messagebox.showerror(
                "Error",
                "Username does not exist."
            )

            return

        verified = recognize_face()

        if verified != username:

            messagebox.showerror(
                "Verification Failed",
                "Face does not match the username."
            )

            self.verified = False

            return

        self.verified = True

        messagebox.showinfo(
            "Success",
            "Face verified successfully."
        )

    # ==========================================
    # RESET PASSWORD
    # ==========================================

    def reset_password(self):

        username = self.username.get().strip()

        password = self.password.get().strip()

        confirm = self.confirm.get().strip()

        if not self.verified:

            messagebox.showerror(
                "Error",
                "Verify your face first."
            )

            return

        if password == "" or confirm == "":

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

        update_password(
            username,
            password
        )

        messagebox.showinfo(
            "Success",
            "Password updated successfully."
        )

        self.destroy()


if __name__ == "__main__":

    app = ForgotPassword()

    app.mainloop()