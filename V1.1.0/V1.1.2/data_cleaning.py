# IMPORTS ##############################
import pandas as pd
########################################

def off_cleanup(compiled_list: list, column_headers: list) -> pd.DataFrame:
    # Create a DataFrame from the combined_list with column_headers
    df = pd.DataFrame(compiled_list, columns=column_headers).replace('',0).groupby('Tm').sum().reset_index()

    print(df)

    # Convert empty strings to 0 and other columns to float
    # df = df.apply(lambda x: x.astype(float) if x.name != 'Tm' else x.replace('', 0))

    # # Group by 'Tm' (team name) and sum the values in other columns
    # grouped = df.groupby('Tm').sum().reset_index()

    # return grouped.sort_values(by='Tm', ascending=True)
