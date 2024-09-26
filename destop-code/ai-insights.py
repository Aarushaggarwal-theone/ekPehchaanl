#this is a sample of a rfr model, 
# once we integrate users on our platform and learn from their data + integrate our expense categorization feature to classify each expense, 
# we can do a much more detailed analysis and feed the data into a recommendation system or a gpt model to generate data driven insights for our users.

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor

df = pd.read_csv('financial_data.csv')

most_recent_month = df.iloc[-1]

top_saving_goals_months = df.nlargest(5, 'Saving_Goals_%_Match')
top_investment_goals_months = df.nlargest(5, 'Investment_Goals_%_Match')

X = df.drop(columns=['Month',s 'Saving_Goals_%_Match', 'Investment_Goals_%_Match'])
y_saving = df['Saving_Goals_%_Match']
y_investment = df['Investment_Goals_%_Match']

X_train_saving, X_test_saving, y_train_saving, y_test_saving = train_test_split(X, y_saving, test_size=0.2, random_state=0)
X_train_investment, X_test_investment, y_train_investment, y_test_investment = train_test_split(X, y_investment, test_size=0.2, random_state=0)

rf_saving = RandomForestRegressor(n_estimators=100, random_state=0)
rf_saving.fit(X_train_saving, y_train_saving)
y_pred_saving = rf_saving.predict(X_test_saving)

rf_investment = RandomForestRegressor(n_estimators=100, random_state=0)
rf_investment.fit(X_train_investment, y_train_investment)
y_pred_investment = rf_investment.predict(X_test_investment)

importances_saving = rf_saving.feature_importances_
importances_investment = rf_investment.feature_importances_

features = X.columns
importances_df = pd.DataFrame({
    'Feature': features,
    'Importance_for_Saving_Goals': importances_saving,
    'Importance_for_Investment_Goals': importances_investment
})

importances_df = importances_df.sort_values(by='Importance_for_Saving_Goals', ascending=False)

important_factors_saving = importances_df[importances_df['Importance_for_Saving_Goals'] > 0.1]['Feature'].tolist()
important_factors_investment = importances_df[importances_df['Importance_for_Investment_Goals'] > 0.1]['Feature'].tolist()

