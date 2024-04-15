import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import sqlite3
from selection import SelectionFrame
from employee import EmployeeAccessFrame
from fonts import *

conn = sqlite3.connect('pto.db')
cursor = conn.cursor()

# Create the employee table with EmpID as primary key
cursor.execute('''
    CREATE TABLE IF NOT EXISTS employee(
    EmpID INT PRIMARY KEY,
    UserID INT NOT NULL,
    EmpPos VARCHAR(255) NOT NULL,
    EmpSalary DECIMAL(10, 2) NOT NULL,
    Password VARCHAR(255) NOT NULL,
    EmpDep VARCHAR(255),
    FOREIGN KEY (UserID) REFERENCES user(UserID))''')

# Check if there's any data in the table
cursor.execute('SELECT COUNT(*) FROM employee')
if cursor.fetchone()[0] == 0:  # If the table is empty, then insert data
    employees_data = [
        (10000, 1,'Employee', 10000, 'Passw0rd', 'Finance'),
        (11111, 2, 'Manager', 20000.33, 'Passw0rd1', 'Finance'),
        (12345, 3, 'HR', 50000, 'Passw0rd2', 'HR'),
        (22222, 4, 'HR', 1245.36, 'Passw0rd3', None),
        (54321, 5, 'Employee', 10000.55, 'Passw0rd4', None)
    ]
    cursor.executemany('''
        INSERT INTO employee (EmpID, UserID, EmpPos, EmpSalary, Password, EmpDep)
        SELECT ?, ?, ?, ?, ?, ?
        WHERE NOT EXISTS (SELECT 1 FROM employee WHERE EmpID = ?)
    ''', [(emp_data + (emp_data[0],)) for emp_data in employees_data])
    conn.commit()

class LoginFrame:
    def __init__(self, master):
        self.master = master
        self.frame = ctk.CTkFrame(master=self.master, corner_radius=10, width=500, height=300)
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.font3 = ('Arial', 13, 'bold')
        self.username_label = ctk.CTkLabel(master=self.frame, text="Username", font=font3)
        self.username_label.pack(pady=(30, 10))
        self.username_entry = ctk.CTkEntry(master=self.frame, placeholder_text="Username", width=300)
        self.username_entry.pack(pady=10)
        self.password_label = ctk.CTkLabel(master=self.frame, text="Password", font=font3)
        self.password_label.pack(pady=10)
        self.password_entry = ctk.CTkEntry(master=self.frame, placeholder_text="Password", show="*", width=300)
        self.password_entry.pack(pady=10)
        self.login_button = ctk.CTkButton(master=self.frame, text="Login", font=font2, fg_color="#4e8d7c",
                                          hover_color="#34675c",
                                          command=self.login_account)
        self.login_button.pack(pady=20)

    def login_account(self):
        emp_id = self.username_entry.get()
        password = self.password_entry.get()
        if emp_id != '' and password != '':
            cursor.execute('SELECT EmpPos, Password FROM employee WHERE EmpID=?', [emp_id])
            result = cursor.fetchone()
            if result:
                emp_pos = result[0]
                emp_password = result[1]
                if emp_password == password:
                    self.frame.destroy()
                    if emp_pos in ['Manager', 'HR']:
                        SelectionFrame(self.master, emp_pos, emp_id)
                    elif emp_pos == 'Employee':
                        EmployeeAccessFrame(self.master, emp_id)
                    else:
                        messagebox.showerror("Error", "Invalid role")
                else:
                    messagebox.showerror("Error", "Password is wrong")
            else:
                messagebox.showerror("Error", "Employee doesn't exist")
        else:
            messagebox.showerror("Error", "Please enter both username and password")
