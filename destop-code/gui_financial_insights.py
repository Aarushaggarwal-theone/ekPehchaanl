import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt

# Create main application window
root = tk.Tk()
root.title("Family Financial Insights")
root.geometry("800x600")

# Global variables to hold user data
user_data = None
user_clusters = None
rf_model_saving = RandomForestRegressor(n_estimators=100, random_state=0)
rf_model_investment = RandomForestRegressor(n_estimators=100, random_state=0)

# Function to set financial goals
def set_goals():
    goal_saving = saving_goal_entry.get()
    goal_investment = investment_goal_entry.get()
    try:
        goal_saving = float(goal_saving)
        goal_investment = float(goal_investment)
        messagebox.showinfo("Goals Set", f"Saving Goal: {goal_saving}, Investment Goal: {goal_investment}")
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numeric values for goals.")

# Function to upload financial data
def upload_data():
    global user_data
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path:
        try:
            user_data = pd.read_csv(file_path)
            messagebox.showinfo("Data Uploaded", "Your financial data has been uploaded successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read the file: {e}")

# Function to perform clustering and show similar families
def show_similar_families():
    global user_clusters
    if user_data is None:
        messagebox.showerror("No Data", "Please upload your financial data first.")
        return

    try:
        # Features available for clustering from the provided CSV
        available_features = ['Salary_Earned', 'Amount_Spent_on_Necessities', 
                              'Amount_Spent_on_Luxuries', 'Amount_Saved', 
                              'Amount_Invested', 'Avg_Risk_Per_Investment_%']
        
        # Ensure 'User_ID' is excluded during clustering
        if 'User_ID' in user_data.columns:
            user_data.drop(columns=['User_ID'], inplace=True, errors='ignore')

        # Use available numeric features for clustering
        X = user_data[available_features]
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Applying KMeans clustering
        kmeans = KMeans(n_clusters=4, random_state=0)
        user_data['Cluster'] = kmeans.fit_predict(X_scaled)

        user_clusters = user_data
        
        # Display a plot of clusters
        plt.figure(figsize=(10, 7))
        plt.scatter(X_scaled[:, 0], X_scaled[:, 1], c=user_data['Cluster'], cmap='viridis')
        plt.xlabel('Salary Earned')
        plt.ylabel('Amount Spent on Necessities')
        plt.title('User Clusters')
        plt.colorbar()
        plt.show()

        messagebox.showinfo("Clustering Complete", "Similar families have been identified and visualized.")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to cluster data: {e}")

# Function to provide insights based on similar families
def get_insights():
    if user_data is None or user_clusters is None:
        messagebox.showerror("No Data", "Please upload data and run clustering first.")
        return

    try:
        # Filter the available features for the Random Forest model
        X = user_data[['Salary_Earned', 'Amount_Spent_on_Necessities', 
                       'Amount_Spent_on_Luxuries', 'Amount_Saved', 
                       'Amount_Invested', 'Avg_Risk_Per_Investment_%']]

        # Generate target variables for savings and investment goals
        y_saving = user_data['Saving_Goals_%_Match']
        y_investment = user_data['Investment_Goals_%_Match']

        # Split data for model training
        X_train_saving, X_test_saving, y_train_saving, y_test_saving = train_test_split(X, y_saving, test_size=0.2, random_state=0)
        X_train_investment, X_test_investment, y_train_investment, y_test_investment = train_test_split(X, y_investment, test_size=0.2, random_state=0)

        # Train Random Forest models
        rf_model_saving.fit(X_train_saving, y_train_saving)
        rf_model_investment.fit(X_train_investment, y_train_investment)

        y_pred_saving = rf_model_saving.predict(X_test_saving)
        y_pred_investment = rf_model_investment.predict(X_test_investment)

        # Display insights
        insights_text.delete("1.0", tk.END)
        insights_text.insert(tk.END, f"Predicted Saving Goals (Sample): {y_pred_saving[:5]}\n")
        insights_text.insert(tk.END, f"Predicted Investment Goals (Sample): {y_pred_investment[:5]}\n")
        insights_text.insert(tk.END, "Insights on your financial habits will be displayed here...")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate insights: {e}")

# GUI Elements
tk.Label(root, text="Set Your Financial Goals").pack(pady=10)
frame_goals = tk.Frame(root)
frame_goals.pack(pady=5)
tk.Label(frame_goals, text="Saving Goal:").grid(row=0, column=0)
saving_goal_entry = tk.Entry(frame_goals)
saving_goal_entry.grid(row=0, column=1)
tk.Label(frame_goals, text="Investment Goal:").grid(row=1, column=0)
investment_goal_entry = tk.Entry(frame_goals)
investment_goal_entry.grid(row=1, column=1)
tk.Button(root, text="Set Goals", command=set_goals).pack(pady=10)

tk.Button(root, text="Upload Financial Data", command=upload_data).pack(pady=10)
tk.Button(root, text="Show Similar Families", command=show_similar_families).pack(pady=10)
tk.Button(root, text="Get Insights", command=get_insights).pack(pady=10)

insights_text = tk.Text(root, height=10, width=80)
insights_text.pack(pady=20)

# Run the GUI loop
root.mainloop()
