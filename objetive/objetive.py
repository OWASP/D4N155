import sys
import mechanicalsoup # needed

def main(url):
    # Connect to target
    browser = mechanicalsoup.StatefulBrowser()

    try:
        status = browser.open(url) # func_timeout(15, browser.open, args=sys.argv[1])

        if 'text/' in status.headers['Content-Type']:
            pass
        else:
            #exit(2)
            pass

    except:
        #exit(1)
        pass

    # All functions for get values
    def all():
        value = ""
        for p in browser.get_current_page().select('p'):
            value = value + p.text + ' '

        for h1 in browser.get_current_page().select('h1'):
            value = value + h1.text + ' '

        for link in browser.get_current_page().select('a'):
            value = value + link.text + ' '

        return value.translate(str.maketrans(' ', ' ', '\n\t')).replace('—','').replace(',','').replace('|','')
    # All texts
    try:
        return all()
    except:
        return "Not any texts :("
