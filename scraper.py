import argparse
import pathlib
import sqlite3
from dataclasses import dataclass

import requests
import us
from bs4 import BeautifulSoup


SCRIPT_DIR = pathlib.Path(__file__).parent.absolute()
EVENTBRITE_URL = 'https://www.eventbrite.com/d'


def validate_state(state):
    if state not in us.states.STATES:
        return argparse.ArgumentTypeError(f'Invalid state: {state}')

    return state


def validate_city(city):
    if len(city) < 1:
        return argparse.ArgumentTypeError(f'City cannot be empty')

    return city.replace(' ', '-')


@dataclass
class Event:
    url: str
    title: str
    date: str
    time: str
    venue: str
    street_address: str
    city: str
    state: str
    zipcode: int
    map_url: str
    price: float

    @classmethod
    def find_event_details(cls, event):
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

    def to_tuple(self):
        return (
            self.url, self.title, self.date, self.time, self.venue, self.street_address,
            self.city, self.state, self.zipcode, self.map_url, self.price
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Python calculator")
    parser.add_argument(
        "category",
        type=str,
        help="Select the type of events you'd like to find",
    )
    parser.add_argument(
        "city",
        type=validate_city,
        help="Select the city e.g. Chicago.",
    )
    parser.add_argument(
        "state",
        type=validate_state,
        help="Select the two letter state e.g. IL.",
    )
    parser.add_argument(
        "-n",
        "--number",
        default=20,
        type=int,
        help="Number of events you'd like to find, please specify in multiples of 20.",
    )

    args = parser.parse_args()

    page = requests.get(f'{EVENTBRITE_URL}/{args.state}--{args.city}/{args.category}')
    soup = BeautifulSoup(page.content, 'html.parser')

    event_elems = soup.find_all('article',
                                class_='eds-l-pad-all-4 eds-event-card-content eds-event-card-content--list '
                                       'eds-event-card-content--standard eds-event-card-content--fixed')

    for val in range(1,int(args.number / 20)):
        page = requests.get(f'{EVENTBRITE_URL}/{category}/?page={val+1}')
        soup = BeautifulSoup(page.content, 'html.parser')

        event_elems += soup.find_all('article',
                                    class_='eds-l-pad-all-4 eds-event-card-content eds-event-card-content--list '
                                           'eds-event-card-content--standard eds-event-card-content--fixed')

    events = list(map(lambda e: Event.find_event_details(e), event_elems))
    events_data = list(map(lambda e: e.to_tuple(), events))

    connection = sqlite3.connect(f"{SCRIPT_DIR}/events.db")
    cursor = connection.cursor()
    cursor.execute(
        """
        CREATE TABLE events
                 (
                    [id] INTEGER PRIMARY KEY,
                    [url] text,
                    [title] text,
                    [date] text,
                    [time] text,
                    [venue] text,
                    [street_address] text,
                    [city] text,
                    [state] text,
                    [zipcode] int,
                    [map_url] text,
                    [price] text
                 )
        """
    )

    connection.commit()

    insert_events_query = """
                INSERT INTO `events`
                    (`url`, `title`, `date`, `time`, `venue`, `street_address`, 
                    `city`, `state`, `zipcode`, `map_url`, `price`)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

    cursor.executemany(insert_events_query, events_data)
    connection.commit()

    counter = 1
    for event in events:
        print(f'{counter}. {event.title} on {event.date} {event.time}, event page: {event.url}')
        counter += 1
