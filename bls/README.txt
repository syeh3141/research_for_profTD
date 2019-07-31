# blsdata_price.py

Script for extracting price level data from the Bureau of Labor Statistics
broken down by recreation item, region/division for various year ranges
Outputs three different files
All with a year column, month column, region/division column and 
item column for each column

User input needed- csv output file name, starting and ending year
registration key
The three function calls at the end of the script are for:
Recreation by Region
Recreaion Commodities and Recreation Services by Region
Recreation by Division
The commented-out function call: Historical Recreation data

## Packages needed

requests
json
csv

## Usage

Script can be run in Python IDEs (was created on Spyder IDE)
csv files are saved into current working directory (prompted in Spyder)
May encounter query limit (500 queries daily for registered API Ver. 2.0 BLS account)

## Functions

Three defined functions
csvWriter: writing the data to a csv file with file name and data as arguments

seriesListDictMaker: takes in prefix (four letter code) and makes all possible
series id combinations with the region codes and item codes put in as parameters
Parameters: prefix- four letter string
region_codes- list of region codes
item_codes- list of item codes
Outputs a tuple (list, dictionary)
list- list of series id
dict- dictionary of series id mapping to two elements
first element is the region code (four digit #), second element is the item suffix

blsDataPrice: This function takes BLS price data with registration key and outputs
a csv file with a year column, month column, region/division column and 
item column for each column
Parameters: the starting year (string format)
ending year (string format)
seriesid_list- list of series IDs
seriesid_dict - Python dictionary mapping each series ID to list of two elements
    first element is the region code (four digit #) second element is the item suffix
items - Python dictionary mapping each item suffix to the name of item
areas - Python dictionary mapping each area code to the area name
regis_key - API V 2.0 Registration Key
Outputs csv file in current working directory with file_name
Note: file_name does not need file extension .csv
Note: seriesid_list listed item code then area code as such:   
    CUUR0100SAR  CUUR0200SAR  CUUR0100SARC  CUUR0200SARC
NOT CUUR0100SAR  CUUR0100SARC  CUUR0200SAR  CUUR0200SARC
