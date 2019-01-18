#!/usr/bin/env bash

# Get expression and get all dorks of google hacking
# All vul. pages and routers :]
__vul(){
	# Check arguments
	if [ "$1" ]
	then
		echo "Attacking $1"
		target="$1"
	else
		printf "Target is: $1"; read target
	fi

	# Update db
	echo -e "\033[33mYou want update the list Google hacking? (y/n)\033[32m"
	read typed
	case $typed in
		"Yes" | y*)
			echo "Updating database"
			echo "`python3 pagodo/ghdb_scraper.py`"
		;;
		"No" | n*)
			echo "OK ..."
		;;
	esac

	# Make the attack
	echo -e "\033[33mBenning attack using diferents user agents ;)\033[32m"
	cd pagodo/
	echo "It will to delay..."
	# It's good? Then go go go go
	python3 pagodo.py -d $target -g google_dorks.txt -l 40 -s -e 1
	if [ "$?" = "0" ]
	then
		mv $target.txt ../reports/ &&
			echo "Finalized attack to $target, see in reports/$target.txt" || 
			echo -e "\033[31mThe file dont has been saved\033[32m"
	else
		echo -e "Error: in \033[31mpagodo.py\033[33m\nrun: pip3 install -r requirements.txt\033[32m"
	fi
	cd ../
}

# Get expression and get all pages indexes of google
# 1# just read page
# 2# get all texts, alts etc.
# 3# add alternations in names stored
# 4# make combinations
# 5# save and call route of file
__wordlist(){
	# Check arguments
	if [ "$1" ]
	then
		echo "Attacking $1"
		target="$1"
	else
		printf "Target is: $1"; read target
	fi

	# Make the attack
	echo -e "\033[33mBenning attack, with Google indexations\033[32m"
	cd pagodo/
	# It's good? Then go go go go
	python3 pagodo.py -d $target -g blank.txt -l 300 -s -e 1
	if [ "$?" = "0" ]
	then
		# Check if exists directory
		test -d ../reports/db &&
			echo -e "reports/db\t...\t\033[34mok\033[32m" ||
			mkdir ../reports/db
		# Check if be ok
		mv "$target.txt" "../reports/db/" &&
			echo -e "Finalized search to $target, database\nhas been saved in reports/db/$target.txt" || 
			echo -e "\033[31mThe file dont has been saved\033[32m"
		# Generate the wordlist
		#	get all urls and read all text
		#	Check for equals worlds and remove
		#	remove characters like: , or ?
		echo "Make the wordlist *-*"
		cat ../reports/db/$target.txt | \
			while read url
			do
				echo "$url";
				python3 ../objetive/objetive.py "$url" -t -txt -a >> ../reports/db/$target.blob.txt
			done && \
				\
			python3 ../modules/generator.py "$(cat ../reports/db/$target.blob.txt)" \
				> ../reports/wordlist/$target.wordlist.txt || \
				echo -e "\033[031mError fatal\033[32m"

			echo -e "\033[032mWordlist has been saved in\n\033[033m$here/reports/wordlist/$target.wordlist.txt\033[0m"
			# clear trash files
			rm -rf ../reports/db/$target*
			exit 0
	else
		echo -e "Error: in \033[31mpagodo.py\033[33m\nrun: pip3 install -r requirements.txt\033[32m"
	fi
	cd ../
}

