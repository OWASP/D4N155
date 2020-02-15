# D4N155
![](https://img.shields.io/badge/Documentation-OFF-%23f00) [![made-with-bash](https://img.shields.io/badge/Made%20with-Flask-1f425f.svg)](https://github.com/OWASP/D4N155/search?l=shell) [![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://github.com/OWASP/D4N155/blob/master/LICENSE)

# API project of D4N155
Test: [d4n155.herokuapp.com/make/param](https://d4n155.herokuapp.com/make/test%20param)

| PROTOCOL | PATH | FUNCTION |
|:--------:|:----:|:--------:|
|   GET    |/make/:word|Operations|
|   GET    |/domain/:domain|Get all urls of Domain|
|   GET    |/domain/:number-limit:url|Get wordlist|

# Example
* [d4n155.herokuapp.com/make/param](https://d4n155.herokuapp.com/make/test%20param) `// Limit: 500 :(`
* [d4n155.herokuapp.com/domain/scanme.nmap.org](https://d4n155.herokuapp.com/domain/scanme.nmap.org)
* [d4n155.herokuapp.com/domain/500?url=http://scanme.nmap.org/](https://d4n155.herokuapp.com/domain/500?url=http://scanme.nmap.org/)

# Run local
```sh
git clone https://github.com/owasp/D4N155.git
git checkout api
docker-compose up
```
