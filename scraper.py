from lxml import html
import requests
import scraperwiki
import time
import string
from dateutil.parser import parse

def scrape_events():
    page = requests.get('https://www.oakfordsocialclub.com/events')
    tree = html.fromstring(page.text)
    sections = tree.xpath('//div[@class="accordion--accordion"]/section')
    count = 0
    for section in sections:
        h1 = section.xpath('.//h1/text()')
        title = h1[0].split('- ',1)[0]
        date = h1[0].split('- ',1)[1]
        date = parse(date)
        date = date.strftime('%Y-%m-%d')
        event_time = section.xpath('.//div[@class="text--only"]/p[1]/text()')
        description = section.xpath('.//div[@class="text--only"]/p[2]/text()')
        count += 1
        
        data = {
            'id': count,
            'title': title,
            'date': date,
            'time': event_time[0],
            'description': description[0],
            'venue': 'Oakford Social Club',
            'location': 'Reading',
            }
        print data
        
        scraperwiki.sqlite.save(unique_keys = ['id'], data = data)
        time.sleep(0.5)
    
scrape_events()
