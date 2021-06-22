import argparse

import us

from db import DatabaseFactory
from scraper import EventbriteScraper


def validate_state(state):
    if state not in us.states.STATES:
        return argparse.ArgumentTypeError(f'Invalid state: {state}')

    return state


def validate_city(city):
    if len(city) < 1:
        return argparse.ArgumentTypeError(f'City cannot be empty')

    return city.replace(' ', '-')


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
    parser.add_argument(
        "-d",
        "--database",
        default="sqlite",
        type=str,
        choices=["sqlite", "mysql"],
        help="Select either a sqlite or mysql database, by default sqlite is used."
    )

    args = parser.parse_args()

    events = EventbriteScraper.get_events(args.state, args.city, args.category, args.number)
    event_tuples = list(map(lambda e: e.to_tuple(), events))

    table_schema =  """
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

    insert_events_query = """
                        INSERT INTO `events`
                            (`url`, `title`, `date`, `time`, `venue`, `street_address`, 
                            `city`, `state`, `zipcode`, `map_url`, `price`)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """

    db = DatabaseFactory.create_database(**{'database_exist': False, 'database': args.database,  'database_name': 'eventbrite_events'})
    db.create_tables([table_schema])
    db.insert(insert_events_query, event_tuples)

    counter = 1
    for event in events:
        print(f'{counter}. {event.title} on {event.date} {event.time}, event page: {event.url}')
        counter += 1
