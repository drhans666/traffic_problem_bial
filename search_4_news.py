import bs4
import requests
import re


def get_news():
    # gets and checks url
    main_url = requests.get('https://www.bialystok.pl/pl/dla_mieszkancow/drogi_i_inwestycje/utrudnienia-drogowe.html')
    try:
        main_url.raise_for_status()
    except Exception as exc:
        print('There was a problem: %s' % exc)

    # bs4 parsing of url
    main_url_soup = bs4.BeautifulSoup(main_url.text, "html.parser")
    samples = main_url_soup.select('h2 a')
    raw_url = str(samples)

    # cleans url addresses from html statements and descriptions
    raw_url_regex = re.compile(r'''(
    pl            
    [-a-zA-Z0-9/_]+
    .html
    )''', re.VERBOSE)
    url_result = raw_url_regex.findall(raw_url)
    url_list = []
    for i in range(0, 3):
        url_list.append('https://www.bialystok.pl/' + url_result[i])
    return url_list


