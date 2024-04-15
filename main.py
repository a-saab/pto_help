import tkinter as tk
import customtkinter as ctk
from login import LoginFrame
import sqlite3

conn = sqlite3.connect('pto.db')
cursor = conn.cursor()


# Create the employee table with EmpID as primary key
cursor.execute('''
    CREATE TABLE IF NOT EXISTS user(
    UserID INTEGER PRIMARY KEY AUTOINCREMENT,
    FName VARCHAR(20) NOT NULL,
    LName VARCHAR(20) NOT NULL,
    DOB TEXT,
    Address VARCHAR(255),
    Email VARCHAR(30),
    Phone INT)''')

# Check if there's any data in the table
cursor.execute('SELECT COUNT(*) FROM user')
if cursor.fetchone()[0] == 0:  # If the table is empty, then insert data
    user_data = [
        ('John', 'Doe', '05/15/80', '123 Main St, Toronto, ON, M5V 1J1', 'john.doe@email.com', 1234567890),
        ('Jane', 'Smith', '10/20/85', '456 Elm St, Vancouver, BC, V6C 1A1', 'jane.smith@email.com', 9876543210),
        ('Michael', 'Johnson', '03/08/76', '789 Oak St, Montreal, QC, H3B 4G7', 'michael.johnson@email.com', 5551234567),
        ('Emily', 'Brown', '12/25/90', '101 Pine St, Calgary, AB, T2P 5K8', 'emily.brown@email.com', 4447890123),
        ('David', 'Lee', '07/14/88', '222 Maple St, Ottawa, ON, K1P 1J1', 'david.lee@email.com', 3335678901)
    ]
    cursor.executemany('''
        INSERT INTO user (FName, LName, DOB, Address, Email, Phone)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', user_data)
    conn.commit()


#  PTORequest SQL
cursor.execute('''
    CREATE TABLE IF NOT EXISTS PTORequest(
    PTOID INTEGER PRIMARY KEY AUTOINCREMENT,
    EmpID INT NOT NULL,
    PTODate TEXT, /*for created date in our form*/
    PTOType INT,
    PTOReason VARCHAR(200),
    PTOStartDate TEXT,
    PTOEndDate TEXT,
    FOREIGN KEY (EmpID) REFERENCES employee(EmpID))''')

# Check if there's any data in the table
cursor.execute('SELECT COUNT(*) FROM PTORequest')
if cursor.fetchone()[0] == 0:  # If the table is empty, then insert data
    ptorequest_data = [
        (10000, '04/14/24', 1, 'Family vacation', '04/20/24', '04/25/24'),
        (11111, '04/14/24', 2, 'Flu', '04/10/24', '04/12/24'),
        (12345, '04/14/24', 1, 'Attending a family event', '04/18/24', '04/19/24'),
        (22222, '04/14/24', 1, 'Traveling abroad', '05/01/24', '05/10/24'),
        (54321, '04/14/24', 2, 'Food poisoning', '04/14/24', '04/16/24')
    ]
    cursor.executemany('''
        INSERT INTO PTORequest (EmpID, PTODate, PTOType, PTOReason, PTOStartDate, PTOEndDate)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', ptorequest_data)
    conn.commit()


    # create data for PTO Documentation
cursor.execute('''
    CREATE TABLE IF NOT EXISTS PTODocument(
    PTODOCID INTEGER PRIMARY KEY AUTOINCREMENT,
    PTOID INT NOT NULL,
    PDFData BLOB NOT NULL,
    FOREIGN KEY (PTOID) REFERENCES PTORequest(PTOID))''')



app = ctk.CTk()
app.title('PTO')
app.geometry("800x500")
app.configure(bg="#121212")

if __name__ == "__main__":
    login_frame = LoginFrame(app)
    app.mainloop()
