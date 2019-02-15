#!/usr/bin/env bash

# This file contains
# Functions in order by
# _vul
# _wordlist
# _fwordlist

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

	test "$#" == "2" && \
		export dest="$2" || \
		export dest="reports/wordlist/$target.wordlist.txt"
	
	
	# Make the attack
	echo -e "\033[33mBenning attack, with Google indexations\033[32m"
	cd pagodo/
	# It's good? Then go go go go
	python3 pagodo.py -d $target -g blank.txt -l 300 -s -e 1
	if [ "$?" = "0" ]
	then
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
				python3 "../objetive/objetive.py" "$url" \
				>> ../reports/db/$target.blob.txt && \
				echo -e ":.........................................[\e[92m✔\e[32m]" || \
				echo -e ":.........................................[\e[31m✘\e[32m]"
			done && \
				\
			python3 "../modules/generator.py" "$(cat ../reports/db/$target.blob.txt)" \
				> ../$dest || \
        ( echo -e "\033[031mError fatal\033[32m";exit 2 )

			test "$?" == 0 && \
				echo -e "\033[032mWordlist has been saved in\n\033[033m$dest\033[0m" || \
				exit 1
			# clear trash files
      # Call report pdf
      . ../modules/report/main.sh "../reports/db/$target.txt" "../reports/db/$target.blob.txt" \
          "../$dest"  "$target"
			rm -rf ../reports/db/$target.*
			exit 0
	else
		echo -e "Error: in \033[31mpagodo.py\033[33m\nrun: pip3 install -r requirements.txt\033[32m"
	fi
	cd ../
}

# _fwordlist
# means file wordlist
# This function are main for get targets based in file
# root directory
__fwordlist (){

	cat  $1 |\
		while read url
		do
			echo "$url";
			python3 "objetive/objetive.py" "$url" \
				>> reports/db/wordlist.blob.txt && \
				echo -e ":.........................................[\e[92m✔\e[32m]" || \
				echo -e ":.........................................[\e[31m✘\e[32m]"
		done && \   
			\
			python3 "modules/generator.py" "$(cat reports/db/wordlist.blob.txt)" \
				> "reports/wordlist/wordlist.txt" || \
        ( echo -e "\033[031mError fatal\033[32m";exit 2 )
	
		if [ "$?" == "0" ]
		then
			echo -e "\033[032mWordlist has been saved in\n\033[033m./reports/wordlist/wordlist.txt\033[0m"
			# clear trash files
      # Report in pdf
      . modules/report/main.sh "$1" "reports/db/wordlist.blob.txt" \
          "reports/wordlist/wordlist.txt"  "$1"
			rm -rf reports/db/wordlist.blob.txt
			exit 0
		else
			echo -e "\033[31mError in save the wordlist\033[32m"
			exit 1
		fi
}
# Cus of custom :] | Staps
# 1 - Get text
# 2 - send to generator.py
# 3 - save
__cus() {
  # $1 → file base
  # $2 → file to output
  echo "$2"
  [ $2 ] && export save="$2" || export save="_wordlist.txt"
  echo "$save"
  echo "Processing all data..."
  python3 "modules/generator.py" "$(cat $1 | awk '{ gsub("['–',',']","");print }')"  >> "$save" && \
    ( echo -e "[\e[92m✔\e[m] Wordlist been created in $save"; exit 0 ) || \
    ( echo -e "[\e[31m✘\e[m] Error fatal, don't create file"; exit 2 )

}
