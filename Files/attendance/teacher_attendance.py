import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from datetime import datetime
from attendance.attendance_graph import AttendanceGraph

from database.database import (
    get_all_students,
    attendance_exists,
    save_attendance,
    update_attendance
)


# ==========================================
# COLOR / FONT PALETTE
# ==========================================

CARD_COLOR = "#242840"
CARD_COLOR_LIGHT = "#2c3150"
ACCENT_COLOR = "#5b8def"
ACCENT_HOVER = "#4a76d1"
TEXT_COLOR = "#f2f3f7"

FONT_FAMILY = "Segoe UI"

STUDENT_NO_WIDTH = 100
NAME_WIDTH = 220
CLASS_WIDTH = 130


class TeacherAttendance(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(parent)

        self.class_count = 2

        self.columns = [
            "student_no",
            "name",
            "class_1",
            "class_2"
        ]

        # holds header label widgets, keyed by column
        self.header_widgets = {}

        # holds one entry per student:
        # {"student_no", "username", "student_no_label",
        #  "name_label", "dropdowns": {class_number: CTkOptionMenu},
        #  "vars": {class_number: StringVar}}
        self.student_rows = []

        self.build_gui()

    # =========================================
    def build_gui(self):
        self.tabs = ctk.CTkTabview(self)

        self.tabs.pack(
          fill="both",
          expand=True,
          padx=10,
          pady=10
        )
        self.tabs.add("Attendance Status")
        self.tabs.add("Graph")

        self.status_tab = self.tabs.tab("Attendance Status")
        self.graph_tab = self.tabs.tab("Graph")

        self.build_status()

        self.build_graph()

    # =========================================

    def build_status(self):

        top = ctk.CTkFrame(self.status_tab)

        top.pack(
            fill="x",
            padx=10,
            pady=10
        )

        ctk.CTkButton(
            top,
            text="+ Add Class",
            width=140,
            command=self.add_class
        ).pack(
            side="left",
            padx=10
        )

        ctk.CTkButton(
            top,
            text="Update Attendance",
            width=180,
            command=self.save_table
        ).pack(
            side="left",
            padx=10
        )

        # Scrollable grid that holds the header row + one row per student.
        self.table_frame = ctk.CTkScrollableFrame(
            self.status_tab,
            fg_color=CARD_COLOR
        )

        self.table_frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        self.build_header()

        self.load_students()

    # =========================================
    def build_graph(self):
         graph = AttendanceGraph(
             self.graph_tab
         )

         graph.pack(
             fill="both",
             expand = True
         )

    # =========================================

    def build_header(self):

        for widget in self.header_widgets.values():
            widget.destroy()

        self.header_widgets = {}

        student_no_label = ctk.CTkLabel(
            self.table_frame,
            text="Student No",
            font=(FONT_FAMILY, 13, "bold"),
            width=STUDENT_NO_WIDTH,
            fg_color=ACCENT_COLOR,
            text_color="white",
            corner_radius=6
        )
        student_no_label.grid(row=0, column=0, padx=4, pady=4, sticky="nsew")
        self.header_widgets["student_no"] = student_no_label

        name_label = ctk.CTkLabel(
            self.table_frame,
            text="Name",
            font=(FONT_FAMILY, 13, "bold"),
            width=NAME_WIDTH,
            fg_color=ACCENT_COLOR,
            text_color="white",
            corner_radius=6
        )
        name_label.grid(row=0, column=1, padx=4, pady=4, sticky="nsew")
        self.header_widgets["name"] = name_label

        for class_number in range(1, self.class_count + 1):
            self.add_header_column(class_number)

    # =========================================

    def add_header_column(self, class_number):

        column = f"class_{class_number}"

        label = ctk.CTkLabel(
            self.table_frame,
            text=f"Class {class_number}",
            font=(FONT_FAMILY, 13, "bold"),
            width=CLASS_WIDTH,
            fg_color=ACCENT_COLOR,
            text_color="white",
            corner_radius=6
        )

        label.grid(
            row=0,
            column=class_number + 1,
            padx=4,
            pady=4,
            sticky="nsew"
        )

        self.header_widgets[column] = label

    # =========================================

    def load_students(self):

        for row in self.student_rows:
            row["student_no_label"].destroy()
            row["name_label"].destroy()

            for dropdown in row["dropdowns"].values():
                dropdown.destroy()

        self.student_rows = []

        students = get_all_students()

        count = 1

        for student in students:

            username = student[0]

            self.add_student_row(count, username)

            count += 1

    # =========================================

    def add_student_row(self, count, username):

        row_index = len(self.student_rows) + 1

        student_no = str(count).zfill(3)

        no_label = ctk.CTkLabel(
            self.table_frame,
            text=student_no,
            width=STUDENT_NO_WIDTH,
            fg_color=CARD_COLOR_LIGHT,
            text_color=TEXT_COLOR,
            corner_radius=6
        )
        no_label.grid(row=row_index, column=0, padx=4, pady=3, sticky="nsew")

        name_label = ctk.CTkLabel(
            self.table_frame,
            text=username,
            width=NAME_WIDTH,
            fg_color=CARD_COLOR_LIGHT,
            text_color=TEXT_COLOR,
            corner_radius=6
        )
        name_label.grid(row=row_index, column=1, padx=4, pady=3, sticky="nsew")

        dropdowns = {}
        variables = {}

        for class_number in range(1, self.class_count + 1):
            self.add_attendance_dropdown(
                row_index,
                class_number,
                dropdowns,
                variables
            )

        self.student_rows.append({
            "student_no": student_no,
            "username": username,
            "student_no_label": no_label,
            "name_label": name_label,
            "dropdowns": dropdowns,
            "vars": variables
        })

    # =========================================

    def add_attendance_dropdown(self, row_index, class_number, dropdowns, variables):

        var = tk.StringVar(value="Present")

        dropdown = ctk.CTkOptionMenu(
            self.table_frame,
            values=["Present", "Absent"],
            variable=var,
            width=CLASS_WIDTH,
            fg_color=ACCENT_COLOR,
            button_color=ACCENT_HOVER,
            button_hover_color=ACCENT_HOVER,
            dropdown_fg_color=CARD_COLOR_LIGHT
        )

        dropdown.grid(
            row=row_index,
            column=class_number + 1,
            padx=4,
            pady=3,
            sticky="nsew"
        )

        dropdowns[class_number] = dropdown
        variables[class_number] = var

    # =========================================

    def add_class(self):

        self.class_count += 1

        self.columns.append(
            f"class_{self.class_count}"
        )

        self.add_header_column(self.class_count)

        for row_index, row in enumerate(self.student_rows, start=1):

            self.add_attendance_dropdown(
                row_index,
                self.class_count,
                row["dropdowns"],
                row["vars"]
            )

    # =========================================

    def save_table(self):

        today = datetime.now()

        attendance_date = today.strftime("%d-%m-%Y")

        month = today.strftime("%B")

        for row in self.student_rows:

            student_number = row["student_no"]
            username = row["username"]

            for class_number in range(
                1,
                self.class_count + 1
            ):

                status = row["vars"][class_number].get()

                if attendance_exists(
                    username,
                    class_number
                ):

                    update_attendance(

                        username=username,

                        class_number=class_number,

                        status=status,

                        attendance_date=attendance_date,

                        month=month

                    )

                else:

                    save_attendance(

                        username=username,

                        student_number=student_number,

                        student_name=username,

                        class_number=class_number,

                        attendance_date=attendance_date,

                        month=month,

                        status=status

                    )

        messagebox.showinfo(
            "Success",
            "Attendance updated successfully."
        )


if __name__ == "__main__":

    app = ctk.CTk()

    app.geometry("1200x700")

    app.title("Teacher Attendance")

    page = TeacherAttendance(app)

    page.pack(
        fill="both",
        expand=True
    )

    app.mainloop()