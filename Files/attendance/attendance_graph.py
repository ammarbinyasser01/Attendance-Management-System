import customtkinter as ctk
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from database.database import (
    get_all_students,
    get_student_attendance
)


class AttendanceGraph(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(parent)

        self.build_gui()

    # =====================================

    def build_gui(self):

        left = ctk.CTkFrame(
            self,
            width=220
        )

        left.pack(
            side="left",
            fill="y",
            padx=10,
            pady=10
        )

        right = ctk.CTkFrame(self)

        right.pack(
            side="right",
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        ctk.CTkLabel(
            left,
            text="Students",
            font=("Arial",22,"bold")
        ).pack(pady=15)

        self.student_list = tk.Listbox(
            left,
            width=22,
            height=25
        )

        self.student_list.pack(
            padx=10,
            pady=10,
            fill="y"
        )

        for student in get_all_students():

            self.student_list.insert(
                "end",
                student[0]
            )

        self.student_list.bind(
            "<<ListboxSelect>>",
            self.load_graph
        )

        self.graph_frame = ctk.CTkFrame(right)

        self.graph_frame.pack(
            fill="both",
            expand=True
        )

    # =====================================

    def load_graph(self, event):

        selection = self.student_list.curselection()

        if not selection:
            return

        username = self.student_list.get(
            selection[0]
        )

        records = get_student_attendance(
            username
        )

        for widget in self.graph_frame.winfo_children():

            widget.destroy()

        figure = Figure(
            figsize=(7, 5),
            dpi=100
        )

        axis = figure.add_subplot(111)

        if len(records) == 0:

            axis.text(
                0.5,
                0.5,
                "No Attendance Found",
                ha="center",
                va="center",
                fontsize=16
            )

            axis.set_xticks([])
            axis.set_yticks([])

        else:

            x = []

            y = []

            present = 0

            for record in records:

                class_number = record[0]

                month = record[1]

                status = record[2]

                x.append(
                    f"C{class_number}"
                )

                if status == "Present":

                    present += 1

                y.append(present)

            axis.plot(
                x,
                y,
                marker="o",
                linewidth=2
            )

            axis.set_title(
                f"{username} Attendance"
            )

            axis.set_xlabel(
                "Classes"
            )

            axis.set_ylabel(
                "Present Count"
            )

            axis.grid(True)

        canvas = FigureCanvasTkAgg(
            figure,
            self.graph_frame
        )

        canvas.draw()

        canvas.get_tk_widget().pack(
            fill="both",
            expand=True
        )


if __name__ == "__main__":

    app = ctk.CTk()

    app.geometry("1200x700")

    graph = AttendanceGraph(app)

    graph.pack(
        fill="both",
        expand=True
    )

    app.mainloop()