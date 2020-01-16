#!/usr/bin/env python3
from googlesearch import search, get_random_user_agent

def go_gle (query):
    my_results_list = []
    for i in search(query,        # Expression
                    tld = 'com',  # TL domain
                    lang = 'en',  # Set lang en
                    num = 10,     # Number of results / page
                    start = 0,    # First result to retrieve
                    stop = None,  # Last result to retrieve
                    pause = 0,  # Lapse between HTTP requests
                    user_agent = get_random_user_agent(),
                   ):
        my_results_list.append(i)

    return '\n'.join(my_results_list)
