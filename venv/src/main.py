from database import Database
from gui import PayrollApp
import tkinter as tk

if __name__ == "__main__":
    # Database configuration
    db = Database(dbname="localhost", user="nomina", password="1234", host="localhost", port="5432")

    # Create the GUI
    root = tk.Tk()
    app = PayrollApp(root, db)
    root.mainloop()

    # Close the database connection when the program exits
    db.close()