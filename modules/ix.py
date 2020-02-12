from requests import post

def ix_api(wordlist):
    try:
        response = post('http://ix.io', {'f:2': wordlist}).text
    except:
        response = f':( Error for ix.io'
    
    return response
