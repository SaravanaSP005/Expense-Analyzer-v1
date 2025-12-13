import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox, filedialog
import pandas as pd
from datetime import datetime

class ExpenseAnalyzerApp:
    VERSION = "1.0.0"
    def __init__(self, root):
        self.root = root
        self.root.title("💰 Expense Dashboard")
        self.root.geometry("1000x600")

        # Store data
        self.user_list = []
        self.expense_list = []

        # Page container
        self.container = ttkb.Frame(root)
        self.container.pack(fill="both", expand=True)

        # Pages
        self.frames = {}
        for F in (UserPage, ExpensePage):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(UserPage)

    def show_frame(self, page):
        self.frames[page].tkraise()


class UserPage(ttkb.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ttkb.Label(self, text="Number of Users:").grid(row=0, column=0, padx=5, pady=5)
        self.num_users_entry = ttkb.Entry(self, width=5)
        self.num_users_entry.grid(row=0, column=1)

        ttkb.Button(self, text="OK", command=self.generate_user_fields).grid(row=0, column=2, padx=5)

        self.user_frame = ttkb.Frame(self)
        self.user_frame.grid(row=1, column=0, columnspan=3, pady=10)

        self.user_entries = []

        ttkb.Button(self, text="Save Users", command=self.save_users).grid(row=2, column=0, pady=10)

    def generate_user_fields(self):
        for widget in self.user_frame.winfo_children():
            widget.destroy()
        self.user_entries = []

        try:
            num = int(self.num_users_entry.get())
            if num < 1: raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Enter valid number")
            return

        for i in range(num):
            ttkb.Label(self.user_frame, text=f"Username {i+1}").grid(row=i, column=0)
            username_entry = ttkb.Entry(self.user_frame)
            username_entry.grid(row=i, column=1)

            ttkb.Label(self.user_frame, text=f"ShortName {i+1}").grid(row=i, column=2)
            short_entry = ttkb.Entry(self.user_frame)
            short_entry.grid(row=i, column=3)

            self.user_entries.append({"username": username_entry, "shortname": short_entry})

    def save_users(self):
        users = []
        for e in self.user_entries:
            u = e["username"].get().strip()
            s = e["shortname"].get().strip()
            if u and s:
                continue  # Skip empty entries

            # Check if ShortName is already used
            duplicate = False
            for data in users:
                if data["ShortName"] == s:
                    duplicate = True
                    break

            if duplicate:
                messagebox.showerror("Error", "ShortName '{}' must be unique.".format(s))
                return
        if not users:
            messagebox.showerror("Error", "No users entered")
            return

        self.controller.user_list = users
        self.controller.show_frame(ExpensePage)


class ExpensePage(ttkb.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.sno = 1

        # Input fields
        ttkb.Label(self, text="Date (dd-mm-yyyy):").grid(row=0, column=0)
        self.date_entry = ttkb.Entry(self)
        self.date_entry.grid(row=0, column=1)

        ttkb.Label(self, text="Expense Name:").grid(row=1, column=0)
        self.expense_entry = ttkb.Entry(self)
        self.expense_entry.grid(row=1, column=1)

        ttkb.Label(self, text="Amount:").grid(row=2, column=0)
        self.amount_entry = ttkb.Entry(self)
        self.amount_entry.grid(row=2, column=1)

        ttkb.Label(self, text="Select Persons:").grid(row=3, column=0)
        self.person_listbox = tk.Listbox(self, selectmode="multiple", height=5)
        self.person_listbox.grid(row=3, column=1)

        ttkb.Button(self, text="Add Expense", command=self.add_expense).grid(row=4, column=0, pady=5)
        ttkb.Button(self, text="Save CSV", command=self.save_csv).grid(row=4, column=1, pady=5)

        # Treeview
        self.tree = ttkb.Treeview(self, columns=("Sno","Date", "Expense", "Amount", "Persons", "Count"), show="headings")
        for c in self.tree["columns"]:
            self.tree.heading(c, text=c)
        self.tree.grid(row=5, column=0, columnspan=2, pady=10)

    def tkraise(self, aboveThis=None):
        super().tkraise(aboveThis)
        self.person_listbox.delete(0, "end")
        for u in self.controller.user_list:
            self.person_listbox.insert("end", u["ShortName"])

    def add_expense(self):
        date = self.date_entry.get().strip()
        expense = self.expense_entry.get().strip()
        amount = self.amount_entry.get().strip()
        selected_indices = self.person_listbox.curselection()
        persons = [self.person_listbox.get(i) for i in selected_indices]
        count = len(persons)

        if not date or not expense or not amount or count == 0:
            messagebox.showerror("Error", "All fields required")
            return
        try:
            amount = float(amount)
        except:
            messagebox.showerror("Error", "Amount must be a number")
            return

        entry = {"Sno": self.sno, "Date": date, "Expense": expense, "Amount": amount, "Persons": persons, "Count": count}
        self.controller.expense_list.append(entry)

        self.tree.insert("", "end", values=(self.sno, date, expense, amount, ",".join(persons), count))
        self.sno += 1

        # Clear inputs
        self.date_entry.delete(0, "end")
        self.expense_entry.delete(0, "end")
        self.amount_entry.delete(0, "end")
        self.person_listbox.selection_clear(0, "end")

    def save_csv(self):
        if not self.controller.expense_list:
            messagebox.showerror("Error", "No expenses to save")
            return
        df = pd.DataFrame(self.controller.expense_list)
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files","*.csv")])
        if file_path:
            df.to_csv(file_path, index=False)
            messagebox.showinfo("Success", f"CSV saved to {file_path}")