import os
import tkinter as tk
from tkinter import filedialog
from tkinter.messagebox import showinfo
from tkinter import ttk  # Import ttk for Treeview
import customtkinter as ctk
from fonts import *
from tkcalendar import DateEntry
from datetime import datetime
import sqlite3

conn = sqlite3.connect('pto.db')
cursor = conn.cursor()


class EmployeeAccessFrame:
    def __init__(self, master, emp_id):
        self.master = master
        self.emp_id = emp_id
        self.frame = ctk.CTkFrame(master=self.master, corner_radius=10, width=500, height=300)
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.welcome_label = ctk.CTkLabel(master=self.frame, text=f"Welcome Employee {self.emp_id}", font=font2)
        self.welcome_label.pack(pady=20)
        self.menu_page_label = ctk.CTkLabel(master=self.frame, text="Menu Page", font=font1)
        self.menu_page_label.pack(pady=(10, 20))
        self.document_button = ctk.CTkButton(master=self.frame, text="Document", font=font3)
        self.document_button.pack(pady=10, fill='x', padx=50)
        self.history_button = ctk.CTkButton(master=self.frame, text="History", font=font3,
                                            command=lambda: ViewHistoryFrame(self.master, self.emp_id))
        self.history_button.pack(pady=10, fill='x', padx=50)
        self.plan_button = ctk.CTkButton(master=self.frame, text="Plan", font=font3)
        self.plan_button.pack(pady=10, fill='x', padx=50)
        self.request_button = ctk.CTkButton(master=self.frame, text="Request", font=font3,
                                            command=self.open_request_frame)
        self.request_button.pack(pady=10, fill='x', padx=50)

    def open_request_frame(self):

        # Close the current frame
        self.frame.destroy()
        # Create an instance of PTORequestFrame
        PTORequestFrame(self.master, self.emp_id)


class PTORequestFrame:
    def __init__(self, master, emp_id):
        self.master = master
        self.emp_id = emp_id
        self.frame = ctk.CTkFrame(master=self.master, corner_radius=10, width=600, height=500)
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # PTO Request Form Label
        self.form_label = ctk.CTkLabel(master=self.frame, text="PTO REQUEST FORM", font=font1)
        self.form_label.pack(pady=(20, 10))

        # Employee Information Section
        self.info_frame = ctk.CTkFrame(master=self.frame)
        self.info_frame.pack(pady=(10, 20), fill='x')
        self.first_name_label = ctk.CTkLabel(master=self.info_frame, text="First Name", font=font3)
        self.first_name_label.grid(row=0, column=0, padx=10, pady=5)
        self.first_name_entry = ctk.CTkEntry(master=self.info_frame)
        self.first_name_entry.grid(row=0, column=1, padx=10, pady=5)
        self.last_name_label = ctk.CTkLabel(master=self.info_frame, text="Last Name", font=font3)
        self.last_name_label.grid(row=0, column=2, padx=10, pady=5)
        self.last_name_entry = ctk.CTkEntry(master=self.info_frame)
        self.last_name_entry.grid(row=0, column=3, padx=10, pady=5)

        # Fetch and fill employee details
        self.fetch_and_fill_employee_details()

        self.created_on_label = ctk.CTkLabel(master=self.info_frame, text="Created On", font=font3)
        self.created_on_label.grid(row=0, column=4, padx=10, pady=5)
        self.created_on_entry = ctk.CTkEntry(master=self.info_frame)
        self.created_on_entry.grid(row=0, column=5, padx=10, pady=5)
        # Automatically fill the 'Created On' entry with today's date
        today = datetime.now().strftime("%m/%d/%y")
        self.created_on_entry.insert(0, today)
        self.created_on_entry.configure(state='disabled')

        # Request Details Section
        self.details_frame = ctk.CTkFrame(master=self.frame)
        self.details_frame.pack(pady=(0, 20), fill='x')
        self.reason_label = ctk.CTkLabel(master=self.details_frame, text="Reason for Request", font=font3)
        self.reason_label.grid(row=0, column=0, padx=10, pady=5)
        self.reason_entry = ctk.CTkEntry(master=self.details_frame)
        self.reason_entry.grid(row=0, column=1, padx=10, pady=5, columnspan=3)

        # Radio buttons for Request Type
        self.type_label = ctk.CTkLabel(master=self.details_frame, text="Select Type", font=font3)
        self.type_label.grid(row=1, column=0, padx=10, pady=5)
        self.type_var = tk.StringVar(value="Paid")
        self.unpaid_rb = ctk.CTkRadioButton(master=self.details_frame, text="UnPaid", variable=self.type_var,
                                            value="UnPaid", font=font3)
        self.unpaid_rb.grid(row=1, column=1, padx=10, pady=5)
        self.paid_rb = ctk.CTkRadioButton(master=self.details_frame, text="Paid", variable=self.type_var, value="Paid",
                                          font=font3)
        self.paid_rb.grid(row=1, column=2, padx=10, pady=5)

        # Request Dates Section
        self.dates_frame = ctk.CTkFrame(master=self.frame)
        self.dates_frame.pack(pady=(0, 20), fill='x')
        self.start_date_label = ctk.CTkLabel(master=self.dates_frame, text="Start date:", font=font3)
        self.start_date_label.grid(row=0, column=0, padx=10, pady=5)
        self.start_date_entry = DateEntry(master=self.dates_frame, width=20, font=font3)
        self.start_date_entry.grid(row=0, column=1, padx=10, pady=5)
        self.end_date_label = ctk.CTkLabel(master=self.dates_frame, text="End date:", font=font3)
        self.end_date_label.grid(row=0, column=2, padx=10, pady=5)
        self.end_date_entry = DateEntry(master=self.dates_frame, width=20, font=font3)
        self.end_date_entry.grid(row=0, column=3, padx=10, pady=5)

        # Submit Button
        self.submit_button = ctk.CTkButton(master=self.frame, text="SUBMIT", font=font2, command=self.submit_request)
        self.submit_button.pack(pady=(20, 10), fill='x', padx=150)

    def fetch_and_fill_employee_details(self):
        # Now, you would use 'self.emp_id' to get the user's UserID from the 'employee' table.
        cursor.execute('SELECT UserID FROM employee WHERE EmpID = ?', (self.emp_id,))
        user_id = cursor.fetchone()[0]

        # Next, use 'user_id' to fetch the first name and last name from the 'user' table.
        cursor.execute('SELECT FName, LName FROM user WHERE UserID = ?', (user_id,))
        first_name, last_name = cursor.fetchone()

        # Now insert the first and last names into the entry fields
        self.first_name_entry.insert(0, first_name)
        self.last_name_entry.insert(0, last_name)

        # Disable the entry fields to prevent editing
        self.first_name_entry.configure(state='disabled')
        self.last_name_entry.configure(state='disabled')

    def submit_request(self):

        # Check if any required field is empty
        if not all([self.reason_entry.get(), self.start_date_entry.get(), self.end_date_entry.get()]):
            showinfo("Incomplete Form", "Please fill out all required fields.")
            return

        # Determine PTO type
        pto_type = 1 if self.type_var.get() == "UnPaid" else 2

        # Collect all PTO request data here
        pto_data = {
            "EmpID": self.emp_id,
            "first_name": self.first_name_entry.get(),
            "last_name": self.last_name_entry.get(),
            "PTODate": self.created_on_entry.get(),
            "PTOType": pto_type,
            "PTOReason": self.reason_entry.get(),
            "PTOStartDate": self.start_date_entry.get(),
            "PTOEndDate": self.end_date_entry.get(),
        }

        # Close the current frame
        self.frame.destroy()

        # Transition to the PTODocumentFrame, passing the collected data
        PTODocumentFrame(self.master, pto_data)


class PTODocumentFrame:
    def __init__(self, master, pto_data):
        self.master = master
        self.pto_data = pto_data
        self.frame = ctk.CTkFrame(master=self.master, corner_radius=10, width=600, height=300)
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.title_label = ctk.CTkLabel(master=self.frame, text="PTO DOCUMENTATION", font=font1)
        self.title_label.pack(pady=20)

        self.browse_button = ctk.CTkButton(master=self.frame, text="Browse", command=self.browse_file)
        self.browse_button.pack(side=tk.TOP, pady=20)

        self.file_label = ctk.CTkLabel(master=self.frame, text="No file selected")
        self.file_label.pack(side=tk.TOP, pady=10)

        self.submit_button = ctk.CTkButton(master=self.frame, text="Submit Request", command=self.save_request,
                                           state="disabled")
        self.submit_button.pack(side=tk.TOP, pady=20)

    def browse_file(self):
        filename = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if filename:
            self.file_label.configure(text=os.path.basename(filename))
            self.pto_data["pdf_filename"] = filename  # Add the filename to the PTO data dictionary
            self.submit_button.configure(state="normal")  # Enable the Submit button
            showinfo("File Selected", f"You have selected {filename}")

    def save_request(self):
        # Insert data into PTORequest table
        cursor.execute('''INSERT INTO PTORequest (EmpID, PTODate, PTOType, PTOReason, PTOStartDate, PTOEndDate)
                          VALUES (?, ?, ?, ?, ?, ?)''', (self.pto_data["EmpID"], self.pto_data["PTODate"],
                                                         self.pto_data["PTOType"], self.pto_data["PTOReason"],
                                                         self.pto_data["PTOStartDate"], self.pto_data["PTOEndDate"]))
        conn.commit()

        # Retrieve the newly inserted PTOID
        cursor.execute('''SELECT last_insert_rowid()''')
        pto_id = cursor.fetchone()[0]

        # Read the binary data of the PDF file
        with open(self.pto_data["pdf_filename"], 'rb') as file:
            pdf_blob = file.read()

        # Insert data into PTODocument table
        cursor.execute('''INSERT INTO PTODocument (PTOID, PDFData) VALUES (?, ?)''', (pto_id, pdf_blob))
        conn.commit()

        showinfo("Request Submitted", "PTO request submitted successfully!")

        self.frame.destroy()  # Close the document frame

        # Open the employee frame again
        EmployeeAccessFrame(self.master, self.pto_data["EmpID"])


class ViewHistoryFrame:
    def __init__(self, master, emp_id):
        self.master = master
        self.emp_id = emp_id
        self.frame = ctk.CTkFrame(master=self.master, corner_radius=10)
        self.frame.pack(fill='both', expand=True, padx=10, pady=10)

        self.title_label = ctk.CTkLabel(master=self.frame, text="VIEW PTO HISTORY", font= font1)  # Adjust the font to match your application
        self.title_label.pack(pady=10)

        # Define the column headers before creating the Treeview
        self.headers = ["PTO ID", "Employee ID", "Submitted On", "Type", "Reason", "Start Date", "End Date"]

        # Create Treeview widget
        self.tree = ttk.Treeview(self.frame, columns=self.headers, show='headings')
        self.style_treeview()  # Call a method to style the Treeview

        # Configure the columns and headings
        for col in self.headers:
            self.tree.heading(col, text=col, anchor='center')
            self.tree.column(col, anchor='center', width=120)  # Adjust the column width as needed

        self.tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Insert data into the treeview
        self.populate_history()

        self.return_button = ctk.CTkButton(master=self.frame, text="Return", command=self.return_to_main, corner_radius=8)  # Make sure the corner radius matches other buttons
        self.return_button.pack(pady=10)
        self.return_button.place(relx=1, rely=0, anchor='ne', x=-10, y=10)

    def style_treeview(self):
        # You can adjust the colors and styles to match your customtkinter styles
        style = ttk.Style(self.frame)
        style.theme_use("clam")  # This is a theme that allows for more customization

        # Adjust the following colors and styles to match your app's theme
        style.configure("Treeview",
                        background="#ECECEC",
                        foreground="black",
                        rowheight=25,
                        fieldbackground="#ECECEC",
                        font= font3)

        style.map('Treeview',
                  background=[('selected', '#347083')])  # Use your app's selection color

        style.configure("Treeview.Heading",
                        background="#D3D3D3",
                        foreground="black",
                        relief="flat",
                        font= font2)

        style.map("Treeview.Heading",
                  relief=[('active', 'groove'), ('pressed', 'sunken')])

    def populate_history(self):
        # Assume 'cursor' is a database cursor connected to your database
        cursor.execute(
            'SELECT PTOID, EmpID, PTODate, PTOType, PTOReason, PTOStartDate, PTOEndDate FROM PTORequest WHERE EmpID = ?',
            (self.emp_id,))
        records = cursor.fetchall()

        for record in records:
            pto_type = "Unpaid" if record[3] == 1 else "Paid"
            self.tree.insert("", 'end',
                             values=(record[0], record[1], record[2], pto_type, record[4], record[5], record[6]))

    def return_to_main(self):
        self.frame.destroy()
        EmployeeAccessFrame(self.master, self.emp_id)
