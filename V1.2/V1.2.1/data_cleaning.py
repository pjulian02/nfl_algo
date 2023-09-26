# IMPORTS ##############################
import pandas as pd
########################################

def off_cleanup(compiled_list: list, column_headers: list) -> pd.DataFrame:
    # Create a DataFrame from the combined_list with column_headers
    df = pd.DataFrame(compiled_list, columns=column_headers).replace('',0) # Replaces any empty values with 0
    


    # Grabs all numeric columns (columns that arent team name)
    for col in [col for col in df.columns if col != 'Tm']:
        df[col] = df[col].astype(float)

    return df.groupby('Tm').sum().reset_index()
    # print(df)

def rfr_training_cleanup(data: pd.DataFrame, importance: float) -> list:
    selected_features = data.loc[data['Average Importance'] > importance, 'Feature'].tolist()
    if "TO%" not in selected_features: selected_features.append("TO%")

    return selected_features

def edit_columns(data: pd.DataFrame, cols: list, remove_columns: bool) -> pd.DataFrame:
    if remove_columns:
        return data.drop(columns=cols)
    else:
        return data[[col for col in cols if col in data.columns]]