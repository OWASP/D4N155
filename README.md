# OWASP D4N155 
[![made-with-bash](https://img.shields.io/badge/Made%20with-Bash-1f425f.svg)](https://github.com/OWASP/D4N155/search?l=shell) [![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://github.com/OWASP/D4N155/blob/master/LICENSE) [![OWASP project](https://img.shields.io/badge/Project-OWASP-1f425f)](https://github.com/OWASP)

It's an information security audit tool that creates intelligent wordlists based on the content of the target page.

[Help us](https://www2.owasp.org/www-project-d4n155/#div-contributing)

[See some calculations used](https://www2.owasp.org/www-project-d4n155/#div-operations)

# Install
Need to: [Python3.6](https://realpython.com/installing-python/), [Bash (GNU Bourne-Again SHell)](https://www.gnu.org/software/bash/#download)

Optional: [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git), [Groff](https://www.gnu.org/software/groff/)

```bash
git clone https://github.com/owasp/D4N155.git
cd D4N155
pip3 install -r requirements.txt
bash main
```
Or whithout git

```bash
wget -qO- https://github.com/owasp/D4N155/archive/master.zip | bsdtar -xf-
cd D4N155-master
pip3 install -r requirements.txt
bash main
```

[![asciicast](https://asciinema.org/a/294029.svg)](https://asciinema.org/a/294029)

# Manual
```
    D4N155: Tool for smart audit security

    Usage: bash main <option> <value>
    All options are optionals

    Options:
	-w, --wordlist	<url|ip>	Make the smartwordlist based in informations
					on website.
	-t, --targets	<file>  	Make the smart-wordlist based in your passed
					source informations in urls.
	-b, --based	<file>		Analyze texts to generate the
					custom wordlist
	-r, --rate	<time>		Defines time interval between requests
	-o, --output	<file>		For to store the all wordlist.
  -?a, --aggressive      Aggressive reading with headless
	-h, --help			Show this mensage.

     Value: <url | ip | source | file | time>
	URL				URL target, example: scanme.nmap.org
	IP				IP address
	TIME				Time, example: 2.5. I.e: 0:02:30. 0 are default
	FILE				File, for save the result, get urls or using in
					wordlist
```
