These modules extend D4N155 to generate custom word lists per name identified on the page. The assumption is that the user will provide a "Contact Us" or "About Us" page as input. The additions include:

Standard custom word list generation, which will attempt to scrape the page for human names (as well as username handles based on @ and twitch.tv/), find websites associated with the human names, and place the names in a file under the names modules/names directory with the name used.

Aggressive custom word list generation, which will attempt to perform a reverse image search on photographs of people under the assumption that they may reuse photographs.

The aggressive word generation is significantly slower because it finds extra results for images on each searched result.

For the searches of people, there is also the getCookies function, which allows the user to pass in a Firefox profile to take any session tokens and use these when searching through websites.
This should help with social media sites which block the user if they have not logged in. Users who wish to use this feature should open a Firefox browser, navigate to the about:profiles section, log in with a given profile, and copy the profile's directory into the profilePath variable.



To run:

python3 modules/nameSearch.py [0 for no reverse image and 1 for reverse image] [url] [optionalFireFoxfrofilePath] [optionalFirefoxBinaryPath]

This will produce a directory called "names" with wordlists for each identified name.


To extract names, this module uses spaCy: https://spacy.io/usage

python google search: https://python-googlesearch.readthedocs.io/en/latest/