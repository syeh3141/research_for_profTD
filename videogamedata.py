# -*- coding: utf-8 -*-
"""
Created on Sun May 19 18:35:41 2019

@author: syeh3
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv  
    

def processGameName(game, result_set):
    """This function takes in a string argument in the form
    'game name (game system)game maker, game type'
    Returns a list
    1st element -> game name
    2nd element -> game system
    3rd element -> game maker
    4th element -> game type
    Preconditions: game must have at least 1 set of parenthese and 1 comma
    """
    blank = False
    
    if game.count("(") == 0  or game.count(")") == 0 or game.count(",") == 0:
        #Checking preconditions
        print('Invalid game name string')
        return 
    
    name = game[: game.find('(') - 1]
    system = game[game.rfind('(') + 1: game.rfind(')')]
    maker = game[game.rfind(')') + 1: game.rfind(',')]
    game_type = game[game.rfind(',') + 2:]
    #String splicing
    
    if not name:
        #if name is blank, get name from picture reference
        reference_td = result_set[1]
        picture_ref = reference_td.a['href']
        raw_title = picture_ref[picture_ref.rfind('/') + 1:]
        raw_title = raw_title.replace('-', ' ')
        name = raw_title.title()
        if name == "Walkthrough":
            #if name is 'Walkthrough', get name from ssecond slash set
            raw_title_nowalk = picture_ref[:picture_ref.rfind('/')]
            raw_title_nowalk = raw_title_nowalk[raw_title_nowalk.rfind('/') + 1:]
            raw_title_nowalk = raw_title_nowalk.replace('-', ' ')
            name = raw_title_nowalk.title()
        print(name)
        blank = True
    
    
    return [name, system, maker, game_type, blank]


def csvWriter(file_name, data):
    """This function takes in a string argument for file name and list data
    for data to be written to a new csv file
    Note: overwrites files of the same name
    """
    with open(file_name + '.csv', 'w', newline ='', encoding='utf-8') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(data)

        
#Script start
#To run only one instance, comment out the while loop
option = 43464
#Starting HTML url for week of December 29th 2018

csv_game_data = [['Date','Position','Game','Game System','Maker','Game Type','Weekly Sales','Total Sales','Week #']]
#csv list to be written out into csv file with column headings
csv_blanks = [['Date','Game Name']]
#csv list of blanked names that were revised    
    
while option >= 38319:
#Ending HTML url for week of November 27th 2004
    

    url = "http://www.vgchartz.com/weekly/" + str(option) + "/USA/"
    html = urlopen(url)
    soup = BeautifulSoup(html, 'lxml')
    
    date = soup.find("option", {"selected": True})
    #date element found under option selected in <div class="chart_date_selector"
    
    table = soup.find("table", {"class": "chart"})
    table_rows = table.find_all('tr')
    cell_count = 1
    
    while cell_count <= 60:
        try:
            td_data = table_rows[cell_count].find_all('td')
            #Beautifulsoup Resultset element of all content in each table row
            
        except(IndexError):
            print("Less than 30 game cells for week: " + date.text)
            #If IndexError, then break out of table grabbing data for this week
            #Some of the later data i.e. year 2004 only has data for less than 30 games
            break
                
        original_row = [i.text for i in td_data] 
        #Creates list with each element an element from td_data object
        
        position = original_row[0]
        weekly_sales = original_row[4].replace(',','')
        total_sales = original_row[5].replace(',','')
        week_number = original_row[6].replace(',','')
        game_attributes = processGameName(original_row[3], td_data)
        if game_attributes[4]:
            #To create a new csv file to check correctness of correcting blanks
            print("Blank!")
            blanks_row = []
            blanks_row.append(date.text)
            blanks_row.append(position)
            blanks_row.append(game_attributes[0])
            csv_blanks.append(blanks_row)
        
        #Function call to processGameName
            
        new_row = []
        new_row.append(date.text)
        new_row.append(position)
        new_row.extend(game_attributes[:3])
        new_row.append(weekly_sales)
        new_row.append(total_sales)
        new_row.append(week_number)
        csv_game_data.append(new_row)
        cell_count += 2
        #Each new game cell skips the next cell
        #30 games for 60 cells in total
            
    print(date.text)
            
    option -= 7
    #Each HTML url decrements by 7 for a new week

csvWriter("Game Sales Data", csv_game_data)
csvWriter("Blanks", csv_blanks)
#Function call to csvWriter
