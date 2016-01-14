from lxml import html
import requests
import scraperwiki
import time
import string
from dateutil.parser import parse
from datetime import date

def scrape_events():
    page = requests.get('https://www.oakfordsocialclub.com/events')
    tree = html.fromstring(page.text)
    sections = tree.xpath('//div[@class="accordion--accordion"]/section')
    for section in sections:
        h1 = section.xpath('.//h1/text()')
        title = h1[0].split('- ',1)[0]
        event_date = h1[0].split('- ',1)[1]
        event_date = parse(event_date)
        id = event_date.strftime('%Y%m%d')
        event_date = event_date.strftime('%Y-%m-%d')
        event_time = section.xpath('.//div[@class="text--only"]/p[1]/text()')
        description = section.xpath('.//div[@class="text--only"]/p[2]/text()')
        
        data = {
            'id': 'oak' + str(id),
            'title': title,
            'date': event_date,
            'time': event_time[0],
            'description': description[0],
            'venue': 'Oakford Social Club',
            'location': 'Reading',
            }
        print data
        
        scraperwiki.sqlite.save(unique_keys = ['id'], data = data)
        time.sleep(0.5)
    
if scraperwiki.sql.show_tables():
    scraperwiki.sqlite.execute("DELETE FROM data") #use 'swdata' on Mac, use 'data' on morph.io

scrape_events()
