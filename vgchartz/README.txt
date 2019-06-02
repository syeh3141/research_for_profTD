# vgchartzdata.py

Script for extracting data of top 30 weekly selling video games
and stored into csv files

## Packages needed

urllib.request
bs4 (BeautifulSoup) -> can be installed using pip install command
csv

## Usage

Script can be run in Python IDEs (was created on Spyder IDE)
csv files are saved into current working directory (prompted in Spyder)

## Functions

Two defined functions
processGameName: string processing for splitting up game name, system, maker and type
csvWriter: writing the data to a csv file with file name and data as arguments