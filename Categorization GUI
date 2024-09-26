import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import pandas as pd
import random

# Define the possible categories for transactions
categories = [
    "Food", "Luxury", "Furniture", "Transportation", "Groceries",
    "Utilities", "Entertainment", "Travel", "Clothing", "Electronics",
    "Health", "Education", "Insurance", "Home Improvement", "Miscellaneous"
]

# Function to load the transactions CSV file and randomly assign categories
def load_and_categorize_csv():
    global df_transactions
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        df_transactions = pd.read_csv(file_path)
        
        # Mapping card numbers to people for demonstration purposes
        card_to_person = {3456: "Rebecca", 4444: "John", 3696: "Adam"}
        df_transactions["Person"] = df_transactions["Card_Number"].map(card_to_person)

        # Randomly assign a category to each transaction
        df_transactions['Category'] = [random.choice(categories) for _ in range(len(df_transactions))]
        
        # Create a new DataFrame with only Transaction_ID and Category
        df_result = df_transactions[['Transaction_ID', 'Category']]
        
        # Show a success message
        messagebox.showinfo("Loaded", "CSV file loaded and categories assigned successfully!")

        # Print the Transaction_ID and Category for verification
        print(df_result.head())  # Display the first few rows of the result DataFrame

# Create the main application window
root = tk.Tk()
root.title("Transaction Data Uploader")

# Create and place buttons in the window
frame = ttk.Frame(root, padding="20")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Label to display instructions
ttk.Label(frame, text="Upload Transaction Data", font=("Arial", 16)).grid(row=0, column=0, columnspan=1)

# Upload CSV Button
upload_button = ttk.Button(frame, text="Upload CSV", command=load_and_categorize_csv)
upload_button.grid(row=1, column=0, padx=10, pady=10)

# Run the main loop
root.mainloop()
