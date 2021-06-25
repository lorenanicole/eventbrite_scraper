import pathlib

from bs4 import BeautifulSoup
import requests

from models import Event

SCRIPT_DIR = pathlib.Path(__file__).parent.absolute()
EVENTBRITE_URL = 'https://www.eventbrite.com/d'


class EventbriteScraper:
    @classmethod
    def get_events(cls, state, city, category, number):
        page = requests.get(f'{EVENTBRITE_URL}/{state}--{city}/{category}')
        soup = BeautifulSoup(page.content, 'html.parser')

        event_elems = soup.find_all('article',
                                    class_='eds-l-pad-all-4 eds-event-card-content eds-event-card-content--list '
                                           'eds-event-card-content--standard eds-event-card-content--fixed')

        for val in range(1, int(number / 20)):
            page = requests.get(f'{EVENTBRITE_URL}/{category}/?page={val+1}')
            soup = BeautifulSoup(page.content, 'html.parser')

            event_elems += soup.find_all('article',
                                         class_='eds-l-pad-all-4 eds-event-card-content eds-event-card-content--list '
                                                'eds-event-card-content--standard eds-event-card-content--fixed')

        return list(map(lambda e: EventbriteScraper.create_event(e), event_elems))

    @classmethod
    def create_event(cls, event):
        url = event.find('a').attrs.get('href')
        title = event.find('h3').text

        event_page = requests.get(url)
        event_soup = BeautifulSoup(event_page.content, 'html.parser')

        event_details = event_soup.find('div', class_='event-details')
        event_details_data = event_details.findAll('div', class_='event-details__data')

        # date = event_details.find('p', class_='js-date-time-first-line').text
        # time = event_details.find('p', class_='js-date-time-second-line').text

        date_elem = event_details.find('time', class_='clrfix').findAll('p')
        date = date_elem[0].text
        time = date_elem[1].text

        address_elem = list(filter(lambda e: e.find('a', class_='js-view-map-link is-hidden'), event_details_data))[0]
        address_p = address_elem.findAll('p')
        venue = address_p[0].text
        street_address = address_p[1].text
        parts_address = address_p[2].text.strip(',').split(' ')
        city = parts_address[0]
        state = parts_address[1]
        zipcode = int(parts_address[2]) if parts_address[2].isnumeric() else -1

        if len(address_p[3]) >= 3:
            map_url = address_p[3].findAll('a')[1].attrs.get('href')
        else:
            map_url = ""

        price = event_soup.find('div', class_='js-display-price').text.strip('$')
        price = float(price) if price.isnumeric() else 0.0

        return Event(
            url=url, title=title, date=date, time=time, venue=venue, street_address=street_address,
            city=city, state=state, zipcode=zipcode, map_url=map_url, price=price
        )
