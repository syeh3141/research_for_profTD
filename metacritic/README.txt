# metacriticdata.py

Script for extracting data user and metascore ratings of
games from 1995-2019

## Packages needed

urllib.request
bs4 (BeautifulSoup) -> can be installed using pip install command
csv

## Usage

Script can be run in Python IDEs (was created on Spyder IDE)
csv files are saved into current working directory (prompted in Spyder)
May encounter HTTP Internal Server Error
Suggested: loop over smaller time periods

## Functions

Three defined functions
processGameDetailsMetacritic: string processing for splitting up game name, platform, metascore, user score, release date
csvWriter: writing the data to a csv file with file name and data as arguments
lastPageNumber: returns the number of the last page of a given year
numberOfReviews: returns list that includes the number of positive, mixed and negative reviews of both users and critics