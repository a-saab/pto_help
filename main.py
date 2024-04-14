import tkinter as tk
import customtkinter as ctk
from login import LoginFrame

app = ctk.CTk()
app.title('PTO')
app.geometry("800x500")
app.configure(bg="#121212")

if __name__ == "__main__":
    login_frame = LoginFrame(app)
    app.mainloop()
