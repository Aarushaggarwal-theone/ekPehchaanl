#sample clustering algo for random 20 users divided into 4 clusters, scatter plot also given for ease of understandinng. 

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

np.random.seed(0)

users = []
for user_id in range(1, 21):
    data = {
        "User_ID": [user_id] * 36,
        "Month": pd.date_range(start="2021-01-01", periods=36, freq='M'),
        "Salary_Earned": np.random.randint(4000, 7000, size=36),
        "Amount_Spent_on_Necessities": np.random.randint(1000, 3000, size=36),
        "Amount_Spent_on_Luxuries": np.random.randint(500, 2000, size=36),
        "Amount_Saved": np.random.randint(500, 3000, size=36),
        "Amount_Invested": np.random.randint(500, 3000, size=36),
        "Avg_Risk_Per_Investment_%": np.random.uniform(1, 15, size=36),
        "Saving_Goals_%_Match": np.random.uniform(50, 100, size=36),
        "Investment_Goals_%_Match": np.random.uniform(50, 100, size=36),
    }
    users.append(pd.DataFrame(data))

df_users = pd.concat(users, ignore_index=True)

csv_file_path = '/mnt/data/financial_data_multiple_users.csv'
df_users.to_csv(csv_file_path, index=False)

df_users = pd.read_csv('/mnt/data/financial_data_multiple_users.csv')

features = ["Salary_Earned", "Amount_Spent_on_Necessities", "Amount_Spent_on_Luxuries", 
            "Amount_Saved", "Amount_Invested", "Avg_Risk_Per_Investment_%"]

df_aggregated = df_users.groupby("User_ID")[features].mean().reset_index()

scaler = StandardScaler()
X = scaler.fit_transform(df_aggregated[features])

kmeans = KMeans(n_clusters=4, random_state=0)
df_aggregated['Cluster'] = kmeans.fit_predict(X)

plt.figure(figsize=(10, 7))
plt.scatter(X[:, 0], X[:, 1], c=df_aggregated['Cluster'], cmap='viridis')
plt.xlabel('Salary Earned')
plt.ylabel('Amount Spent on Necessities')
plt.title('User Clusters')
plt.colorbar()
plt.show()

df_aggregated.to_csv('/mnt/data/clustered_users.csv', index=False)
