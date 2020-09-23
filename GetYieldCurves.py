import requests
import xmltodict, re
from pandas.io.json import json_normalize

def main():
    #TODO: Make year dynamic
    year = '2020'

    # Grab URL from the internet
    url = 'https://www.treasury.gov/resource-center/data-chart-center/interest-rates/pages/XmlView.aspx?data=yieldYear&year=%s'%year
    page = getPageText(url)
    
    # Get dataframe with yield curves
    df = json_normalize(parseTreasuryXML(page))

    # output to CSV
    df.to_csv('P:/2020/083120/Scenarios/TreasuryCurves_2020.csv', index = False)

def getPageText(url):
    # intialize session
    session_requests = requests.session()

    # request the URL
    response = session_requests.get(url)

    return response.text

def parseTreasuryXML(s):
    # Dictionary to store yield for each date
    yields = dict()

    # List to store yields for all dates
    l = []

    # Parse xml page
    d = xmltodict.parse(s)

    # Loop through relevant data attributes
    for i in range(len(d["pre"]["entry"])):
        data = d["pre"]["entry"][i]["content"]["m:properties"]
        # Save each yield curve to a dictionary
        for key in data.keys():
            if 'date' in key.lower(): 
                date = re.search('([0-9]{4}-[0-9]{2}-[0-9]{2})', data[key]['#text'])[1]
                yields['Date'] = date
                yields['Curve'] = dict()
            elif 'bc' in key.lower() and not 'display' in key.lower():
                yields['Curve'][re.sub('d:BC_', '',key)] = data[key]['#text']
        
        # Add curve to list
        l.append(yields.copy())
          
    return l

if __name__=="__main__":
    main()