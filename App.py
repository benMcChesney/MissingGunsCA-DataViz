#made by Ben McChesney 8/19/2017
#following original tutorial here: https://www.dataquest.io/blog/web-scraping-tutorial-python/

import requests
from bs4 import BeautifulSoup

page = requests.get("http://apps.mercurynews.com/policeguns/")
soup = BeautifulSoup(page.content, 'html.parser')

gunItems = soup.find_all( class_ = "itemdata" )
print( "there are " + str( len( gunItems ) ) + " tags matching itemdata")

it = 0
for item in gunItems:
    #extract the serial
    serialHeader = item.find( class_ = "serialno monosp")
    serial = item.find( 'strong' ).get_text()
    #print( "#" + str( it ) + " serial : " + str( serial ) )

    subgroups = item.find_all( 'div' , class_ = 'subgroup' )
    dateAndLocation = subgroups[0].find_all( 'span')
    date = dateAndLocation[0].get_text()
    location = dateAndLocation[1].get_text()
    #print( "#" + str( it ) + " date : " + date + " - location " + location )

    gunInfo = subgroups[1]
    gunFields = gunInfo.find_all( 'p' )
    type = gunFields[0].get_text()
    make = gunFields[1].get_text()
    model = gunFields[2].get_text()
    caliber = gunFields[3].get_text()
    #print( "#" + str( it ) + type + " | " + make  + " | " + model  + " | " + caliber )

    crimeInfo = subgroups[2].find_all( 'p' )

    #substring out the extra characters since these are formatted a little differently
    reported = crimeInfo[ len( crimeInfo ) - 2 ].get_text()[10:]
    vehicle = crimeInfo[ len( crimeInfo ) - 1 ].get_text()[14:]

    recovered = False
    if( len( crimeInfo ) > 2 ):
        recovered = True

    print( "#" + str( it ) +" : " + str( recovered ) + " | " + vehicle  + " | " + reported )

    #reported = crimeInfoo

    '''
    not recovered 
    <div class="subgroup">
        <p><strong>Reported</strong>: Stolen</p>
        <p><strong>From vehicle?</strong>: Yes</p>
    </div>
    
    recovered TAGS
    <div class="subgroup">
        <p class="recovered"><strong>RECOVERED</strong></p>
        <p><strong>Reported</strong>: Stolen</p>
        <p><strong>From vehicle?</strong>: Yes</p>
    </div>
    '''
    it += 1