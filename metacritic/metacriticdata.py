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
      
        
def numberOfReviews(game):
    """This function takes in a game BeatifulSoup Tag (from the MetaCritic yearly
    chart) and goes to specific game's MetaCritic website 
    Returns list as follows
    1st element -> number of total critic reviews
    2nd element -> number of positive critic reviews
    3rd element -> number of mixed critic reviews
    4th element -> number of negative critic reviews
    5th element -> number of total user reviews
    6th element -> number of positive user reviews
    7th element -> number of mixed user reviews
    8th element -> number of negative user reviews
    If no user rating aka "tbd", then the number of total user ratings
    comes from taking four minus the number needed to get to the valid number
    of ratings (4)
    """
    ending_url = game.a['href']
    full_url = "https://www.metacritic.com" + ending_url

    for i in range(0,10):
        if i == 9:
            return ["SERVER FAIL"]
        try:
            ratings_url_headers = urllib.request.Request(full_url, headers={'User-Agent' : "Magic Browser"})
            html_ratings = urllib.request.urlopen(ratings_url_headers)
            soup_ratings = BeautifulSoup(html_ratings, 'lxml')
            #soup the website of the specific game on MetaCritic
        except urllib.error.HTTPError as error:
            error_codes = [404, 500, 502, 503, 504]
            if error.code in error_codes and i == 0:
                httpErrorGames.append(ending_url)
                continue
            elif error.code in error_codes:
                continue
            else:
                 raise
        break
    #Try for server failures or page not found 404 errors
    
    all_reviews = []
    
    main_details = soup_ratings.find("div", {"class": "details main_details"})
    critic_count = main_details.find("span", {"class": "count"})
    critic_text = critic_count.text
    number_of_critic_ratings = [int(s) for s in critic_text.split() if s.isdigit()]
    #Obtain number of critic ratings
    
    critic_reviews = []
    critic_reviews_soup = soup_ratings.find("div", {"class": "module reviews_module critic_reviews_module"})
    critic_reviews_count = critic_reviews_soup.find("ol", {"class":"score_counts hover_none"})
    for review in critic_reviews_count.find_all("li",{"class":"score_count"}):
        review = review.text.replace('\n','')
        review = int(review[review.find(":")+1:review.rfind('u')-2].strip())
        critic_reviews.append(review)
    #Obtain score breakdown of the critic reviews into [# of positive, # of mixed, # of negative]
    
    all_reviews.extend(number_of_critic_ratings)
    all_reviews.extend(critic_reviews)
    assert all_reviews[0] >= all_reviews[1] + all_reviews[2] + all_reviews[3]
    #Assert number of critic ratings >= all critic reviews added up 
    
    side_details = soup_ratings.find("div", {"class": "details side_details"})
    user_desc = side_details.find("span", {"class": "desc"}).text
    user_count = side_details.find("span", {"class": "count"})
    user_text = user_count.text
    if user_desc == 'No user score yet':
        number_of_user_ratings = [4-int(s) for s in user_text.split() if s.isdigit()]
        if not number_of_user_ratings:
            number_of_user_ratings = [0]
    else:
        number_of_user_ratings = [int(s) for s in user_text.split() if s.isdigit()]
        #string splicing
    #Obtain number of user ratings
    #With a rating of 'tbd' refer to Metacritic FAQ
    #https://www.metacritic.com/faq#item13 stating that need at least 4 user
    #ratings for there to be an actual number
    
    user_reviews = []
    user_reviews_soup = soup_ratings.find("div", {"class": "module reviews_module user_reviews_module"})
    user_reviews_count = user_reviews_soup.find("ol", {"class":"score_counts hover_none"})
    if user_reviews_count:
        for review in user_reviews_count.find_all("li",{"class":"score_count"}):
            review = review.text.replace('\n','')
            review = int(review[review.find(":")+1:review.rfind('u')-2].strip().replace(',',''))
            user_reviews.append(review)
    else:
        #CONDITON: no user reviews exist
        user_reviews = [0,0,0]
    #Obtain score breakdown of the user reviews into [# of positive, # of mixed, # of negative]
        
    all_reviews.extend(number_of_user_ratings)
    all_reviews.extend(user_reviews)
    assert all_reviews[4] >= all_reviews[5] + all_reviews[6] + all_reviews[7]
    #Assert number of user ratings >= all user reviews added up 
    print(all_reviews)
    return all_reviews


#script start
httpErrorGames = []
httpErrorPages = []

csv_game_data = [['Year','Game','Platform','Metascore','User Score','Release Date', 
                  'Total Number of Critic Ratings', 'Positive Critic Reviews', 
                  'Mixed Critic Reviews', 'Negative Critic Reviews',
                  'Total Number of User Ratings', 'Positive User Reviews', 
                  'Mixed User Reviews', 'Negative User Reviews']]
#csv list to be written out into csv file with column headings

year = 2001
#starting year

while year <= 2003:
#ending year
    
    page = 0
    last_page = lastPageNumber(year)
    
    while (page < int(last_page)) or (page == 0 and int(last_page) == 0):
        #CONDITION: page less than last_page or currently on the only page for the year
        print(page)
        print(last_page)
        for i in range(0,10):
            try:
                url = "https://www.metacritic.com/browse/games/score/metascore/year/all/filtered?sort=desc&year_selected=" + str(year) +"&page=" + str(page)
                url_headers = urllib.request.Request(url, headers={'User-Agent' : "Magic Browser"})
                html = urllib.request.urlopen(url_headers)
                soup = BeautifulSoup(html, 'lxml')
            except urllib.error.HTTPError as error:
                error_codes = [404, 500, 502, 503, 504]
                if error.code in error_codes and i == 0:
                    httpErrorPages.append(year)
                    httpErrorPages.append(page)
                    continue
                elif error.code in error_codes:
                    continue
                else:
                    raise
            break
        #Try for server failures or page not found 404 errors
        
        only_product = soup.find("li", {"class": "product game_product first_product last_product"})
        #first, last and only game on the page
        if only_product is not None:    
            only_row = [year]
            only_row.extend(processGameDetailsMetacritic(only_product.text))
            only_row.extend(numberOfReviews(only_product))
            csv_game_data.append(only_row)
            break
            
        first_product = soup.find("li", {"class": "product game_product first_product"})
        #first game on the page
        if first_product is not None:
            first_row = [year]
            first_row.extend(processGameDetailsMetacritic(first_product.text))
            first_row.extend(numberOfReviews(first_product))
            csv_game_data.append(first_row)
            
        all_products = soup.find_all("li", {"class": "product game_product"})
        #all games on the page besides the first and last
        if all_products is not None:
            for product in all_products:
                new_row = [year]
                new_row.extend(processGameDetailsMetacritic(product.text))
                new_row.extend(numberOfReviews(product))
                csv_game_data.append(new_row)
            
        last_product = soup.find("li", {"class": "product game_product last_product"})
        #last game on the page
        if last_product is not None:
            last_row = [year]
            last_row.extend(processGameDetailsMetacritic(last_product.text))
            last_row.extend(numberOfReviews(last_product))
            csv_game_data.append(last_row)
                   
        if int(last_page) == 0:
            print("Only one page!")
        page += 1
        print(page)
        
    year += 1
            
csvWriter("Metacritic Data with Reviews 2001 to 2003", csv_game_data)
    
print(httpErrorGames)
print(httpErrorPages)