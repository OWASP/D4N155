#!/usr/bin/env python3
import mechanicalsoup

def go_duck(query):

    # Connect to duckduckgo
    browser = mechanicalsoup.StatefulBrowser()
    browser.set_user_agent('Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0')
    browser.open(f"https://duckduckgo.com/html/?q={query}")
    
    # List 
    list1 = []

    # Subfunction
    def change_page():
        browser.select_form(browser.get_current_page().select('form')[-1])
        browser.submit_selected()
        read_urls()


    def check():
        if browser.get_current_page().select('.btn--alt'):
            change_page()

    def read_urls():
        for link in browser.get_current_page().select('a.result__url'):
            list1.append(link.text.replace('\n',''))

        check()
        return '\n'.join(filter(bool, list1))

    return read_urls().replace(' ','')
