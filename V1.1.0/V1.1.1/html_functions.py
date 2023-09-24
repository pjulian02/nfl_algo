eal# IMPORTS ##############################
from datetime import datetime
import requests
from bs4 import BeautifulSoup, Comment
########################################

def craft_url(offset: int) -> str:
    """
    creats modified url based on users needs

    :param offset (int): what year of stats you would like to return {current_year - offset}
    :return (str): a string contianing the modified url for specific year
    """ 
    return f'https://www.pro-football-reference.com/years/{datetime.now().year - offset}/#all_team_stats'
    # return f'https://www.pro-football-reference.com/years/2020/#all_team_stats'

def modify_html_code(url: str) -> str:
    """
    modifies the html code to uncomment the needed table

    :param html (str): url for which to grab the html code from
    :return (str): a string contianing the modified html code for specified url
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    comments = soup.find_all(string=lambda string: isinstance(string, Comment))
    
    # Uses BS4 to find all comments and sets designated start and end of comment area
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

def scrape_website(offset: int) -> list:
    """
    grabs the table elements from the html code and saves it to a pandas dataframe

    :param html (str): string containing the html code for specified website
    :return: None
    """ 
    compiled_data = [] # Holds the table grabbed from website
    for urls in range(1, offset+1):
        soup = BeautifulSoup(modify_html_code(craft_url(offset=offset)), 'html.parser')
        offensive_stats = soup.find_all('div', id='all_team_stats')
        column_headers, team_data = [], []

        for div in offensive_stats:
            for th in div.find_all('th',{'scope':'col'}):
                column_headers.append(th.get_text().strip())
            for tr in div.find_all('tr')[2:-3]:
                team_stats = [td.get_text().strip() for td in tr.find_all('td')]
                team_stats = ["Washington Commanders" if "Washington" in team_name else "Las Vegas Raiders" if "Raiders" in team_name else team_name for team_name in team_stats]
                team_data.append(team_stats)

                compiled_data += team_data
    
            # TODO: consolidate list function
        
scrape_website(4)
