# IMPORTS ##############################
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
########################################

def training(iterations: int, data: pd.DataFrame) -> list:
    modified_data = data.drop(columns=['Tm','G','1stPy','Int','FL','EXP'])
    total_importance = {feature: 0.0 for feature in modified_data.columns}

    for _ in range(iterations):
        model = RandomForestRegressor() # Intializes RFR ML Model
        model.fit(modified_data, data['EXP'])

        total_importance = {feature:total_importance[feature]+importance for feature, importance in zip(modified_data.columns, model.feature_importances_)}

    avg_importance = {feature: total / iterations for feature, total in total_importance.items()}
    importance_df = pd.DataFrame({'Feature': avg_importance.keys(), 'Average Importance': avg_importance.values()}).sort_values(by='Average Importance', ascending=False)

    return importance_df

# print(average_importance_df['Feature'].head(5).tolist())
