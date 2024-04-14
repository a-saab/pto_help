import tkinter as tk
import customtkinter as ctk
from fonts import *
from tkcalendar import DateEntry
from datetime import datetime


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
        self.history_button = ctk.CTkButton(master=self.frame, text="History", font=font3)
        self.history_button.pack(pady=10, fill='x', padx=50)
        self.plan_button = ctk.CTkButton(master=self.frame, text="Plan", font=font3)
        self.plan_button.pack(pady=10, fill='x', padx=50)
        self.request_button = ctk.CTkButton(master=self.frame, text="Request", font=font3,
                                            command=self.open_request_frame)
        self.request_button.pack(pady=10, fill='x', padx=50)

    def open_request_frame(self):
        # Create an instance of PTORequestFrame
        pto_request_frame = PTORequestFrame(self.master, self.emp_id)


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
        self.created_on_label = ctk.CTkLabel(master=self.info_frame, text="Created On", font=font3)
        self.created_on_label.grid(row=0, column=4, padx=10, pady=5)
        self.created_on_entry = ctk.CTkEntry(master=self.info_frame)
        self.created_on_entry.grid(row=0, column=5, padx=10, pady=5)
        # Automatically fill the 'Created On' entry with today's date
        today = datetime.now().strftime("%Y-%m-%d")
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
        self.submit_button = ctk.CTkButton(master=self.frame, text="SUBMIT", font=font2)
        self.submit_button.pack(pady=(20, 10), fill='x', padx=150)
