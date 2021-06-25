# Eventbrite Scraper

A Python 3+ scraper that pulls USA event data from Eventbrite. The data is persisted to a sqlite3 or MySQL database as well as outputs the found events to stdout.

### Installation

1. Clone the repository
2. `pip install -r requirements.txt` (Note: There is a `pyproject.toml` provided, but this is a quicker way to get up and started!)

### Usage

To use, you will need to specify a category, a city, and a two letter USA state abbreviation. 

For example: `python scraper.py jazz chicago il`.

Example:

```
$ python scraper.py jazz chicago il
1. Friday Jazz @ The Quarry w/ Bethany PickensFriday Jazz @ The Quarry w/ Bethany Pickens on Fri, June 18, 2021 7:00 PM – 9:00 PM CDT, event page: https://www.eventbrite.com/e/friday-jazz-the-quarry-w-bethany-pickens-tickets-157522511071?aff=ebdssbdestsearch
2. Fathers Day Smooth Jazz BrunchFathers Day Smooth Jazz Brunch on Sun, June 20, 2021 12:00 PM – 5:30 PM CDT, event page: https://www.eventbrite.com/e/fathers-day-smooth-jazz-brunch-tickets-156624723765?aff=ebdssbdestsearch
3. Friday Night Jazz @ Schweikher House featuring the Paul Wagner QuartetFriday Night Jazz @ Schweikher House featuring the Paul Wagner Quartet on Fri, June 25, 2021 6:30 PM – 8:00 PM CDT, event page: https://www.eventbrite.com/e/friday-night-jazz-schweikher-house-featuring-the-paul-wagner-quartet-tickets-159162879457?aff=ebdssbdestsearch
4. The Courtyard Series Presents: Jazz & Beyond Maja RiosThe Courtyard Series Presents: Jazz & Beyond Maja Rios on Tue, August 3, 2021 6:30 PM – 8:30 PM CDT, event page: https://www.eventbrite.com/e/the-courtyard-series-presents-jazz-beyond-maja-rios-tickets-157686228755?aff=ebdssbdestsearch
5. John Hanrahan & Friends - Coltrane CelebrationJohn Hanrahan & Friends - Coltrane Celebration on Wed, June 23, 2021 8:00 PM – 9:30 PM CDT, event page: https://www.eventbrite.com/e/john-hanrahan-friends-coltrane-celebration-tickets-158173630587?aff=ebdssbdestsearch
6. JAZZ FESTIVAL in the park!JAZZ FESTIVAL in the park! on Sat, July 10, 2021 5:00 PM – 11:00 PM CDT, event page: https://www.eventbrite.com/e/jazz-festival-in-the-park-tickets-156145831385?aff=ebdssbdestsearch
7. 3rd Annual Chicago Jazz Getaway - September 16 - 19, 20213rd Annual Chicago Jazz Getaway - September 16 - 19, 2021 on Thu, Sep 16, 2021, 6:00 PM – Sun, Sep 19, 2021, 7:00 PM CDT, event page: https://www.eventbrite.com/e/3rd-annual-chicago-jazz-getaway-september-16-19-2021-tickets-71848008327?aff=ebdssbdestsearch
8. Jon Deitemyer performs  ART PEPPER + ELEVEN @ Fulton Street CollectiveJon Deitemyer performs  ART PEPPER + ELEVEN @ Fulton Street Collective on Tue, July 13, 2021 8:00 PM – 10:30 PM CDT, event page: https://www.eventbrite.com/e/jon-deitemyer-performs-art-pepper-eleven-fulton-street-collective-tickets-159532924271?aff=ebdssbdestsearch
9. THE REGULATORS - Jazz in the Park Outdoor Concert SeriesTHE REGULATORS - Jazz in the Park Outdoor Concert Series on Thu, June 17, 2021 8:00 PM – 10:00 PM CDT, event page: https://www.eventbrite.com/e/the-regulators-jazz-in-the-park-outdoor-concert-series-tickets-154779586911?aff=ebdssbdestsearch
10. Neil Carson's New Nostalgia live @ Fulton Street CollectiveNeil Carson's New Nostalgia live @ Fulton Street Collective on Wed, July 7, 2021 8:00 PM – 10:30 PM CDT, event page: https://www.eventbrite.com/e/neil-carsons-new-nostalgia-live-fulton-street-collective-tickets-159518952481?aff=ebdssbdestsearch
11. Thursday Night Life Music Live from the Allegro Royal Sonesta HotelThursday Night Life Music Live from the Allegro Royal Sonesta Hotel on Multiple Dates , event page: https://www.eventbrite.com/e/thursday-night-life-music-live-from-the-allegro-royal-sonesta-hotel-tickets-153477626713?aff=ebdssbdestsearch
12. Jazz Under the Twilight Car Concert Dee, Terisa, Meagan, &  SamJazz Under the Twilight Car Concert Dee, Terisa, Meagan, &  Sam on Sat, July 24, 2021 4:00 PM – 10:00 PM CDT, event page: https://www.eventbrite.com/e/jazz-under-the-twilight-car-concert-dee-terisa-meagan-sam-tickets-158563705311?aff=ebdssbdestsearch
13. Gustavo Cortinas & Desafio Candente live  @ Fulton Street CollectiveGustavo Cortinas & Desafio Candente live  @ Fulton Street Collective on Wed, June 23, 2021 8:00 PM – 10:30 PM CDT, event page: https://www.eventbrite.com/e/gustavo-cortinas-desafio-candente-live-fulton-street-collective-tickets-158252115337?aff=ebdssbdestsearch
14. Delvon Lamarr Organ Trio - 8pm ShowDelvon Lamarr Organ Trio - 8pm Show on Sun, October 3, 2021, 8:00 PM CDT Doors at 7:00 PM, event page: https://www.eventbrite.com/e/delvon-lamarr-organ-trio-8pm-show-tickets-154628609333?aff=ebdssbdestsearch
15. Sunday Supper ClubSunday Supper Club on Multiple Dates , event page: https://www.eventbrite.com/e/sunday-supper-club-tickets-152759470689?aff=ebdssbdestsearch
16. Fly Me To The Moon: The Music of Vince GuaraldiFly Me To The Moon: The Music of Vince Guaraldi on Multiple Dates , event page: https://www.eventbrite.com/e/fly-me-to-the-moon-the-music-of-vince-guaraldi-tickets-152701366899?aff=ebdssbdestsearch
17. Clark Sommer's LENS: In-Person & Livestream @ Fulton Street CollectiveClark Sommer's LENS: In-Person & Livestream @ Fulton Street Collective on Sun, June 27, 2021 8:00 PM – 10:30 PM CDT, event page: https://www.eventbrite.com/e/clark-sommers-lens-in-person-livestream-fulton-street-collective-tickets-159317429721?aff=ebdssbdestsearch
18. Saxophonist Rajiv Halim QuintetSaxophonist Rajiv Halim Quintet on Sat, June 19, 2021 8:00 PM – 9:30 PM CDT, event page: https://www.eventbrite.com/e/saxophonist-rajiv-halim-quintet-tickets-156299569219?aff=ebdssbdestsearch
19. SSMA presents SENSES to SOUL School of MusicSSMA presents SENSES to SOUL School of Music on Fri, June 25, 2021 7:00 PM – 9:30 PM CDT, event page: https://www.eventbrite.com/e/ssma-presents-senses-to-soul-school-of-music-tickets-157527861073?aff=ebdssbdestsearch
20. Saxophonist Isaiah Collier & The Chosen FewSaxophonist Isaiah Collier & The Chosen Few on Fri, June 25, 2021 8:00 PM – 9:30 PM CDT, event page: https://www.eventbrite.com/e/saxophonist-isaiah-collier-the-chosen-few-tickets-156573207679?aff=ebdssbdestsearch
```

**Optional Parameters**

- *number* - You can specify the number of events (in multiples of 20) -- 20 is the default -- with the optional `-n` parameter: `python scraper.py jazz chicago il -n 40`.
- *database* - You can specify the database -- `sqlite` or `mysql`, set to `sqlite` as default -- with the optional `-d` parameter: `python scraper.py jazz chicago il -d mysql`.

If you need help on the usage run: `python scraper.py -h`.

## Using a MySQL database

To use MySQL you'll need to create a `.env` file that has the following values: `DATABASE_USER` and `DATABASE_PASSWORD`.
For information on setting up MySQL you can read the docs [here](https://dev.mysql.com/doc/mysql-installer/en/).

## Querying the data

Depending on the database flavor you choose, you can can query the data with with the database flavor's command line utility:

For example with `sqlite`:

```
$ sqlite3
> .open all_events.db
> select count(*) from all_events;
20
```

Or with `mysql`:

```
$ mysql -u USERNAME -p PASSWORD
> use database all_events;
> select count(*) from events;
20
```

### Questions?

You can contact me at `me@lorenamesa.com`.
