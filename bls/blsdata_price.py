# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 19:20:32 2019

@author: syeh3
"""

import requests
import json
import csv 


def csvWriter(file_name, data):
    """This function takes in a string argument for file name and list data
    for data to be written to a new csv file
    Note: overwrites files of the same name
    """
    with open(file_name + '.csv', 'w', newline ='', encoding='utf-8') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(data)
        
def blsDataPrice(start_year, end_year, seriesid_list, seriesid_dict, items, areas, file_name):
    """This function takes in 7 arguments: the starting year, ending year (both in string format)
    seriesid_list -> list of series IDs
    seriesid_dict -> Python dictionary mapping each series ID to list of two elements
    first element is the region code (four digit #) second element is the item suffix
    items -> Python dictionary mapping each item suffix to the name of item
    areas -> Python dictionary mapping each area code to the area name
    Outputs csv file in current working directory with file_name
    Note: file_name does not need file extension .csv
    """
    csv_cu_data = [['Year','Month','Region']]
    headers = {'Content-type': 'application/json'}  
    data = json.dumps({"seriesid": seriesid_list,"startyear":start_year, "endyear":end_year})
    p = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)
    json_data = json.loads(p.text)
    for series in json_data['Results']['series']:
        print(series['seriesID'])
        if series == json_data['Results']['series'][0]:
        #First series, add the year, month, column heading and value
            seriesID = series['seriesID']
            csv_cu_data[0].append(items[seriesid_dict[seriesID][1]] + " " + areas[seriesid_dict[seriesID][0]])
            for item in series['data']:
                row = [item['year'],item['periodName'],item['value']]
                period = item['period']
                if 'M01' <= period <= 'M12':
                    csv_cu_data.append(row)
        else:
        #Every series besides first, add column heading and value
            seriesID = series['seriesID']
            csv_cu_data[0].append(items[seriesid_dict[seriesID][1]] + " " + areas[seriesid_dict[seriesID][0]])
            row_count = 1
            #Checking the right year and month row
            for item in series['data']:
                if csv_cu_data[row_count][0] == item['year'] and csv_cu_data[row_count][1] == item['periodName']:
                    csv_cu_data[row_count].append(item['value'])
                row_count += 1

    csvWriter(file_name, csv_cu_data)
        
#begin script        
region_codes = {'0100':"Northeast",'0200':"Midwest",'0300':"South",'0400':"West"}
cu_currentseries_items = {"SAR":"Recreation", "SARC": "Recreation commodities", 
                          "SARS": "Recreation services"}
cu_oldseries_items = {"SA6":"Entertainment","SA61":"Entertainment commodities",
                      "SE62":"Entertainment services"}
csv_cu_data = [['Year','Month']]
division_codes = {'0110':"New England", "0120": "Middle Atlantic","0230":"East North Central",
                  "0240":"West North Central","0350":"South Atlantic","0360":"East South Central",
                  "0370":"West South Central","0480":"Mountain", "0490":"Pacific"}
#Division code series ID use only the SAR item suffix



#Creating series ID list and dictionary (for ease in naming the columns)
seriesidlist = []
seriesiddict = {}
for area_code in region_codes:
    for suffix in cu_currentseries_items:
        seriesiddict["CUUR" + area_code + suffix] = [area_code, suffix]
        seriesidlist.append("CUUR" + area_code + suffix)
        
blsDataPrice("2011", "2014", seriesidlist, seriesiddict, cu_currentseries_items, region_codes,"test_5")
