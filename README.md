# D4N155
![](https://img.shields.io/badge/Documentation-ON-%0f0) [![made-with-bash](https://img.shields.io/badge/Made%20with-Flask-1f425f.svg)](https://github.com/OWASP/D4N155/search?l=shell) [![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://github.com/OWASP/D4N155/blob/master/LICENSE)

## API project of D4N155
See test app: [d4n155.herokuapp.com/](https://d4n155.herokuapp.com/)

| PROTOCOL | PATH | FUNCTION | EXAMPLE |
|:--------:|:----:|:--------:|:--------:|
|   GET    |/make/:word|Operations|localhost/make/moscou%201918|
|   GET    |/domain/:domain|Get all urls of Domain|localhost/domain/nmap.org|
|   GET    |/domain/:number-limit:url|Get wordlist|localhost/domain/30?url=nmap.org|

## Run local
```sh
git clone https://github.com/owasp/D4N155.git
git checkout api
docker-compose up
```

### Response
All response is `JSON` format.
#### localhost/make/<param>
  ```JSON
  {
  "helpus": "Its OWASP D4N155 project for API, see: https://github.com/OWASP/D4N155, branch: api",
  "result":
    {
      "data": ["<PARAm>1", "..."],
      "length": 40,
      "wordlist":{
        "length": 40,
        "url": "http://ix.io/2cEW\n"
      }
    }
  }
  ```
  * `result`
  * * `result.data`: Result of wordlist __limit 500 :(__
  * * `result.length`: Length of wordlist returned in `result.data`
  * * `result.wordlist`:
  * * * `result.wordlist.length`: Length of complete wordlist
  * * * `result.wordlist.url`: Link of wordlist
  
### localhost/domain/scanme.nmap.org
```JSON
{
  "helpus":"Its OWASP D4N155 project for API, see: https://github.com/OWASP/D4N155, branch: api",
  "result":{
    "data":["scanme.nmap.org","..."],
    "length":4
  }
}
```
  * `result`
  * * `result.data`: Result of domains
  * * `result.length`: Number of domains
  
### localhost/domain/500?url=https://jul10l1r4.github.io
```JSON
{
  "helpus":"Its OWASP D4N155 project for API, see: https://github.com/OWASP/D4N155, branch: api",
  "result":{
    "data":["mEDIUM/vAULcYBERsEC1","..."],
    "length":500,
    "wordlist":{
      "length":48132,
      "url":"http://ix.io/2bx9\n"
    }
  }
}
```
  * `result`
  * * `result.data`: Result of wordlist __limit 500 :(__
  * * `result.length`: Length of wordlist returned in `result.data`
  * * `result.wordlist`:
  * * * `result.wordlist.length`: Length of complete wordlist
  * * * `result.wordlist.url`: Link of wordlist


## API-CLIENT
* [Telegram bot: OWASP D4N155](https://github.com/Jul10l1r4/D4N155_bot)
* [Codepen: Function to make words](https://codepen.io/Jul10l1r4/pen/gObVoMd)
* [Codepen: Function to search urls](https://codepen.io/Jul10l1r4/pen/jOPEKPj)
* [Codepen: Function to read url](https://codepen.io/Jul10l1r4/pen/KKpdzVJ)
