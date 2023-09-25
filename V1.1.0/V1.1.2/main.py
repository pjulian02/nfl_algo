# IMPORTS ##############################
import html_functions
import train_data
########################################

past_data = html_functions.scrape_website(start=1, offset=4)
print(train_data.training(100, past_data))

#added consolidate list capabilities
#fixed bug where stats werent able to be gathered for current year 
#added file to train data
#'
