import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import training_data as td


# Define the number of runs 
num_runs = 10  # Change this to the desired number of runs

# Create an empty dictionary to store the total importance for each feature
df = td.gather_training_data(4)
total_importance = {feature: 0.0 for feature in df.drop(columns=['Tm', 'EXP']).columns}

# Run the loop multiple times
for _ in range(num_runs):
    
    # Separate the features (X) and the target variable (y)
    X = df.drop(columns=['Tm', 'EXP'])  # Exclude 'Tm' and 'EXP' columns
    y = df['EXP']
    
    # Initialize a Random Forest Regressor model (you can choose other models as well)
    model = RandomForestRegressor()
    
    # Fit the model on the data
    model.fit(X, y)
    
    # Get feature importances
    feature_importances = model.feature_importances_
    
    # Add the importance values to the total_importance dictionary
    total_importance = {feature: total_importance[feature] + importance for feature, importance in zip(X.columns, feature_importances)}

# Calculate the average importance for each feature
average_importance = {feature: total / num_runs for feature, total in total_importance.items()}

# Create a DataFrame to store feature names and their average importances
average_importance_df = pd.DataFrame({'Feature': average_importance.keys(), 'Average Importance': average_importance.values()})

# Sort the features by average importance in descending order
average_importance_df = average_importance_df.sort_values(by='Average Importance', ascending=False)

# Print the top features with average importance
print(average_importance_df['Feature'].head(5).tolist())
