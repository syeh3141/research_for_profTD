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
        
def seriesListDictMaker(prefix, region_codes, item_codes):
    """This function takes in prefix (four letter code) and makes all possible
    combinations with the codes in region_codes and item_codes
    Outputs a tuple of the (list, dictionary)
    list -> list of series IDs
    dict -> Python dictionary mapping each series ID to list of two elements
    first element is the region code (four digit #) second element is the item suffix
    """
    series_list = []
    series_dict = {}
    
    #for code in region_codes:
        #for suffix in item_codes:
    for suffix in item_codes:
        for code in region_codes:
            series_dict[prefix + code + suffix] = [code, suffix]
            series_list.append(prefix + code + suffix)
    
    return series_list, series_dict
    
        
def blsDataPrice(start_year, end_year, seriesid_list, seriesid_dict, items, areas, file_name):
    """This function takes in 7 arguments: the starting year, ending year (both in string format)
    seriesid_list -> list of series IDs
    seriesid_dict -> Python dictionary mapping each series ID to list of two elements
    first element is the region code (four digit #) second element is the item suffix
    items -> Python dictionary mapping each item suffix to the name of item
    areas -> Python dictionary mapping each area code to the area name
    Outputs csv file in current working directory with file_name
    Note: file_name does not need file extension .csv
    Note: seriesid_list listed item code then area code as such:   
    CUUR0100SAR  CUUR0200SAR  CUUR0100SARC  CUUR0200SARC
    NOT CUUR0100SAR  CUUR0100SARC  CUUR0200SAR  CUUR0200SARC
    """
    csv_cu_data = [['Year','Month','Region']]
    
    
    for i in range(0,len(seriesid_list)):
        year = int(end_year)
        while year >= int(start_year):
            startyear = year - 9
            if startyear < int(start_year):
                startyear = start_year
            headers = {'Content-type': 'application/json'}  
            data = json.dumps({"seriesid": [seriesid_list[i]],"startyear":str(startyear), "endyear":str(year)})
            p = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)
            json_data = json.loads(p.text)
            series = json_data['Results']['series'][0]
            seriesID = series['seriesID']
            print(seriesID)
            series_item = items[seriesid_dict[seriesID][1]]
            num_column_titles = len(csv_cu_data[0])
            index_row_no_col = 0
            #first row that is not full column
            while index_row_no_col <= len(csv_cu_data) - 1:
                if len(csv_cu_data[index_row_no_col]) < num_column_titles:
                    #print(index_row_no_col)
                    #print(csv_cu_data[index_row_no_col])
                    #print("Length of last row no full column: " + str(len(csv_cu_data[index_row_no_col])))
                    #print("Number of Columns: " +str(num_column_titles))
                    break
                index_row_no_col += 1
            #print(csv_cu_data[index_row_no_col-1])
            new_column = True   
            for item in csv_cu_data[0]:
                #checking to see if a new item column is needed
                if series_item == item:
                    new_column = False
                    break
        
            if new_column and seriesID == seriesid_list[0]:
                print(1)
                #first series and creating a new column
                csv_cu_data[0].append(series_item)
                for item in series['data']:
                    area = areas[seriesid_dict[seriesID][0]]
                    row = [item['year'],item['periodName'],area, item['value']]
                    period = item['period']
                    if 'M01' <= period <= 'M12':
                        csv_cu_data.append(row)
        
            elif new_column:
                #other series that create a new column aka have a unique item column
                csv_cu_data[0].append(series_item)
                row_count = 1
                for item in series['data']:
                    area = areas[seriesid_dict[seriesID][0]]
                    if csv_cu_data[row_count][0] == item['year'] and csv_cu_data[row_count][1] == item['periodName'] and csv_cu_data[row_count][2] == area:
                        #check for the right year, month and area row
                        csv_cu_data[row_count].append(item['value'])
                    row_count += 1
        
            elif not new_column and series_item == csv_cu_data[0][3]:
                print(3)
                    #check for right column
                for item in series['data']:
                    area = areas[seriesid_dict[seriesID][0]]
                    row = [item['year'],item['periodName'],area, item['value']]
                    period = item['period']
                    if 'M01' <= period <= 'M12':
                        csv_cu_data.append(row)
            
            else:
                print(4)
                if series_item == csv_cu_data[0][len(csv_cu_data[index_row_no_col-1])-1]:
                    #check for right column
                    row_count = index_row_no_col
                    for item in series['data']:
                        area = areas[seriesid_dict[seriesID][0]]
                        if csv_cu_data[row_count][0] == item['year'] and csv_cu_data[row_count][1] == item['periodName'] and csv_cu_data[row_count][2] == area:
                            #check for the right year, month and area row
                            csv_cu_data[row_count].append(item['value'])
                        row_count += 1
                else:
                    print(seriesID + " Column mismatch error")
                    raise NameError('Check for right column!')
            
        
            year -= 10
       
    csvWriter(file_name, csv_cu_data)
        
                
     
current_region_codes = {'0100':"Northeast",'0200':"Midwest",'0300':"South",'0400':"West"}
cu_series_SAR = {"SAR":"Recreation"}
cu_currentseries_otheritems = {"SARC": "Recreation commodities", "SARS": "Recreation services"}

division_codes = {'0110':"New England", "0120": "Middle Atlantic","0230":"East North Central",
                  "0240":"West North Central","0350":"South Atlantic","0360":"East South Central",
                  "0370":"West South Central","0480":"Mountain", "0490":"Pacific"}
#Division code series ID use only the SAR item suffix
old_region_codes = {'0100':"Northeast Region",'0200':"North Central Region",'0300':"Southern Region",'0400':"Western Region"}
cu_oldseries_items = {"SA6":"Entertainment","SA61":"Entertainment commodities",
                      "SE62":"Entertainment services"}


csv_cu_data = [['Year','Month']]

#Creating series ID tupel of list and dictionary
region_current_series_SAR = seriesListDictMaker("CUUR", current_region_codes, cu_series_SAR)
region_current_series_other = seriesListDictMaker("CUUR", current_region_codes, cu_currentseries_otheritems)
division_current_series = seriesListDictMaker("CUUR", division_codes, cu_series_SAR)
region_old_series = seriesListDictMaker("MUUR", old_region_codes, cu_oldseries_items)


        
#blsDataPrice("1997", "2019", region_current_series_SAR[0], region_current_series_SAR[1], cu_series_SAR, current_region_codes,"Region Current SAR PriceLevel")
#blsDataPrice("2009", "2019", region_current_series_other[0], region_current_series_other[1], cu_currentseries_otheritems, current_region_codes,"Region Current OtherRecreation PriceLevel")
#blsDataPrice("2017", "2019", division_current_series[0], division_current_series[1], cu_series_SAR, division_codes,"Division Current PriceLevel")
blsDataPrice("1977", "1997", region_old_series[0], region_old_series[1], cu_oldseries_items, old_region_codes,"Region Old PriceLevel")



