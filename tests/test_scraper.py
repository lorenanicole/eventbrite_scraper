from pathlib import Path

import pytest

from scraper import EVENTBRITE_URL, EventbriteScraper


TEST_DIRECTORY = Path(__file__).parent.absolute()


@pytest.fixture
def mocked_requests(requests_mock):
    urls = [
        ['jazz_request', f'{EVENTBRITE_URL}/IL--Chicago/jazz'],
        ['event_1', 'https://www.eventbrite.com/e/friday-jazz-the-quarry-w-angel-bat-dawid-tickets-160584678095?aff=ebdssbdestsearch'],
        ['event_2', 'https://www.eventbrite.com/e/chicago-soul-jazz-collective-feat-dee-alexander-tickets-161006728459?aff=ebdssbdestsearch'],
        ['event_3', 'https://www.eventbrite.com/e/friday-night-jazz-schweikher-house-featuring-the-paul-wagner-quartet-tickets-159162879457?aff=ebdssbdestsearch'],
        ['event_4', 'https://www.eventbrite.com/e/the-courtyard-series-presents-maja-rios-jazz-beyond-tickets-157686228755?aff=ebdssbdestsearch'],
        ['event_5', 'https://www.eventbrite.com/e/a-evening-with-lush-life-jazz-at-green-street-grill-tickets-160855173153?aff=ebdssbdestsearch']
    ]

    for url in urls:
        content = None
        with open(f'{TEST_DIRECTORY}/fixtures/{url[0]}.html', 'r') as f:
            content = bytes(f.read(), 'utf-8')
        requests_mock.get(url[1], content=content)


def test_scrape_events(mocked_requests):
    events = EventbriteScraper.get_events('IL', 'Chicago', 'jazz', 5)

    urls = [
        'https://www.eventbrite.com/e/friday-jazz-the-quarry-w-angel-bat-dawid-tickets-160584678095?aff=ebdssbdestsearch',
        'https://www.eventbrite.com/e/chicago-soul-jazz-collective-feat-dee-alexander-tickets-161006728459?aff=ebdssbdestsearch',
        'https://www.eventbrite.com/e/friday-night-jazz-schweikher-house-featuring-the-paul-wagner-quartet-tickets-159162879457?aff=ebdssbdestsearch',
        'https://www.eventbrite.com/e/the-courtyard-series-presents-maja-rios-jazz-beyond-tickets-157686228755?aff=ebdssbdestsearch',
        'https://www.eventbrite.com/e/a-evening-with-lush-life-jazz-at-green-street-grill-tickets-160855173153?aff=ebdssbdestsearch'
    ]

    assert all(event.url in urls for event in events)
    assert len(events) == 5
