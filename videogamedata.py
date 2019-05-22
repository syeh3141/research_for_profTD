# -*- coding: utf-8 -*-
"""
Created on Sun May 19 18:35:41 2019

@author: syeh3
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv


def processGameName(game):
    """This function takes in a string argument in the form
    'game name (game system)game maker, game type'
    Returns a list
    1st element -> game name
    2nd element -> game system
    3rd element -> game maker
    4th element -> game type
    Preconditions: game must have at least 1 set of parenthese and 1 comma
    """
    
    if game.count("(") == 0  or game.count(")") == 0 or game.count(",") == 0:
        #Checking preconditions
        print('Invalid game name string')
        return 
    
    name = game[: game.find('(') - 1]
    system = game[game.rfind('(') + 1: game.rfind(')')]
    maker = game[game.rfind(')') + 1: game.rfind(',')]
    game_type = game[game.rfind(',') + 2:]
    #String splicing
    
    return [name, system, maker, game_type]


def csvWriter(file_name, data):
    """This function takes in a string argument for file name and list data
    for data to be written to a new csv file
    Note: overwrites files of the same name
    """
    with open(file_name + '.csv', 'w', newline ='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(data)



#Script start
#To run only one instance, comment out the while loop
option = 43464
#Starting HTML url for week of December 29th 2018

while option >= 39971:

    url = "http://www.vgchartz.com/weekly/" + str(option) + "/USA/"
    html = urlopen(url)
    soup = BeautifulSoup(html, 'lxml')
    
    date = soup.find("option", {"selected": True})
    #date element found under option selected in <div class="chart_date_selector"
    
    table = soup.find("table", {"class": "chart"})
    table_rows = table.find_all('tr')

    cell_count = 1
    csv_game_data = [[date.text],['Position','Game','Game System','Maker','Game Type','Weekly Sales','Total Sales','Week #']]
    #csv list to be written out into csv file with column headings

    while cell_count <= 60:
        td_data = table_rows[cell_count].find_all('td')
        #Beautifulsoup Resultset element of all content in each table row
        original_row = [i.text for i in td_data] 
        #Creates list with each element an element from td_data object
        
        position = int(original_row[0])
        weekly_sales = int(original_row[4].replace(',',''))
        total_sales = int(original_row[5].replace(',',''))
        week_number = int(original_row[6].replace(',',''))
        #replace function used to cast strings to int without worry of comma's
        game_attributes = processGameName(original_row[3])
        #Function call to processGameName
    
        new_row = []
        new_row.append(position)
        new_row.extend(game_attributes)
        new_row.append(weekly_sales)
        new_row.append(total_sales)
        new_row.append(week_number)
        csv_game_data.append(new_row)
        cell_count += 2
        #Each new game cell skips the next cell
        #30 games for 60 cells in total

   
    csvWriter(date.text, csv_game_data)
    #Function call to csvWriter
    print(date.text)
    
    option -= 350
    #Each HTML url decrements by 7 for a new week