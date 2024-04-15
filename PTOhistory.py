import tempfile
import webbrowser
from tkinter.messagebox import showinfo
from tkinter import ttk  # Import ttk for Treeview
import customtkinter as ctk
from fonts import *
from manager import *


import sqlite3

conn = sqlite3.connect('pto.db')
cursor = conn.cursor()

class ViewHistoryFrame:
    def __init__(self, master, emp_id, return_frame):
        self.master = master
        self.emp_id = emp_id
        self.return_frame = return_frame
        self.frame = ctk.CTkFrame(master=self.master, corner_radius=10)
        self.frame.pack(fill='both', expand=True, padx=10, pady=10)

        self.title_label = ctk.CTkLabel(master=self.frame, text="VIEW PTO HISTORY", font=font1)
        self.title_label.pack(pady=10)

        self.headers = ["PTO ID", "Employee ID", "Submitted On", "Type", "Reason", "Start Date", "End Date"]
        self.tree = ttk.Treeview(self.frame, columns=self.headers, show='headings')
        self.style_treeview()
        for col in self.headers:
            self.tree.heading(col, text=col, anchor='center')
            self.tree.column(col, anchor='center', width=120)
        self.tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        self.tree.bind("<Double-1>", self.on_double_click)  # Bind double-click event to treeview

        self.return_button = ctk.CTkButton(master=self.frame, text="Return", command=self.return_to_main,
                                           corner_radius=8, font=font2)
        self.return_button.pack(pady=10)
        self.return_button.place(relx=1, rely=0, anchor='ne', x=-10, y=10)

        # ComboBox for Department filter
        self.dept_label = ctk.CTkLabel(master=self.frame, text="Filter by Department:", font=font2)
        self.dept_label.pack(pady=10)

        self.style = ttk.Style(self.frame)
        self.style.theme_use("clam")  # Use a theme that blends well, 'clam' is a popular choice

        larger_font = ('Arial', 25)
        # Configuring the Combobox style to look like customtkinter Entry
        self.style.configure("TCombobox",
                             fieldbackground="#ECECEC",
                             background="white",
                             foreground="black",
                             bordercolor="#ECECEC",
                             lightcolor="#ECECEC",
                             darkcolor="#ECECEC",
                             borderwidth=1,
                             arrowsize=25,
                             relief="flat",
                             font=larger_font)

        self.style.map("TCombobox",
                       fieldbackground=[("active", "white"), ("!disabled", "#ECECEC")],
                       background=[("active", "white"), ("!disabled", "white")],
                       bordercolor=[("active", "#979da2"), ("!disabled", "#ECECEC")],
                       lightcolor=[("active", "#ECECEC"), ("!disabled", "#ECECEC")],
                       darkcolor=[("active", "#ECECEC"), ("!disabled", "#ECECEC")])

        # Set the padding to increase the height of the combobox
        self.style.configure("TCombobox", padding=10)

        # Create a frame to act as a border with rounded corners
        rounded_border_frame = ctk.CTkFrame(self.frame, corner_radius=10)
        rounded_border_frame.pack(pady=10, padx=10)

        # Create and place the Combobox
        self.dept_combobox = ttk.Combobox(rounded_border_frame, style="TCombobox", height=5)
        self.dept_combobox.pack(pady=10, padx=10)

        # Entry for Employee ID filter
        self.emp_id_label = ctk.CTkLabel(master=self.frame, text="Filter by Employee ID:", font=font2)
        self.emp_id_label.pack(pady=10)

        self.emp_id_entry = ctk.CTkEntry(self.frame)
        self.emp_id_entry.pack(pady=10, padx=10)

        # Add a filter button
        self.filter_button = ctk.CTkButton(master=self.frame, text="Apply Filter", command=self.apply_filters, font=font2)
        self.filter_button.pack(pady=10)

        self.populate_departments()
        self.populate_history()

    def populate_departments(self):
        # Query all departments
        cursor.execute('SELECT DISTINCT EmpDep FROM employee')
        departments = cursor.fetchall()
        self.dept_combobox['values'] = [dept[0] for dept in departments]

    def apply_filters(self):
        self.populate_history()

    def style_treeview(self):

        style = ttk.Style(self.frame)
        style.theme_use("clam")

        style.configure("Treeview",
                        background="#ECECEC",
                        foreground="black",
                        rowheight=25,
                        fieldbackground="#ECECEC",
                        font=font3)

        style.map('Treeview',
                  background=[('selected', '#36719f')])

        style.configure("Treeview.Heading",
                        background="#D3D3D3",
                        foreground="black",
                        relief="flat",
                        font=font2)

        style.map("Treeview.Heading",
                  relief=[('active', 'groove'), ('pressed', 'sunken')])

    def populate_history(self):
        emp_id_filter = self.emp_id_entry.get().strip()
        dept_filter = self.dept_combobox.get().strip()

        query = 'SELECT PTOID, EmpID, PTODate, PTOType, PTOReason, PTOStartDate, PTOEndDate FROM PTORequest WHERE EmpID LIKE ? AND EmpID IN (SELECT EmpID FROM employee WHERE EmpDep LIKE ?)'
        params = (f'%{emp_id_filter}%', f'%{dept_filter}%')

        cursor.execute(query, params)
        records = cursor.fetchall()

        self.tree.delete(*self.tree.get_children())  # Clear existing entries in the treeview
        for record in records:
            pto_type = "Unpaid" if record[3] == 1 else "Paid"
            self.tree.insert("", 'end',
                             values=(record[0], record[1], record[2], pto_type, record[4], record[5], record[6]))

    def return_to_main(self):
        self.frame.destroy()
        if self.return_frame == 'HR':
            from hr import HRAccessFrame
            HRAccessFrame(self.master, self.emp_id)
        elif self.return_frame == 'Manager':
            from manager import ManagerAccessFrame
            ManagerAccessFrame(self.master, self.emp_id)

    def on_double_click(self, event):
        item = self.tree.selection()[0]  # Get selected item
        pto_id = self.tree.item(item, "values")[0]  # Extract PTO ID from selected item
        pdf_data = self.fetch_pdf_data(pto_id)  # Fetch PDF data from database

        if pdf_data:
            self.show_pdf_frame(pdf_data)
        else:
            showinfo("No PDF Attached", f"No PDF is attached to PTO ID {pto_id}.")  # Show popup if no PDF is attached

    def fetch_pdf_data(self, pto_id):
        cursor.execute('SELECT PDFData FROM PTODocument WHERE PTOID = ?', (pto_id,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return None

    def show_pdf_frame(self, pdf_data):
        # Write the PDF data to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_pdf:
            temp_pdf.write(pdf_data)
            temp_pdf_path = temp_pdf.name

        # Open the PDF with the default system PDF viewer through the web browser
        webbrowser.open(f'file://{temp_pdf_path}', new=2)