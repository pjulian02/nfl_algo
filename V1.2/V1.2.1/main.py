# IMPORTS ##############################
import html_functions
import train_data
import data_cleaning
########################################


columns_of_importance = data_cleaning.rfr_training_cleanup(
    train_data.training(1000, html_functions.scrape_website(start=1, offset=4))
    , .0099
)
current_data = data_cleaning.edit_columns(
    html_functions.scrape_website(start=0, offset=0), 
    ["Tm"] + columns_of_importance, 
    remove_columns=False)

print(current_data)