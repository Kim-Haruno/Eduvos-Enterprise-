import json
import os
import tkinter as tk
from tkinter import ttk, messagebox


class EduvosApp:

    DATA_FILE = os.path.join(os.path.dirname(__file__), "eduvos_data.json")

    def __init__(self, root):

        self.root = root

        self.root.title("Eduvos Enterprise Application")
        self.root.geometry("900x600")
        self.root.minsize(750, 500)

        self.registrations = [
            ("R001", "McNeil", "Python Enterprise Programming", "Approved"),
            ("R002", "Kulani", "Concurrent Python Course", "Approved"),
            ("R003", "KIMBERLY", "Concurrent Python Course", "Approved"),
            ("R004", "Saad", "Concurrent Python Course", "Rejected")
        ]
        self.courses = [
            ("C001", "Python Enterprise Programming", "3", "Active"),
            ("C002", "Java Programming", "3", "Active"),
            ("C003", "Database Systems", "3", "Active")
        ]
        self.support_tickets = []
        self.learners = []
        self.load_data()

        # Make the main window responsive
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.create_sidebar()
        self.create_content()

        self.show_dashboard()

    def load_data(self):
        if not os.path.exists(self.DATA_FILE):
            return

        try:
            with open(self.DATA_FILE, "r", encoding="utf-8") as data_file:
                data = json.load(data_file)

            saved_registrations = data.get("registrations")
            saved_tickets = data.get("support_tickets")
            saved_learners = data.get("learners")

            if isinstance(saved_registrations, list):
                self.registrations = [tuple(item) for item in saved_registrations]
            if isinstance(saved_tickets, list):
                self.support_tickets = saved_tickets
            if isinstance(saved_learners, list):
                self.learners = [tuple(item) for item in saved_learners]
        except (OSError, json.JSONDecodeError, TypeError, ValueError):
            messagebox.showwarning(
                "Storage warning",
                "Saved data could not be loaded. Starting with default data."
            )

    def save_data(self):
        data = {
            "registrations": self.registrations,
            "support_tickets": self.support_tickets,
            "learners": self.learners
        }

        try:
            with open(self.DATA_FILE, "w", encoding="utf-8") as data_file:
                json.dump(data, data_file, indent=2)
        except OSError as error:
            messagebox.showerror(
                "Storage error",
                f"The latest changes could not be saved:\n{error}"
            )

    # ==========================================
    # SIDEBAR
    # ==========================================

    def create_sidebar(self):

        self.sidebar = tk.Frame(
            self.root,
            bg="#222222",
            width=210
        )

        self.sidebar.grid(
            row=0,
            column=0,
            sticky="ns"
        )

        self.sidebar.grid_propagate(False)

        # Application title
        tk.Label(
            self.sidebar,
            text="EDUVOS",
            font=("Arial", 22, "bold"),
            bg="#222222",
            fg="white"
        ).pack(pady=(35, 5))

        tk.Label(
            self.sidebar,
            text="Enterprise Application",
            font=("Arial", 9),
            bg="#222222",
            fg="#bbbbbb"
        ).pack(pady=(0, 30))

        self.nav_button("Dashboard", self.show_dashboard)
        self.nav_button("Learners", self.show_learners)
        self.nav_button("Courses", self.show_courses)
        self.nav_button("Registrations", self.show_registrations)
        self.nav_button("Support Tickets", self.show_support)
        self.nav_button("Reports", self.show_reports)

    def nav_button(self, text, command):

        button = tk.Button(
            self.sidebar,
            text=text,
            command=command,
            font=("Arial", 11),
            bg="#333333",
            fg="white",
            activebackground="#555555",
            activeforeground="white",
            relief="flat",
            anchor="w",
            padx=20,
            pady=12
        )

        button.pack(
            fill="x",
            padx=15,
            pady=4
        )

    # ==========================================
    # CONTENT AREA
    # ==========================================

    def create_content(self):

        self.content = tk.Frame(
            self.root,
            bg="#f5f5f5"
        )

        self.content.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        self.content.columnconfigure(0, weight=1)
        self.content.rowconfigure(1, weight=1)

    def clear_content(self):

        for widget in self.content.winfo_children():
            widget.destroy()

    # ==========================================
    # PAGE HEADER
    # ==========================================

    def page_header(self, title, description=""):

        header = tk.Frame(
            self.content,
            bg="#f5f5f5"
        )

        header.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=35,
            pady=(30, 10)
        )

        tk.Label(
            header,
            text=title,
            font=("Arial", 24, "bold"),
            bg="#f5f5f5"
        ).pack(anchor="w")

        if description:

            tk.Label(
                header,
                text=description,
                font=("Arial", 10),
                bg="#f5f5f5",
                fg="#666666"
            ).pack(
                anchor="w",
                pady=(5, 0)
            )

    # ==========================================
    # DASHBOARD
    # ==========================================

    def show_dashboard(self):

        self.clear_content()

        self.page_header(
            "Dashboard",
            "Overview of the Eduvos Enterprise Application"
        )

        area = tk.Frame(
            self.content,
            bg="#f5f5f5"
        )

        area.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=35,
            pady=20
        )

        # Responsive columns
        for i in range(2):
            area.columnconfigure(i, weight=1)

        learner_count = len({registration[1] for registration in self.registrations})
        self.card(area, "Learners", str(learner_count), 0, 0)
        self.card(area, "Courses", str(len(self.courses)), 0, 1)
        self.card(area, "Registrations", str(len(self.registrations)), 1, 0)
        self.card(area, "Support Tickets", str(len(self.support_tickets)), 1, 1)

    def card(self, parent, title, value, row, column):

        frame = tk.Frame(
            parent,
            bg="white",
            bd=1,
            relief="solid"
        )

        frame.grid(
            row=row,
            column=column,
            sticky="nsew",
            padx=8,
            pady=8,
            ipadx=20,
            ipady=20
        )

        tk.Label(
            frame,
            text=value,
            font=("Arial", 28, "bold"),
            bg="white"
        ).pack(pady=(15, 5))

        tk.Label(
            frame,
            text=title,
            font=("Arial", 11),
            bg="white",
            fg="#666666"
        ).pack(pady=(0, 15))

    # ==========================================
    # LEARNERS
    # ==========================================

    def show_learners(self):

        self.clear_content()

        self.page_header(
            "Learner Registration",
            "Register a new learner in the system"
        )

        form = tk.Frame(
            self.content,
            bg="white",
            bd=1,
            relief="solid"
        )

        form.grid(
            row=1,
            column=0,
            sticky="nw",
            padx=35,
            pady=20,
            ipadx=30,
            ipady=25
        )

        fields = []

        course_names = [course[1] for course in self.courses]

        for row, label in enumerate(
            ["Learner ID", "Full Name", "Email", "Course"]
        ):

            tk.Label(
                form,
                text=label,
                font=("Arial", 10, "bold"),
                bg="white"
            ).grid(
                row=row,
                column=0,
                sticky="w",
                padx=20,
                pady=10
            )

            if label == "Course":
                entry = ttk.Combobox(
                    form,
                    values=course_names,
                    state="readonly",
                    width=38,
                    font=("Arial", 10)
                )
            else:
                entry = tk.Entry(
                    form,
                    width=40,
                    font=("Arial", 10)
                )

            entry.grid(
                row=row,
                column=1,
                padx=20,
                pady=10
            )

            fields.append(entry)

        learner_id, name, email, course = fields

        def register():

            if not learner_id.get():
                messagebox.showerror(
                    "Validation Error",
                    "Learner ID is required."
                )
                return

            if not name.get():
                messagebox.showerror(
                    "Validation Error",
                    "Full name is required."
                )
                return

            if "@" not in email.get():
                messagebox.showerror(
                    "Validation Error",
                    "Please enter a valid email."
                )
                return

            if not course.get():
                messagebox.showerror(
                    "Validation Error",
                    "Course is required."
                )
                return

            registration_numbers = [
                int(registration[0][1:])
                for registration in self.registrations
                if registration[0].startswith("R")
                and registration[0][1:].isdigit()
            ]
            next_registration_number = max(registration_numbers, default=0) + 1
            registration_id = f"R{next_registration_number:03d}"
            self.learners.append(
                (
                    learner_id.get().strip(),
                    name.get().strip(),
                    email.get().strip()
                )
            )
            self.registrations.append(
                (
                    registration_id,
                    name.get().strip(),
                    course.get().strip(),
                    "Approved"
                )
            )
            self.save_data()

            messagebox.showinfo(
                "Success",
                f"{name.get()} registered successfully."
            )
            self.show_registrations()

        tk.Button(
            form,
            text="Register Learner",
            command=register,
            font=("Arial", 10, "bold"),
            padx=20,
            pady=8
        ).grid(
            row=4,
            column=1,
            sticky="e",
            padx=20,
            pady=20
        )

    # ==========================================
    # COURSES
    # ==========================================

    def show_courses(self):

        self.clear_content()

        self.page_header(
            "Course Management",
            "View available courses and their capacity"
        )

        table = tk.Frame(
            self.content,
            bg="white"
        )

        table.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=35,
            pady=20
        )

        columns = (
            "ID",
            "Course",
            "Capacity",
            "Status"
        )

        tree = ttk.Treeview(
            table,
            columns=columns,
            show="headings"
        )

        for column in columns:

            tree.heading(
                column,
                text=column
            )

        tree.column("ID", width=100)
        tree.column("Course", width=350)
        tree.column("Capacity", width=120)
        tree.column("Status", width=120)

        for course in self.courses:
            tree.insert(
                "",
                "end",
                values=course
            )

        tree.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

    # ==========================================
    # REGISTRATIONS
    # ==========================================

    def show_registrations(self):

        self.clear_content()

        self.page_header(
            "Registrations",
            "View learner registration results"
        )

        table = tk.Frame(
            self.content,
            bg="white"
        )

        table.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=35,
            pady=20
        )

        columns = (
            "ID",
            "Learner",
            "Course",
            "Status"
        )

        tree = ttk.Treeview(
            table,
            columns=columns,
            show="headings"
        )

        for column in columns:
            tree.heading(
                column,
                text=column
            )

        tree.column("ID", width=100)
        tree.column("Learner", width=150)
        tree.column("Course", width=350)
        tree.column("Status", width=120)

        for registration in self.registrations:
            tree.insert(
                "",
                "end",
                values=registration
            )

        tree.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

    # ==========================================
    # SUPPORT
    # ==========================================

    def show_support(self):

        self.clear_content()

        self.page_header(
            "Support Tickets",
            "Create a support ticket"
        )

        form = tk.Frame(
            self.content,
            bg="white",
            bd=1,
            relief="solid"
        )

        form.grid(
            row=1,
            column=0,
            sticky="nw",
            padx=35,
            pady=20,
            ipadx=30,
            ipady=25
        )

        tk.Label(
            form,
            text="Learner",
            font=("Arial", 10, "bold"),
            bg="white"
        ).grid(
            row=0,
            column=0,
            padx=20,
            pady=10
        )

        learner = tk.Entry(
            form,
            width=40
        )

        learner.grid(
            row=0,
            column=1,
            padx=20,
            pady=10
        )

        tk.Label(
            form,
            text="Issue",
            font=("Arial", 10, "bold"),
            bg="white"
        ).grid(
            row=1,
            column=0,
            padx=20,
            pady=10,
            sticky="n"
        )

        issue = tk.Text(
            form,
            width=40,
            height=6
        )

        issue.grid(
            row=1,
            column=1,
            padx=20,
            pady=10
        )

        def create_ticket():

            if not learner.get():
                messagebox.showerror(
                    "Error",
                    "Learner is required."
                )
                return

            if not issue.get("1.0", "end").strip():
                messagebox.showerror(
                    "Error",
                    "Please describe the issue."
                )
                return

            self.support_tickets.append(
                {
                    "learner": learner.get().strip(),
                    "issue": issue.get("1.0", "end").strip(),
                    "status": "Open"
                }
            )
            self.save_data()

            messagebox.showinfo(
                "Success",
                "Support ticket created successfully."
            )

        tk.Button(
            form,
            text="Create Ticket",
            command=create_ticket,
            font=("Arial", 10, "bold"),
            padx=20,
            pady=8
        ).grid(
            row=2,
            column=1,
            sticky="e",
            padx=20,
            pady=20
        )

    # ==========================================
    # REPORTS
    # ==========================================

    def show_reports(self):

        self.clear_content()

        self.page_header(
            "Reports",
            "Application and monitoring information"
        )

        report = tk.Frame(
            self.content,
            bg="white",
            bd=1,
            relief="solid"
        )

        report.grid(
            row=1,
            column=0,
            sticky="nw",
            padx=35,
            pady=20,
            ipadx=40,
            ipady=25
        )

        successful = sum(
            registration[3] == "Approved"
            for registration in self.registrations
        )
        rejected = sum(
            registration[3] == "Rejected"
            for registration in self.registrations
        )

        information = [
            ("Registration Requests", str(len(self.registrations))),
            ("Successful Registrations", str(successful)),
            ("Rejected Registrations", str(rejected)),
            ("Support Tickets", str(len(self.support_tickets))),
            ("Bugzot Events", "Recorded"),
            ("Performance Monitoring", "Recorded")
        ]

        for row, (label, value) in enumerate(information):

            tk.Label(
                report,
                text=label,
                font=("Arial", 11),
                bg="white"
            ).grid(
                row=row,
                column=0,
                sticky="w",
                padx=20,
                pady=10
            )

            tk.Label(
                report,
                text=value,
                font=("Arial", 11, "bold"),
                bg="white"
            ).grid(
                row=row,
                column=1,
                sticky="e",
                padx=30,
                pady=10
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = EduvosApp(root)
    root.mainloop()