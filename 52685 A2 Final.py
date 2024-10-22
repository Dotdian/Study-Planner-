import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tktooltip import ToolTip
import pandas as pd
from datetime import datetime 

class App:
    def __init__(self, root):
        #creates a window
        self.root = root
        self.root.title("Study Planner")
        self.root.configure(bg = "white")
    
        self.create_input_form()
        self.data_records = pd.DataFrame(columns =["Date", "Subject", "Task", "Notes"])


    def create_input_form(self):
        #clears the interface 
        for widget in self.root.winfo_children():
            widget.destroy()

        # date input
        label_date = tk.Label(self.root,
                              text = "Date: ",
                              bg = "white"
                              )
        label_date.grid(row = 0, column = 0, padx = 10, pady = 5, sticky = "e")
        self.entry_date = tk.Entry(self.root, bg = "white")
        self.entry_date.grid(row = 0, column = 1, padx = 10, pady = 5)

        #subject input
        label_subject = tk.Label(self.root,
                              text = "Subject: ",
                              bg = "white"
                              )
        label_subject.grid(row = 1, column = 0, padx = 10, pady = 5, sticky = "e")
        self.entry_subject = tk.Entry(self.root, bg = "white")
        self.entry_subject.grid(row = 1, column = 1, padx = 10, pady = 5)

        #task drop down menu
        label_task = tk.Label(self.root,
                              text = "Task: ",
                              bg = "white"
                              )
        label_task.grid(row = 2, column = 0, padx = 10, pady = 5, sticky = "e")
        self.combo_task = ttk.Combobox(self.root, values = ["Assignment", "Assessment"])
        self.combo_task.grid(row = 2, column = 1, padx = 10, pady = 5)

        #notes input
        label_notes = tk.Label(self.root,
                              text = "Notes: ",
                              bg = "white"
                              )
        label_notes.grid(row = 3, column = 0, padx = 10, pady = 5, sticky = "e")
        self.text_notes = tk.Text(self.root, height = 5, width = 30, bg = "white")
        self.text_notes.grid(row = 3, column = 1, padx = 10, pady = 5)

        # Next and Exit and Info and View buttons
        #exit_button 
        exit_button = tk.Button(self.root,
                                text = "Exit",
                                cursor = "hand2",
                                command = self.exit_app
                                )
        exit_button.grid(row = 4, column = 0, padx = 10, pady = 5, sticky = "e")

        #view button 
        view_button = tk.Button(self.root,
                                text = "View",
                                cursor = "hand2",
                                command = self.show_data
                                )
        view_button.grid(row = 4, column = 1, padx = 10, pady = 5, sticky = "e")

        #info button
        info_button = tk.Button(self.root,
                                text = "i",
                                )
        info_button.grid(row = 0, column = 2)
        ToolTip(info_button, msg = "Input the tasks in this window")
        
        #next button
        next_button = tk.Button(self.root,
                                text = "Next",
                                cursor = "hand2",
                                command = self.on_next
                                )
        next_button.grid(row = 4, column= 2, padx = 10, pady = 5, sticky = "e")

    def on_next(self):
        if self.validate_date() and self.validate_task():
            self.show_data()

    def validate_date(self):
        #validate date 
        date = self.entry_date.get()
        
        try: 
            datetime.strptime(date, "%d/%m/%Y")
            return True 
        except ValueError:
            messagebox.showerror("Invalid Date", "Please Enter The Date in DD/MM/YYYY Format")
            return False
        
    def validate_task(self):
        #validate task 
        task = self.combo_task.get()
        if task not in ["Assessment", "Assignment"]:
            messagebox.showerror("Invalid Task", "Please Select Either 'Assessment' or 'Assignment'.")
            return False
        return True 

    def show_data(self):
        #get user input
        date = self.entry_date.get()
        subject = self.entry_subject.get()
        task = self.combo_task.get()
        notes = self.text_notes.get("1.0", tk.END).strip()

        #saves the data in dataframe 
        new_record = pd.DataFrame([[date, subject, task, notes]], columns = self.data_records.columns)
        self.data_records = pd.concat([self.data_records, new_record], ignore_index = True)

        for widget in self.root.winfo_children():
            widget.destroy()
        
        #create table
        columns = self.data_records.columns.tolist()
        tree = ttk.Treeview(self.root, columns = columns , show = "headings")

        #create headings
        for col in columns:
            tree.heading(col, text = col)

        #inserts all the record into the table
        for _, record in self.data_records.iterrows():
            tree.insert("", "end", values = record.tolist())

        #displays the table
        tree.pack(pady = 20)

        #exit button
        exit_button = tk.Button(self.root,
                                text = "Exit",
                                cursor = "hand2",
                                command = self.exit_app
                                )
        exit_button.pack(side = tk.LEFT, padx = 10, pady = 20)

        #add more button
        add_more_button = tk.Button(self.root,
                                    text = "Add More",
                                    cursor = "hand2",
                                    command = self.create_input_form
                                    )
        add_more_button.pack(side = tk.RIGHT, padx = 10, pady = 20)


    def exit_app(self):
        self.root.quit()
        

root = tk.Tk()
app = App(root)
root.mainloop()