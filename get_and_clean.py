
import bs4
import requests
import re


def check_url(url):
    # gets/checks & passes url
    source_url = requests.get(url)
    try:
        source_url.raise_for_status()
    except Exception as exc:
        print('There was a problem: %s' % exc)
    return source_url


def get_streets(url):
    source_url = check_url(url)

    # bs4 parsing of url
    street_url_soup = bs4.BeautifulSoup(source_url.text, "html.parser")
    samples = street_url_soup.select('ul')
    streets = str(samples[3])

    # cleans parsed text from html statements
    not_wanted = ['</li>', '<strong>', '</strong>', '<p>', '</p>', '<ul>', '</ul>']
    for i in not_wanted:
        streets = streets.replace(i, "")
    streets = streets.replace('<li>', '-')
    return streets


def get_dates(url):
    source_url = check_url(url)

    # bs4 parsing of url
    event_url_soup = bs4.BeautifulSoup(source_url.text, "html.parser")
    samples = event_url_soup.select('div p')
    raw_dates = str(samples[2])

    # regex search for date in month-word pattern
    dates_regex = re.compile(r'''(
    \d{1,2}       # day of month
    \s            # space
    [a-z]+        # mont name
    \s            # space
    \d{4}         # year
    )''', re.VERBOSE)
    dates_result = dates_regex.findall(raw_dates)

    # regex search for date in month-number pattern
    dates_regex2 = re.compile(r'''(
    \d{1,2}       # day of month
    .             # dot
    \d{1,2}       # month
    .             # dot
    \d{4}         # year
    )''', re.VERBOSE)
    dates_result2 = dates_regex2.findall(raw_dates)

    # return period of time with word-month pattern
    try:
        dates = dates_result[0] + ' - ' + dates_result[1]
    # if no period of time, try single date with word-month pattern
    except IndexError:
        try:
            dates = dates_result[0]
    # if no period/single date with word-month pattern try period number-month pattern
        except IndexError:
            try:
                dates = dates_result2[0] + ' - ' + dates_result2[1]
    # if no period of time in number-month pattern try single date
            except IndexError:
                dates = dates_result2[0]

    return dates
