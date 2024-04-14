import tkinter as tk
import customtkinter as ctk
from fonts import *

class HRAccessFrame:
    def __init__(self, master, emp_id):
        self.master = master
        self.emp_id = emp_id
        self.frame = ctk.CTkFrame(master=self.master, corner_radius=10, width=500, height=400)
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.welcome_label = ctk.CTkLabel(master=self.frame, text=f"Welcome HR {self.emp_id}", font=font2)
        self.welcome_label.pack(pady=20)
        self.menu_page_label = ctk.CTkLabel(master=self.frame, text="Menu Page", font=font1)
        self.menu_page_label.pack(pady=(10, 20))
        self.document_button = ctk.CTkButton(master=self.frame, text="Document", font=font3)
        self.document_button.pack(pady=10, fill='x', padx=50)
        self.history_button = ctk.CTkButton(master=self.frame, text="History", font=font3)
        self.history_button.pack(pady=10, fill='x', padx=50)
        self.plan_button = ctk.CTkButton(master=self.frame, text="Plan", font=font3)
        self.plan_button.pack(pady=10, fill='x', padx=50)
        self.request_button = ctk.CTkButton(master=self.frame, text="Request", font=font3)
        self.request_button.pack(pady=10, fill='x', padx=50)
        self.schedule_button = ctk.CTkButton(master=self.frame, text="Schedule", font=font3)
        self.schedule_button.pack(pady=10, fill='x', padx=50)
