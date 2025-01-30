import tkinter as tk
from tkinter import ttk, messagebox
from database import Database
from payroll import Payroll
import pandas as pd

class PayrollApp:
    def __init__(self, root, db):
        self.root = root
        self.db = db
        self.setup_gui()

    def setup_gui(self):
        self.root.title("Payroll Program")

        # First Box: Worker Data
        frame_data = ttk.LabelFrame(self.root, text="Worker Data")
        frame_data.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(frame_data, text="Full Name:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_name = ttk.Entry(frame_data)
        self.entry_name.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_data, text="ID Number:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_id = ttk.Entry(frame_data)
        self.entry_id.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame_data, text="Professional Category:").grid(row=2, column=0, padx=5, pady=5)
        self.entry_category = ttk.Entry(frame_data)
        self.entry_category.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(frame_data, text="Base Salary:").grid(row=3, column=0, padx=5, pady=5)
        self.entry_salary = ttk.Entry(frame_data)
        self.entry_salary.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(frame_data, text="Start Date (YYYY-MM-DD):").grid(row=4, column=0, padx=5, pady=5)
        self.entry_start_date = ttk.Entry(frame_data)
        self.entry_start_date.grid(row=4, column=1, padx=5, pady=5)

        ttk.Button(frame_data, text="Save Data", command=self.save_worker_data).grid(row=5, column=0, columnspan=2, pady=10)

        # Payroll Calculation
        ttk.Button(frame_data, text="Calculate Payroll", command=self.calculate_payroll).grid(row=6, column=0, columnspan=2, pady=10)
        self.label_result = ttk.Label(frame_data, text="")
        self.label_result.grid(row=7, column=0, columnspan=2, pady=5)

        # Second Box: Payroll Report
        frame_report = ttk.LabelFrame(self.root, text="Payroll Report")
        frame_report.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        ttk.Button(frame_report, text="Generate Payroll Report", command=self.generate_payroll_report).grid(row=0, column=0, pady=10)

        # Treeview to display worker data
        self.tree = ttk.Treeview(self.root, columns=("ID", "Full Name", "ID Number", "Category", "Salary", "Start Date"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Full Name", text="Full Name")
        self.tree.heading("ID Number", text="ID Number")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Salary", text="Salary")
        self.tree.heading("Start Date", text="Start Date")
        self.tree.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        # Load initial data
        self.load_worker_data()

    def save_worker_data(self):
        full_name = self.entry_name.get()
        identification_number = self.entry_id.get()
        professional_category = self.entry_category.get()
        base_salary = float(self.entry_salary.get())
        start_date = self.entry_start_date.get()

        if not all([full_name, identification_number, professional_category, base_salary, start_date]):
            messagebox.showwarning("Input Error", "All fields are required!")
            return

        if self.db.save_worker(full_name, identification_number, professional_category, base_salary, start_date):
            messagebox.showinfo("Success", "Worker data saved successfully!")
            self.load_worker_data()

    def load_worker_data(self):
        rows = self.db.get_workers()
        for row in self.tree.get_children():
            self.tree.delete(row)
        for row in rows:
            self.tree.insert("", "end", values=row)

    def calculate_payroll(self):
        base_salary = float(self.entry_salary.get())
        start_date = self.entry_start_date.get()

        total_salary, error = Payroll.calculate_salary(base_salary, start_date)
        if error:
            messagebox.showerror("Calculation Error", error)
        else:
            self.label_result.config(text=f"Total Salary: ${total_salary:.2f}")

    def generate_payroll_report(self):
        rows = self.db.get_workers()
        df = pd.DataFrame(rows, columns=["ID", "Full Name", "ID Number", "Category", "Salary", "Start Date"])
        df["Days Worked"] = (pd.to_datetime("now") - pd.to_datetime(df["Start Date"])).dt.days
        df["Total Salary"] = (df["Salary"] / 30) * df["Days Worked"]

        report_window = tk.Toplevel(self.root)
        report_window.title("Payroll Report")
        text = tk.Text(report_window)
        text.insert(tk.END, df.to_string(index=False))
        text.pack()