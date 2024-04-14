import customtkinter as ctk
import sqlite3
import tkinter as tk
from tkinter import messagebox

app = ctk.CTk()
app.title('PTO Login')
app.geometry("800x500")
app.configure(bg="#121212")

font1 = ('Helvetica', 25, 'bold')
font2 = ('Arial', 17, 'bold')
font3 = ('Arial', 13, 'bold')
font4 = ('Arial', 13, 'bold', 'underline')

conn = sqlite3.connect('pto.db')
cursor = conn.cursor()

# Create the employee table with EmpID as primary key
cursor.execute('''
    CREATE TABLE IF NOT EXISTS employee(
    EmpID INT PRIMARY KEY,
    EmpPos VARCHAR(255) NOT NULL,
    EmpSalary DECIMAL(10, 2) NOT NULL,
    Password VARCHAR(255) NOT NULL,
    EmpDep VARCHAR(255))''')

# Check if there's any data in the table
cursor.execute('SELECT COUNT(*) FROM employee')
if cursor.fetchone()[0] == 0:  # If the table is empty, then insert data
    employees_data = [
        (10000, 'Employee', 10000, 'Passw0rd', 'Finance'),
        (11111, 'Manager', 20000.33, 'Passw0rd1', 'Finance'),
        (12345, 'HR', 50000, 'Passw0rd2', 'HR'),
        (22222, 'HR', 1245.36, 'Passw0rd3', None),
        (54321, 'Employee', 10000.55, 'Passw0rd4', None)
    ]
    cursor.executemany('''
        INSERT INTO employee (EmpID, EmpPos, EmpSalary, Password, EmpDep)
        SELECT ?, ?, ?, ?, ?
        WHERE NOT EXISTS (SELECT 1 FROM employee WHERE EmpID = ?)
    ''', [(emp_data + (emp_data[0],)) for emp_data in employees_data])
    conn.commit()

# Global variables
selection_frame = None
login_frame = None


def employee_access_frame(emp_id):

    employee_frame = ctk.CTkFrame(master=app, corner_radius=10, width=500, height=300)
    employee_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    welcome_label = ctk.CTkLabel(master=employee_frame, text=f"Welcome Employee {emp_id}", font=font2)
    welcome_label.pack(pady=20)
    document_button = ctk.CTkButton(employee_frame, text="Document", font=font3)
    document_button.pack(pady=10)


def manager_access_frame(emp_id):
    global selection_frame
    if selection_frame:
        selection_frame.destroy()
        selection_frame = None

    access_frame = ctk.CTkFrame(master=app, corner_radius=10, width=500, height=300)
    access_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)


def hr_access_frame(emp_id):
    global selection_frame
    if selection_frame:
        selection_frame.destroy()
        selection_frame = None
    access_frame = ctk.CTkFrame(master=app, corner_radius=10, width=500, height=300)
    access_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)


def login_account():
    global login_frame
    emp_id = username_entry.get()
    password = password_entry.get()
    if emp_id != '' and password != '':
        cursor.execute('SELECT EmpPos, Password FROM employee WHERE EmpID=?', [emp_id])
        result = cursor.fetchone()
        if result:
            emp_pos = result[0]
            emp_password = result[1]
            if emp_password == password:
                if login_frame:
                    login_frame.destroy()
                    login_frame = None
                if emp_pos in ['Manager', 'HR']:
                    selection_frame(emp_pos, emp_id)
                elif emp_pos == 'Employee':
                    employee_access_frame(emp_id)
                else:
                    messagebox.showerror("Error", "Invalid role")
            else:
                messagebox.showerror("Error", "Password is wrong")
        else:
            messagebox.showerror("Error", "Employee doesn't exist")
    else:
        messagebox.showerror("Error", "Please enter both username and password")


def selection_frame(emp_pos, emp_id):
    global selection_frame
    global login_frame
    if login_frame:
        login_frame.destroy()
        login_frame = None
    selection_frame = ctk.CTkFrame(master=app, corner_radius=10, width=500, height=300)
    selection_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    role_label = ctk.CTkLabel(master=selection_frame, text=f"Select role for {emp_pos}", font=font3)
    role_label.pack(pady=(30, 10))
    selected_role = tk.StringVar()
    selected_role.set(emp_pos)
    roles = [("HR", "HR"), ("Employee", "Employee")] if emp_pos == "HR" else [("Manager", "Manager"),
                                                                              ("Employee", "Employee")]
    for role_text, role_value in roles:
        role_radio_button = ctk.CTkRadioButton(master=selection_frame, text=role_text, variable=selected_role,
                                               value=role_value, font=font3)
        role_radio_button.pack()
    continue_button = ctk.CTkButton(master=selection_frame, text="Continue", font=font2, fg_color="#4e8d7c",
                                    hover_color="#34675c",
                                    command=lambda: on_continue(emp_id, selected_role.get()))
    continue_button.pack(pady=20)


def on_continue(emp_id, selected_role):
    global selection_frame  # Ensure we are accessing the global variable
    if selection_frame:
        selection_frame.destroy()
        selection_frame = None  # Clear the reference, as it's no longer valid

    # Now call the frame for the selected role
    if selected_role == 'Manager':
        manager_access_frame(emp_id)
    elif selected_role == 'HR':
        hr_access_frame(emp_id)
    elif selected_role == 'Employee':
        employee_access_frame(emp_id)
    else:
        messagebox.showerror("Error", "Please choose a role")


# Login frame setup
login_frame = ctk.CTkFrame(master=app, corner_radius=10, width=500, height=300)
login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
username_label = ctk.CTkLabel(master=login_frame, text="Username", font=font3)
username_label.pack(pady=(30, 10))
username_entry = ctk.CTkEntry(master=login_frame, placeholder_text="Username", width=300)
username_entry.pack(pady=10)
password_label = ctk.CTkLabel(master=login_frame, text="Password", font=font3)
password_label.pack(pady=10)
password_entry = ctk.CTkEntry(master=login_frame, placeholder_text="Password", show="*", width=300)
password_entry.pack(pady=10)
login_button = ctk.CTkButton(master=login_frame, text="Login", font=font2, fg_color="#4e8d7c", hover_color="#34675c",
                             command=login_account)
login_button.pack(pady=20)

app.mainloop()
