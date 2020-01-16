#!/usr/bin/env python3
from sys import argv, exit
from duckduckgo.search import go_duck
from google.search import go_gle

# vars
use = 'Use: search.py "<seach expression>"'
enable_dorks = '''\
Dorks Google and Duckduckgo search
----------------------------------
site\t\tFind all urls of domain
intitle\t\tFinds pages that include a specific keyword as part of the indexed title
inurl\t\tFind pages that include a specific keyword as a part
filetype\tSearch for specific file type
intext\t\tSearh for specific text
feed\t\tFind RSS related to search term\
'''
banner = f'''\
GeTrails are projet for OSINT and Dorks
{use}
\t-d, --dorks\t\tDorks enable in Google and Duckduckgo hacking
Issue: github.com/Vault-Cyber-Security/getrails/issues\
'''

def search_now (query):
    try:
        result = go_gle(query)
        result = go_duck(query)
    except:
        result = go_duck(query)
    return result

# Use
if len(argv) < 2:
    print(f'{use}')
    exit(1)
elif argv[1] == '--help' or argv[1] == '-h':
    print(banner)
    exit(0)
elif argv[1] == '--dorks' or argv[1] == '-d':
    print(enable_dorks)
    exit(0)

print(search_now(argv[1]))
