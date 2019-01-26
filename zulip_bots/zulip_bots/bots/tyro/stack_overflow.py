import requests
import logging
import re
import urllib

from typing import Optional, Any, Dict
def get_bot_stackoverflow_response(message):
    help_text = 'Please enter your query after @mention-bot to search StackOverflow'

        # Checking if the link exists.
    query = message
    if query == '' or query == 'help':
        return help_text

    query_stack_url = 'http://api.stackexchange.com/2.2/search/advanced'
    query_stack_params = dict(
        order='desc',
        sort='relevance',
        site='stackoverflow',
        title=query
    )
    try:
        data = requests.get(query_stack_url, params=query_stack_params)

    except requests.exceptions.RequestException:
        logging.error('broken link')
        return 'Uh-Oh ! Sorry ,couldn\'t process the request right now.\n' \
               'Please try again later.'

    # Checking if the bot accessed the link.
    if data.status_code != 200:
        logging.error('Page not found.')
        return 'Uh-Oh ! Sorry ,couldn\'t process the request right now.\n' \
               'Please try again later.'

    new_content = 'For search term:' + query + '\n'

    # Checking if there is content for the searched term
    if len(data.json()['items']) == 0:
        new_content = 'I am sorry. The search term you provided is not found'
    else:
        for i in range(min(3, len(data.json()['items']))):
            search_string = data.json()['items'][i]['title']
            link = data.json()['items'][i]['link']
            new_content += str(i+1) + ' : ' + '[' + search_string + ']' + '(' + link + ')\n'
    return new_content
