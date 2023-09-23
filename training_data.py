'''
:Author Philip Julian
:Date 12 September 2023

:Goal To gather training data from the past four years 
    Training Data:
        Historical Data used to train (teach) algorithm on which stats are important and which to avoid

        Typically contains the last 4 years combined in each sport

        After identifying impactful stats, training data is no longer used
'''

# IMPORTS ##############################
from datetime import datetime
import requests
from bs4 import BeautifulSoup, Comment
import pandas as pd
########################################

def grab_url(offset: int) -> str:
    """
    creats modified url based on users needs

    :param offset (int): what year of stats you would like to return {current_year - offset}
    :return (str): a string contianing the modified url for specific year
    """ 
    return f'https://www.pro-football-reference.com/years/{datetime.now().year - offset}/#all_team_stats'


def modify_html_code(offset: int) -> str:
    """
    modifies the html code to uncomment the needed table

    :return (str): a string contianing the modified html code for specified url
    """
    response = requests.get(grab_url(offset))
    soup = BeautifulSoup(response.text, 'html.parser')

    comments = soup.find_all(string=lambda string: isinstance(string, Comment))
    
    target_start = '<div class="table_container" id="div_team_stats">'
    target_end = '</div>'

    # Loop through comments and uncomment the desired portion
    for comment in comments:
        if target_start in comment and target_end in comment:
            # Extract the content between the target_start and target_end
            content_to_uncomment = comment.split(target_start)[1].split(target_end)[0]
            
            # Replace the comment with the uncommented content
            comment.replace_with(BeautifulSoup(content_to_uncomment, 'html.parser'))

    return str(soup.prettify())


def append_list(current_data: list, compiled_data: list) -> list:
    """
    combines all training data into a single list

    :param current_data (pd.Dataframe):
    :param compiled_data (pd.Dataframe): 
    :return (list): single list containing all of teams data
    """ 
    for item in current_data:
        if 'Washington' in item[0]:
            item[0] = 'Washington Commanders'
        elif 'Raiders' in item[0]:
            item[0] = 'Las Vegas Raiders'

    compiled_data += current_data
    return compiled_data

def consolidate_list(combined_list: list, column_headers: list) -> pd.DataFrame:
    """
    combi

    :param 
    :param 
    :return (list): 
    """ 
    for row in combined_list:
        for i in range(1, len(row)):
            if row[i] == '': row[i] = 0
            else: row[i] = float(row[i])

    aggregated_data=[]
    # Loop through the combined list to aggregate data by team name
    for item in combined_list:
        team_name = item[0]
        found = False

        # Check if the team data already exists in the aggregated_data list
        for data in aggregated_data:
            if data[0] == team_name:
                for i in range(1, len(data)):
                    data[i] += item[i]
                found = True
                break

        # If not found, add the team data to aggregated_data
        if not found:
            aggregated_data.append(item)

    # print(len(aggregated_data[0]))
    # print(len(column_headers))

    return pd.DataFrame(aggregated_data, columns=column_headers).sort_values(by='Tm', ascending=True) # Create the DataFrame


def gather_training_data(offset: int) -> pd.DataFrame:
    """
    grabs the table elements from the html code and saves it to a pandas dataframe

    :param html (str): string containing the html code for specified website
    :return: None
    """ 
    compiled_data = []
    for _ in range(1, offset+1):
        soup = BeautifulSoup(modify_html_code(_), 'html.parser')
        offensive_stats = soup.find_all('div', id='all_team_stats')

        column_headers, team_data = [], []
        for div in offensive_stats:
            for th in div.find_all('th', {'scope':'col'}):
                column_headers.append(th.get_text().strip())
            for tr in div.find_all('tr')[2:-3]:
                team_stats = [td.get_text().strip() for td in tr.find_all('td')]
                team_data.append(team_stats)

        compiled_data = append_list(team_data, compiled_data)

    return consolidate_list(compiled_data, column_headers[1:])


# print(gather_training_data(4))
# print(grab_url(1))












# def save_to_html(html: str, filename: str) -> None:
#     with open(filename,'w', encoding='utf-8') as file:
#         file.write(html)
    
# Merge the two DataFrames based on the "Team" column
# combined_df = pd.merge(df_current, df_last_year, on='Team', how='outer')