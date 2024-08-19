import tkinter as tk
from tkinter import filedialog, messagebox
import sqlite3
import pandas as pd

def browse_db_file():
    filename = filedialog.askopenfilename(
        title="Select SQLite Database File",
        filetypes=(("SQLite Database Files", "*.db"), ("All Files", "*.*"))
    )
    db_file_path.set(filename)

def browse_output_folder():
    foldername = filedialog.askdirectory(
        title="Select Output Directory"
    )
    output_folder_path.set(foldername)

def generate_csv():
    db_path = db_file_path.get()
    output_path = output_folder_path.get()
    
    if not db_path or not output_path:
        messagebox.showwarning("Input Error", "Please select both the database file and the output directory.")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
    
        for table_name in tables:
            table_name = table_name[0]
            
            # Extract schema
            cursor.execute(f"PRAGMA table_info({table_name})")
            schema_info = cursor.fetchall()
            schema_df = pd.DataFrame(schema_info, columns=["cid", "name", "type", "notnull", "dflt_value", "pk"])
            schema_df.to_csv(f"{output_path}/{table_name}_schema.csv", index=False)
            
            # Extract data
            data_df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
            data_df.to_csv(f"{output_path}/{table_name}.csv", encoding='utf-8', index=False)
        
        conn.close()
        messagebox.showinfo("Success", "CSV files have been generated successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Set up the main window
root = tk.Tk()
root.title("SQLite to CSV Converter - By @Zeitgeist195")
root.resizable(width=False, height=False)
root.iconbitmap("zeit.ico")

# Define tkinter variables
db_file_path = tk.StringVar()
output_folder_path = tk.StringVar()

# Define and place the widgets
tk.Label(root, text="Select SQLite .db file:").grid(row=0, column=0, padx=12, pady=15, sticky="e")
tk.Entry(root, textvariable=db_file_path, width=50).grid(row=0, column=1, padx=12, pady=15)
tk.Button(root, text="Browse...", command=browse_db_file).grid(row=0, column=2, padx=12, pady=10)

tk.Label(root, text="Select output folder:").grid(row=1, column=0, padx=10, pady=12, sticky="e")
tk.Entry(root, textvariable=output_folder_path, width=50).grid(row=1, column=1, padx=12, pady=10)
tk.Button(root, text="Browse...", command=browse_output_folder).grid(row=1, column=2, padx=12, pady=10)

tk.Button(root, text="Generate CSV!", command=generate_csv).grid(row=2, columnspan=3, pady=20)

# Start the tkinter main loop
root.mainloop()
