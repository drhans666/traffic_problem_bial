# road_problem_bial.py - script searches bialystok-related website for traffic problems
from get_and_clean import get_streets, get_dates
from search_4_news import get_news

news = get_news()


for i in range(0, 3):
    print('loading...')
    url = news[i]
    dates = get_dates(url)
    streets = get_streets(url)
    print(dates)
    # if source article in wrong form print:
    if 'li class' in streets:
        print('Sorry. Streets not loaded correctly\n')

    else:
        print(streets)

