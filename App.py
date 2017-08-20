#made by Ben McChesney 8/19/2017
#based on this https://www.dataquest.io/blog/web-scraping-tutorial-python/

import requests
from bs4 import BeautifulSoup
import pandas as pd

page = requests.get("http://apps.mercurynews.com/policeguns/")
soup = BeautifulSoup(page.content, 'html.parser')

gunItems = soup.find_all( class_ = "itemdata" )
print( "there are " + str( len( gunItems ) ) + " tags matching itemdata")

serials = list()
dates = list()
locations = list()
types = list()
makes = list()
models = list()
calibers = list()
reportedStatuses = list()
vehicles = list()
recoveredStatuses = list()

it = 0
for item in gunItems:
    #extract the serial
    serialHeader = item.find( class_ = "serialno monosp")
    serials.append( item.find( 'strong' ).get_text() )

    subgroups = item.find_all( 'div' , class_ = 'subgroup' )
    dateAndLocation = subgroups[0].find_all( 'span')
    dates.append( dateAndLocation[0].get_text() )
    locations.append( dateAndLocation[1].get_text() )
    #print( "#" + str( it ) + " date : " + date + " - location " + location )

    gunInfo = subgroups[1]
    gunFields = gunInfo.find_all( 'p' )
    types.append( gunFields[0].get_text()[6:] )
    makes.append( gunFields[1].get_text()[6:] )
    models.append( gunFields[2].get_text()[7:] )
    calibers.append( gunFields[3].get_text()[9:] )
    #print( "#" + str( it ) + type + " | " + make  + " | " + model  + " | " + caliber )

    crimeInfo = subgroups[2].find_all( 'p' )

    #substring out the extra characters since these are formatted a little differently
    reportedStatuses.append( crimeInfo[ len( crimeInfo ) - 2 ].get_text()[10:] )
    vehicles.append( crimeInfo[ len( crimeInfo ) - 1 ].get_text()[14:] )

    recovered = False
    if( len( crimeInfo ) > 2 ):
        recovered = True

    recoveredStatuses.append( recovered )
    it += 1

print( "end of loop")
dataFrame = pd.DataFrame({
    "serial":serials,
    "date":dates,
    "location":locations,
    "gun-type":types,
    "gun-make":makes,
    "gun-models":models,
    "gun-calibers":calibers,
    "from-vehicle":vehicles,
    "reported":reportedStatuses,
    "recovered":recoveredStatuses
})

print( dataFrame.head( 5 ))

# source : https://stackoverflow.com/questions/39257147/convert-pandas-dataframe-to-json-format
out = dataFrame.to_json( orient='records', lines=False ).replace('} {', '},{' )
with open( 'export.json' , 'w' ) as f:
    f.write( out )
