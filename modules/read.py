#!/usr/bin/env python3

from sys import argv
from re import sub

target = sub('(^\w+:|^)\/\/', '', argv[1])

def aggressive_read(url):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(f'http://{url}')
        for _ in range(10):
            page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
            page.wait_for_timeout(1000)
        value = page.locator('body').inner_text()
        browser.close()
        return value

def static_read(url):
    from objetive import text
    return text(f'http://{url}')

if argv[2] == '0':
    print(static_read(target))
else:
    print(aggressive_read(target))

