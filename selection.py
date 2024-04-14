import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from employee import EmployeeAccessFrame
from manager import ManagerAccessFrame
from hr import HRAccessFrame
from fonts import *

class SelectionFrame:
    def __init__(self, master, emp_pos, emp_id):
        self.master = master
        self.emp_pos = emp_pos
        self.emp_id = emp_id
        self.frame = ctk.CTkFrame(master=self.master, corner_radius=10, width=500, height=300)
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.role_label = ctk.CTkLabel(master=self.frame, text=f"Select role for {self.emp_pos}", font=font3)
        self.role_label.pack(pady=(30, 10))
        self.selected_role = tk.StringVar()
        self.selected_role.set(self.emp_pos)
        roles = [("HR", "HR"), ("Employee", "Employee")] if self.emp_pos == "HR" else [("Manager", "Manager"),
                                                                                       ("Employee", "Employee")]
        for role_text, role_value in roles:
            role_radio_button = ctk.CTkRadioButton(master=self.frame, text=role_text, variable=self.selected_role,
                                                   value=role_value, font=font3)
            role_radio_button.pack()
        self.continue_button = ctk.CTkButton(master=self.frame, text="Continue", font=font2, fg_color="#4e8d7c",
                                             hover_color="#34675c",
                                             command=self.on_continue)
        self.continue_button.pack(pady=20)

    def on_continue(self):
        if self.selected_role.get() == 'Manager':
            ManagerAccessFrame(self.master, self.emp_id)
        elif self.selected_role.get() == 'HR':
            HRAccessFrame(self.master, self.emp_id)
        elif self.selected_role.get() == 'Employee':
            EmployeeAccessFrame(self.master, self.emp_id)
        else:
            messagebox.showerror("Error", "Please choose a role")
