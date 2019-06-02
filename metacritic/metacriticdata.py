# -*- coding: utf-8 -*-
"""
Created on Fri May 31 22:43:55 2019

@author: syeh3
"""

import urllib.request
from bs4 import BeautifulSoup
import csv  

def processGameDetailsMetacritic(game):
    """This function takes in a string argument in the form
    'game name (game platform)metascoreUser:user_scoreRelease Date:release_date'
    Returns a list
    1st element -> game metascore
    2nd element -> game name
    3rd element -> game platform
    4th element -> game user_score
    5th element -> game release_date
    Preconditions: game must have at least 1 set of parenthese and 1 colon
    """
    
    if game.count("(") == 0  or game.count(")") == 0 or game.count(":") == 0:
        #Checking preconditions
        print('Invalid game name string')
        return 
    
    game = game.replace('\n','')
    name = game[: game.find('(') - 1].strip()
    platform = game[game.rfind('(') + 1: game.rfind(')')]
    metascore = game[game.rfind(')') + 1: game.rfind('U')].strip()
    game_notitleplatform = game[game.rfind(')') + 1 :].strip()
    user_score = game_notitleplatform[game_notitleplatform.find(':') + 1: game_notitleplatform.find(':') + 4]
    release_date = game_notitleplatform[game_notitleplatform.rfind(':') + 1:]
    #String splicing
    
    print([name, platform, metascore, user_score, release_date])
    
    return [name, platform, metascore, user_score, release_date]


def csvWriter(file_name, data):
    """This function takes in a string argument for file name and list data
    for data to be written to a new csv file
    Note: overwrites files of the same name
    """
    with open(file_name + '.csv', 'w', newline ='', encoding='utf-8') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(data)
        
def lastPageNumber(year):
    """This function takes in an int year and returns the string form of the last 
    page number of that year's page of Metacritic
    Returns "0" if no last page/ first page is the last page
    Else returns last page
    """
    
    url = "https://www.metacritic.com/browse/games/score/metascore/year/all/filtered?sort=desc&year_selected=" + str(year) +"&page=0"
    url_headers = urllib.request.Request(url, headers={'User-Agent' : "Magic Browser"})
    html = urllib.request.urlopen(url_headers)
    soup = BeautifulSoup(html, 'lxml')
    
    last_page = soup.find("li", {"class": "page last_page"})

    if last_page is None:
        return "0"
    elif len(last_page) == 1:
        return last_page.text
    else:
        return last_page.text[1:]



csv_game_data = [['Year','Game','Platform','Metascore','User Score','Release Date']]
#csv list to be written out into csv file with column headings

year = 1995
#starting year

while year <= 2019:
    #ending year
    
    page = 0
    last_page = lastPageNumber(year)
    
    while (page < int(last_page)) or (page == 0 and int(last_page) == 0):
        #Conditions: page less than last_page or on the only page for that year
        print(page)
        print(last_page)
    
        url = "https://www.metacritic.com/browse/games/score/metascore/year/all/filtered?sort=desc&year_selected=" + str(year) +"&page=" + str(page)
        url_headers = urllib.request.Request(url, headers={'User-Agent' : "Magic Browser"})
        html = urllib.request.urlopen(url_headers)
        soup = BeautifulSoup(html, 'lxml')
        
        only_product = soup.find("li", {"class": "product game_product first_product last_product"})
        #extracts first, last and only game on the page
        if only_product is not None:    
            only_row = [year]
            only_row.extend(processGameDetailsMetacritic(only_product.text))
            csv_game_data.append(only_row)
            break
            
        first_product = soup.find("li", {"class": "product game_product first_product"})
        #extracts first game on the page
        if first_product is not None:
            first_row = [year]
            first_row.extend(processGameDetailsMetacritic(first_product.text))
            csv_game_data.append(first_row)
            
        all_products = soup.find_all("li", {"class": "product game_product"})
        #extracts all games on the page besides the first and last
        if all_products is not None:
            for product in all_products:
                new_row = [year]
                new_row.extend(processGameDetailsMetacritic(product.text))
                csv_game_data.append(new_row)
            
        last_product = soup.find("li", {"class": "product game_product last_product"})
        #extracts last game on the page
        if last_product is not None:
            last_row = [year]
            last_row.extend(processGameDetailsMetacritic(last_product.text))
            csv_game_data.append(last_row)
                   
        if int(last_page) == 0:
            print("Only one page!")
        page += 1
        print(page)
        
    year += 1
            
    
csvWriter("Metacritic Data Trial Run 2016 to 2019", csv_game_data)


