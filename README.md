# D4N155
It's a tool of security audit for smart wordlist and Google hacking attack

[Help us](CONTRIBUTING.md)

[See some calculations used](https://adasecurity.github.io/D4N155/theories/#operation-of-d4n155)

# Use
Need to:[Python3.6](https://realpython.com/installing-python/),
[Bash (GNU Bourne-Again SHell)](https://www.gnu.org/software/bash/#download), [pip3](https://pip.pypa.io/en/stable/installing/)

Optional: [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)


> You are advised to use proxychains for scan

```bash
git clone https://github.com/adasecurity/D4N155.git
cd D4N155
pip3 install -r requirements.txt
bash main
```
Or whithout git

```bash
wget -qO- https://github.com/adasecurity/D4N155/archive/master.zip | bsdtar -xf-
cd D4N155-master
pip3 install -r requirements.txt
bash main
```

[![asciicast](https://asciinema.org/a/222527.svg)](https://asciinema.org/a/222527)

# Manual
    D4N155: Tool for smart audit security

    Usage: bash main <option> <value>
    All options are optionals

    Options:
	-w, --wordlist	<url|ip>	Make the smartwordlist based in informations
					on website.
	-v, --vulners	<url|ip>	Get urls that can cause attacks.
	-t, --targets	<file>  	Make the smart-wordlist based in your passed
					source informations in urls.
	-b, --based	<file>		Analyze texts to generate the
					custom wordlist
	-r, --rate	<time>		Defines time interval between requests
	-o, --output	<file>		For to store the all wordlist.
	-h, --help			Show this mensage.

     Value: <url | ip | source | file | time>
	URL				URL target, example: scanme.nmap.org
	IP				IP address
	TIME				Time, example: 2.5. I.e: 0:02:30. 0 are default
	FILE				File, for save the result, get urls or using in
					wordlist


# HARDWARE REQUIREMENTS:
## CPU 
* Dual Core or Better
* Native Support to Multi-Thread

## MEMORY
* 4 GB or More

## Dependencies
> Dependencies that will be installed through pip

* beautifulsoup4==4.6.3
* google==2.0.1
* numpy==1.15.4
* requests==2.20.1
* mechanicalsoup
     
<h3 align="center">This project are part of Segmentation fault<br/></h3>
<h5 align="center">It's GNU/GPL version 3 Project page: https://github.com/adasecurity/D4N155</h5>
<p align="center">
		<img src="https://jul10l1r4.github.io/assets/segmentation-fault.png" alt="Segmentation fault">
</p>
