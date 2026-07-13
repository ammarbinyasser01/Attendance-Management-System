import customtkinter as ctk
from tkinter import ttk

from collections import defaultdict

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from database.database import get_student_attendance


# ==========================================
# COLOR / FONT PALETTE (matches dashboards)
# ==========================================

CARD_COLOR_LIGHT = "#2c3150"
ACCENT_COLOR = "#5b8def"
PRESENT_COLOR = "#4cc98a"
ABSENT_COLOR = "#e5566d"
TEXT_COLOR = "#f2f3f7"
SUBTEXT_COLOR = "#a3a8c2"

FONT_FAMILY = "Segoe UI"


class StudentAttendance(ctk.CTkFrame):

    def __init__(self, parent, username):

        super().__init__(parent)

        self.username = username

        self.records = []

        self.canvas = None

        self.build_gui()

    # ===========================================

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

    # ===========================================

    def build_status(self):

        title = ctk.CTkLabel(
            self.status_tab,
            text="My Attendance",
            font=(FONT_FAMILY, 22, "bold"),
            text_color=TEXT_COLOR
        )

        title.pack(
            pady=(15, 10)
        )

        table_wrap = ctk.CTkFrame(self.status_tab, fg_color="transparent")

        table_wrap.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )

        columns = (
            "no",
            "class",
            "month",
            "status"
        )

        self.table = ttk.Treeview(
            table_wrap,
            columns=columns,
            show="headings",
            height=15
        )

        self.table.heading(
            "no",
            text="No"
        )

        self.table.heading(
            "class",
            text="Class No"
        )

        self.table.heading(
            "month",
            text="Month"
        )

        self.table.heading(
            "status",
            text="Status"
        )

        self.table.column(
            "no",
            width=80,
            anchor="center"
        )

        self.table.column(
            "class",
            width=150,
            anchor="center"
        )

        self.table.column(
            "month",
            width=180,
            anchor="center"
        )

        self.table.column(
            "status",
            width=180,
            anchor="center"
        )

        scrollbar = ttk.Scrollbar(
            table_wrap,
            orient="vertical",
            command=self.table.yview
        )
        self.table.configure(yscrollcommand=scrollbar.set)

        self.table.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(side="right", fill="y")

        self.table.tag_configure("present", foreground=PRESENT_COLOR)
        self.table.tag_configure("absent", foreground=ABSENT_COLOR)

        self.load_attendance()

    # ===========================================

    def build_graph(self):

        header = ctk.CTkLabel(
            self.graph_tab,
            text="Attendance Overview",
            font=(FONT_FAMILY, 20, "bold"),
            text_color=TEXT_COLOR
        )

        header.pack(pady=(15, 5))

        self.summary_label = ctk.CTkLabel(
            self.graph_tab,
            text="",
            font=(FONT_FAMILY, 14),
            text_color=SUBTEXT_COLOR
        )

        self.summary_label.pack(pady=(0, 10))

        self.graph_container = ctk.CTkFrame(
            self.graph_tab,
            fg_color=CARD_COLOR_LIGHT,
            corner_radius=12
        )

        self.graph_container.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )

        self.refresh_graph()

    # ===========================================

    def load_attendance(self):

        for row in self.table.get_children():

            self.table.delete(row)

        self.records = get_student_attendance(
            self.username
        )

        count = 1

        for record in self.records:

            class_number = record[0]

            month = record[1]

            status = record[2]

            tag = "present" if status == "Present" else "absent"

            self.table.insert(
                "",
                "end",
                values=(
                    count,
                    class_number,
                    month,
                    status
                ),
                tags=(tag,)
            )

            count += 1

        self.refresh_graph()

    # ===========================================

    def refresh_graph(self):

        # graph tab isn't built yet on the very first call from build_status
        if not hasattr(self, "graph_container"):
            return

        for widget in self.graph_container.winfo_children():
            widget.destroy()

        if self.canvas is not None:
            self.canvas = None

        if not self.records:

            empty_label = ctk.CTkLabel(
                self.graph_container,
                text="No attendance records yet.",
                font=(FONT_FAMILY, 14),
                text_color=SUBTEXT_COLOR
            )

            empty_label.pack(expand=True)

            self.summary_label.configure(text="")

            return

        counts = defaultdict(lambda: {"Present": 0, "Absent": 0})

        for record in self.records:

            class_number = record[0]
            status = record[2]

            if status not in ("Present", "Absent"):
                continue

            counts[class_number][status] += 1

        class_numbers = sorted(counts.keys())

        present_values = [counts[c]["Present"] for c in class_numbers]
        absent_values = [counts[c]["Absent"] for c in class_numbers]

        total = len(self.records)
        present_total = sum(1 for r in self.records if r[2] == "Present")
        percentage = round((present_total / total) * 100, 1) if total else 0

        self.summary_label.configure(
            text=(
                f"Overall Attendance: {present_total}/{total} "
                f"classes present ({percentage}%)"
            )
        )

        figure = Figure(figsize=(6.5, 4), dpi=100)
        figure.patch.set_facecolor(CARD_COLOR_LIGHT)

        ax = figure.add_subplot(111)
        ax.set_facecolor(CARD_COLOR_LIGHT)

        positions = range(len(class_numbers))
        width = 0.35

        ax.bar(
            [p - width / 2 for p in positions],
            present_values,
            width,
            label="Present",
            color=PRESENT_COLOR
        )

        ax.bar(
            [p + width / 2 for p in positions],
            absent_values,
            width,
            label="Absent",
            color=ABSENT_COLOR
        )

        ax.set_xticks(list(positions))
        ax.set_xticklabels(
            [f"Class {c}" for c in class_numbers],
            color=TEXT_COLOR
        )
        ax.tick_params(colors=TEXT_COLOR)

        ax.set_ylabel("Sessions", color=TEXT_COLOR)
        ax.set_title("Attendance by Class", color=TEXT_COLOR)

        for spine in ax.spines.values():
            spine.set_color(SUBTEXT_COLOR)

        legend = ax.legend(
            facecolor=CARD_COLOR_LIGHT,
            edgecolor=SUBTEXT_COLOR
        )

        for text in legend.get_texts():
            text.set_color(TEXT_COLOR)

        figure.tight_layout()

        self.canvas = FigureCanvasTkAgg(figure, master=self.graph_container)
        self.canvas.draw()

        self.canvas.get_tk_widget().pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )


if __name__ == "__main__":

    app = ctk.CTk()

    app.geometry("900x600")

    attendance = StudentAttendance(
        app,
        "ammar"
    )

    attendance.pack(
        fill="both",
        expand=True
    )

    app.mainloop()