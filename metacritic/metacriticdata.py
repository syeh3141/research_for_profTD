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
    Preconditions: game must have at least 1 set of parentheses and 1 colon
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
    #String splicing to obtain specific data
    
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
    Returns "0" if no last page
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
    
    
def numberOfUserRatings(game):
    """This function takes in a game BeatifulSoup Tag (from the MetaCritic year
    chart), goes to specific game's MetaCritic website and returns number of
    user ratings in a string"""
    
    ending_url = game.a['href']
    full_url = "https://www.metacritic.com" + ending_url
    try:
        for i in range(0,10):
            try:
                user_ratings_url_headers = urllib.request.Request(full_url, headers={'User-Agent' : "Magic Browser"})
                html_user_ratings = urllib.request.urlopen(user_ratings_url_headers)
                soup_user_ratings = BeautifulSoup(html_user_ratings, 'lxml')
            except:
                httpErrorGames.append(ending_url)
                continue
            break
        #Try for server failures
        #soup the website of the specific game on MetaCritic
    
        side_details = soup_user_ratings.find("div", {"class": "details side_details"})
        count = side_details.find("span", {"class": "count"})
        text = count.text
        number_of_user_ratings = text[text.find('n')+2:text.rfind('R')-1]
        #string splicing
    
        return number_of_user_ratings
    
    except:
        return "SERVER FAIL"


httpErrorGames = []
httpErrorPages = []

csv_game_data = [['Year','Game','Platform','Metascore','User Score','Release Date', 'Number of User Ratings']]
#csv list to be written out into csv file with column headings

year = 1995
#starting year

try:
    while year <= 2019:
    #ending year
    
        page = 0
        last_page = lastPageNumber(year)
    
        while (page < int(last_page)) or (page == 0 and int(last_page) == 0):
            print(page)
            print(last_page)
            
            for i in range(0,10):
                
                try:
                    url = "https://www.metacritic.com/browse/games/score/metascore/year/all/filtered?sort=desc&year_selected=" + str(year) +"&page=" + str(page)
                    url_headers = urllib.request.Request(url, headers={'User-Agent' : "Magic Browser"})
                    html = urllib.request.urlopen(url_headers)
                    soup = BeautifulSoup(html, 'lxml')
                except:
                    httpErrorPages.append(year)
                    httpErrorPages.append(page)
                    continue
                break
                #Try for server failures
        
            only_product = soup.find("li", {"class": "product game_product first_product last_product"})
            #first, last and only game on the page
            if only_product is not None:    
                only_row = [year]
                only_row.extend(processGameDetailsMetacritic(only_product.text))
                if only_row[4] != "tbd":
                    only_row.append(numberOfUserRatings(only_product))
                else:
                    only_row.append(0)
                csv_game_data.append(only_row)
                break
            
            first_product = soup.find("li", {"class": "product game_product first_product"})
            #first game on the page
            if first_product is not None:
                first_row = [year]
                first_row.extend(processGameDetailsMetacritic(first_product.text))
                if first_row[4] != "tbd":
                    first_row.append(numberOfUserRatings(first_product))
                else:
                    first_row.append(0)
                csv_game_data.append(first_row)
            
            all_products = soup.find_all("li", {"class": "product game_product"})
            #all games on the page besides the first and last
            if all_products is not None:
                for product in all_products:
                    new_row = [year]
                    new_row.extend(processGameDetailsMetacritic(product.text))
                    if new_row[4] != "tbd":
                        new_row.append(numberOfUserRatings(product))
                    else:
                        new_row.append(0)
                    csv_game_data.append(new_row)
            
            last_product = soup.find("li", {"class": "product game_product last_product"})
            #last game on the page
            if last_product is not None:
                last_row = [year]
                last_row.extend(processGameDetailsMetacritic(last_product.text))
                if last_row[4] != "tbd":
                    last_row.append(numberOfUserRatings(last_product))
                else:
                    last_row.append(0)
                csv_game_data.append(last_row)
                   
            if int(last_page) == 0:
                print("Only one page!")
            page += 1
            print(page)
        
        year += 1
            
    csvWriter("Metacritic Data Trial Run with User Ratings", csv_game_data)
        
except:
    csvWriter("Metacritic Data Trial Run with User Ratings", csv_game_data)
    
print(httpErrorGames)
print(httpErrorPages)