import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from attendance.teacher_attendance import TeacherAttendance

# Project Root
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from database.database import connect_database


# ==========================================
# COLOR / FONT PALETTE
# ==========================================

BG_COLOR = "#1a1d2e"
CARD_COLOR = "#242840"
CARD_COLOR_LIGHT = "#2c3150"
ACCENT_COLOR = "#5b8def"
ACCENT_HOVER = "#4a76d1"
DANGER_COLOR = "#e5566d"
DANGER_HOVER = "#c74558"
TEXT_COLOR = "#f2f3f7"
SUBTEXT_COLOR = "#a3a8c2"

FONT_FAMILY = "Segoe UI"


class TeacherDashboard(ctk.CTk):

    def __init__(self, username):

        super().__init__()

        self.username = username

        self.title("Teacher Dashboard")
        self.geometry("1100x700")
        self.resizable(False, False)

        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.configure(fg_color=BG_COLOR)

        # ==========================================
        # Header
        # ==========================================

        header = ctk.CTkFrame(
            self,
            fg_color=CARD_COLOR,
            corner_radius=14
        )
        header.pack(fill="x", padx=16, pady=(16, 8))

        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.pack(side="left", padx=20, pady=15)

        title = ctk.CTkLabel(
            title_frame,
            text="\U0001F4DA  Teacher Dashboard",
            font=(FONT_FAMILY, 26, "bold"),
            text_color=TEXT_COLOR
        )
        title.pack(anchor="w")

        self.user_label = ctk.CTkLabel(
            title_frame,
            text=f"Welcome back, {username}",
            font=(FONT_FAMILY, 14),
            text_color=SUBTEXT_COLOR
        )
        self.user_label.pack(anchor="w", pady=(2, 0))

        self.logout_btn = ctk.CTkButton(
            header,
            text="Logout",
            width=110,
            height=38,
            corner_radius=8,
            fg_color=DANGER_COLOR,
            hover_color=DANGER_HOVER,
            font=(FONT_FAMILY, 13, "bold"),
            command=self.logout
        )
        self.logout_btn.pack(side="right", padx=(0, 16), pady=15)

        self.back_btn = ctk.CTkButton(
            header,
            text="\u2190 Back",
            width=110,
            height=38,
            corner_radius=8,
            fg_color="transparent",
            border_width=1,
            border_color=SUBTEXT_COLOR,
            hover_color=CARD_COLOR_LIGHT,
            font=(FONT_FAMILY, 13, "bold"),
            text_color=TEXT_COLOR,
            command=self.go_back
        )
        self.back_btn.pack(side="right", padx=6, pady=15)

        # ==========================================
        # Notebook styling
        # ==========================================

        style = ttk.Style()
        style.theme_use("default")

        style.configure(
            "TNotebook",
            background=BG_COLOR,
            borderwidth=0
        )
        style.configure(
            "TNotebook.Tab",
            background=CARD_COLOR,
            foreground=SUBTEXT_COLOR,
            padding=(18, 10),
            font=(FONT_FAMILY, 12, "bold"),
            borderwidth=0
        )
        style.map(
            "TNotebook.Tab",
            background=[("selected", ACCENT_COLOR)],
            foreground=[("selected", "#ffffff")]
        )

        style.configure(
            "Treeview",
            background=CARD_COLOR_LIGHT,
            fieldbackground=CARD_COLOR_LIGHT,
            foreground=TEXT_COLOR,
            rowheight=32,
            borderwidth=0,
            font=(FONT_FAMILY, 11)
        )
        style.configure(
            "Treeview.Heading",
            background=ACCENT_COLOR,
            foreground="#ffffff",
            font=(FONT_FAMILY, 12, "bold"),
            borderwidth=0,
            relief="flat"
        )
        style.map(
            "Treeview",
            background=[("selected", ACCENT_COLOR)],
            foreground=[("selected", "#ffffff")]
        )
        style.map(
            "Treeview.Heading",
            background=[("active", ACCENT_HOVER)]
        )

        self.tabs = ttk.Notebook(self)

        self.tabs.pack(
            fill="both",
            expand=True,
            padx=16,
            pady=8
        )

        self.course_tab = ctk.CTkFrame(self.tabs, fg_color=BG_COLOR)
        self.attendance_tab = ctk.CTkFrame(self.tabs, fg_color=BG_COLOR)
        self.feedback_tab = ctk.CTkFrame(self.tabs, fg_color=BG_COLOR)

        self.tabs.add(
            self.course_tab,
            text="  \U0001F4D6  Course  "
        )

        self.tabs.add(
            self.attendance_tab,
            text="  \U0001F4CB  Attendance  "
        )

        self.tabs.add(
            self.feedback_tab,
            text="  \U0001F4AC  User Feedback  "
        )

        self.tabs.bind(
            "<<NotebookTabChanged>>",
            self.tab_changed
        )

        # ==========================================
        # COURSE TAB
        # ==========================================

        course_card = ctk.CTkFrame(
            self.course_tab,
            fg_color=CARD_COLOR,
            corner_radius=14
        )
        course_card.pack(fill="both", expand=True, padx=20, pady=20)

        course_title = ctk.CTkLabel(
            course_card,
            text="Enrolled Courses",
            font=(FONT_FAMILY, 18, "bold"),
            text_color=TEXT_COLOR
        )
        course_title.pack(anchor="w", padx=20, pady=(18, 10))

        table_wrap = ctk.CTkFrame(course_card, fg_color="transparent")
        table_wrap.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        columns = (
            "sr",
            "course",
            "instructor",
            "email"
        )

        self.course_table = ttk.Treeview(
            table_wrap,
            columns=columns,
            show="headings",
            height=15
        )

        self.course_table.heading(
            "sr",
            text="Sr No"
        )

        self.course_table.heading(
            "course",
            text="Course Name"
        )

        self.course_table.heading(
            "instructor",
            text="Instructor"
        )

        self.course_table.heading(
            "email",
            text="Instructor Email"
        )

        self.course_table.column(
            "sr",
            width=80,
            anchor="center"
        )

        self.course_table.column(
            "course",
            width=300,
            anchor="center"
        )

        self.course_table.column(
            "instructor",
            width=220,
            anchor="center"
        )

        self.course_table.column(
            "email",
            width=320,
            anchor="center"
        )

        scrollbar = ttk.Scrollbar(
            table_wrap,
            orient="vertical",
            command=self.course_table.yview
        )
        self.course_table.configure(yscrollcommand=scrollbar.set)

        self.course_table.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(side="right", fill="y")

        self.course_table.tag_configure(
            "oddrow", background=CARD_COLOR_LIGHT
        )
        self.course_table.tag_configure(
            "evenrow", background=CARD_COLOR
        )

        self.load_course()

        # ==========================================
        # ATTENDANCE TAB
        # ==========================================

        attendance_card = ctk.CTkFrame(
            self.attendance_tab,
            fg_color=CARD_COLOR,
            corner_radius=14
        )
        attendance_card.pack(fill="both", expand=True, padx=20, pady=20)

        attendance_title = ctk.CTkLabel(
            attendance_card,
            text="Attendance",
            font=(FONT_FAMILY, 18, "bold"),
            text_color=TEXT_COLOR
        )
        attendance_title.pack(anchor="w", padx=20, pady=(18, 10))

        self.teacher_attendance = TeacherAttendance(
            attendance_card
        )

        self.teacher_attendance.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )

        # ==========================================
        # USER FEEDBACK TAB
        # ==========================================

        feedback_card = ctk.CTkFrame(
            self.feedback_tab,
            fg_color=CARD_COLOR,
            corner_radius=14
        )
        feedback_card.pack(fill="both", expand=True, padx=20, pady=20)

        feedback_title = ctk.CTkLabel(
            feedback_card,
            text="\U0001F4E2  Institute Feedback",
            font=(FONT_FAMILY, 20, "bold"),
            text_color=TEXT_COLOR
        )

        feedback_title.pack(pady=(24, 4))

        feedback_subtitle = ctk.CTkLabel(
            feedback_card,
            text="Share your thoughts, suggestions or concerns with the institute.",
            font=(FONT_FAMILY, 13),
            text_color=SUBTEXT_COLOR
        )
        feedback_subtitle.pack(pady=(0, 16))

        self.feedback_box = ctk.CTkTextbox(
            feedback_card,
            width=700,
            height=250,
            corner_radius=10,
            fg_color=CARD_COLOR_LIGHT,
            border_width=1,
            border_color=ACCENT_COLOR,
            font=(FONT_FAMILY, 13)
        )

        self.feedback_box.pack(pady=10)

        self.submit_feedback_btn = ctk.CTkButton(
            feedback_card,
            text="Submit Feedback",
            width=220,
            height=42,
            corner_radius=8,
            fg_color=ACCENT_COLOR,
            hover_color=ACCENT_HOVER,
            font=(FONT_FAMILY, 14, "bold"),
            command=self.submit_feedback
        )

        self.submit_feedback_btn.pack(pady=16)

    # ==========================================
    # LOAD COURSE
    # ==========================================

    def load_course(self):

        self.course_table.delete(
            *self.course_table.get_children()
        )

        rows = [
            (
                1,
                "Artificial Intelligence",
                "Dr. Ahmed",
                "ahmed@university.edu"
            )
        ]

        for index, row in enumerate(rows):
            tag = "evenrow" if index % 2 == 0 else "oddrow"
            self.course_table.insert(
                "",
                "end",
                values=row,
                tags=(tag,)
            )

    # ==========================================
    # TAB CHANGED
    # ==========================================

    def tab_changed(self, event):
        selected = self.tabs.tab(
            self.tabs.select(),
            "text"
        ).strip()

        if "Attendance" not in selected:
              return

        try:
            from face.recognize_face import verify_face

            verified = verify_face(self.username)

        except Exception as error:

            messagebox.showerror(
                "Face Verification Unavailable",
                "Face verification could not be started.\n\n"
                f"Reason: {error}\n\n"
                "Please make sure the face recognition module "
                "and its dependencies (e.g. deepface, opencv, "
                "tensorflow) are installed, and that a webcam "
                "is available."
            )

            self.tabs.select(0)
            return

        if not verified:
             messagebox.showerror(
            "Verification Failed",
            "Face verification failed."
        )
             self.tabs.select(0)

    # ==========================================
    # SUBMIT FEEDBACK
    # ==========================================

    def submit_feedback(self):

        feedback = self.feedback_box.get(
            "1.0",
            "end"
        ).strip()

        if feedback == "":

            messagebox.showerror(
                "Error",
                "Please enter feedback."
            )

            return

        connection, cursor = connect_database()

        cursor.execute(
            """
            INSERT INTO feedback(username, feedback)
            VALUES(?,?)
            """,
            (
                self.username,
                feedback
            )
        )

        connection.commit()
        connection.close()

        self.feedback_box.delete(
            "1.0",
            "end"
        )

        messagebox.showinfo(
            "Success",
            "Feedback submitted successfully."
        )

    # ==========================================
    # BACK
    # ==========================================

    def go_back(self):

        self.destroy()

        from gui.login import LoginPage

        app = LoginPage()

        app.mainloop()

    # ==========================================
    # LOGOUT
    # ==========================================

    def logout(self):

        self.destroy()

        from gui.login import LoginPage

        app = LoginPage()

        app.mainloop()


if __name__ == "__main__":

    app = TeacherDashboard("Teacher")

    app.mainloop()