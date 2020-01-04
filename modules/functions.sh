#!/usr/bin/env bash

# This file contains
# Functions in order by
# _vul
# _wordlist
# _fwordlist

# Update db
_updateDB(){
	printf "$orange You want update the list Google hacking? (y/n)$green\n → "
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
}

# Check Time format
_checkTime(){
  if [ "$1" == "" ] || [[ ! "$1" =~  ^[+-]?([0-9]*[.])?[0-9]+$ ]]
  then
    export time="0"
    elif [[ "$1" =~ ^[+-]?([0-9]*[.])?[0-9]+$ ]] || [[ "$1" =~ ^-?[0-9]+$ ]]
  then
    export time="$settime"
  fi
}

# Download Gecko with arch
_getGecko(){
	if [ "$(uname -m) | grep 64 -q" ]
	then	
		$(wget "https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz" -q \
      -O "modules/geckodriver/Geckodriver.tar")
	else
		$(wget "https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux32.tar.gz" --progress=bar \
      -O "modules/geckodriver/Geckodriver.tar") 
	fi
  [ -e "modules/geckodriver/geckodriver" ] || echo -e "$incorrect Dont downloaded, check you conection"
  # Extract file to geckodriver
  tar -C "modules/geckodriver/" -xf "modules/geckodriver/Geckodriver.tar" || exit 1
}

# Check if gecko are install
_checkGecko(){
	if [ -e "modules/geckodriver/geckodriver" ]
	then
		echo -e "$correct Gecko file exists"
	else
		echo "Download Geckodriver"
		_getGecko
		[ -e "modules/geckodriver/GeckoDriver" ] && echo -e "$correct Geckodriver downloaded" || echo -e "$incorrect Geckodriver error"
	fi
}

# Get expression and get all pages indexes of google
# 1# just read page
# 2# get all texts, alts etc.
# 3# add alternations in names stored
# 4# make combinations
# 5# save and call route of file
__wordlist(){
	# Check arguments
	if [ "$1" != "" ]
	then
		echo "Attacking $1"
    target="$(printf $1 | awk '{ gsub("['/',':','-']","");print }')"
    
    # Checking time parse
    [ "$3" != ""  ] && export time="$3" || export time="0"
	else
		printf "Target is: $1"; read target
    target="$(printf $target | awk '{ gsub("['/',':','-']","");print }')";

    # Get time rate
    printf "Time interval in seconds (Default: -1): ";read settime
    _checkTime 
  fi

  # Define destination to save
	[ "$#" == "2" ] && \
		export dest="$2" || \
		export dest="reports/wordlist/$target.wordlist.txt"
	
	# Make the attack
	echo -e "$orange Beginning attack, with Google indexations$end"
	
  # Run pagodo for get all urls
  cd pagodo/
	python3 pagodo.py -d $target -l 300 -s -e 1

  # If get all ok then:
	if [ "$?" = "0" ]
	then
		cd ..
		mv "pagodo/$target.txt" "reports/db/" 2> /dev/null

    if [ "$?" == "0" ]
    then
			echo -e "Finalized search to $target, database\nhas been saved in$orange reports/db/$target.txt$green"
    else
      echo -e "$red The file dont has been saved, the result was found?$green"
      exit 2
    fi

		echo "Make the wordlist *-*"
    
    . modules/operations/calc.sh "reports/db/$target.txt" "$target" "$dest"

		test "$?" == 0 && \
		  echo -e "$green Wordlist has been saved in\n$orange$dest$end" || \
			exit 1

			# clear trash files
      # Call report pdf
    . modules/report/main.sh "reports/db/$target.txt" "reports/db/$target.blob.txt" \
      "$dest"  "$target"
		rm -rf reports/db/$target.*
		exit 0
	else
		echo -e "Error: in$red pagodo.py$green\n"
	fi
}

# _fwordlist
# means file wordlist
# This function are main for get targets based in file
# root directory
__fwordlist (){

  [ "$3" != ""  ] && export time="$3" || export time="0"

  . modules/operations/calc.sh "$1" "wordlist" "reports/wordlist/wordlist.txt"
	
	if [ "$?" == "0" ]
	then
		echo -e "$green Wordlist has been saved in\n$orange./reports/wordlist/wordlist.txt$end"
		# clear trash files
    # Report in pdf
    . ./modules/report/main.sh "$1" "reports/db/wordlist.blob.txt" \
        "reports/wordlist/wordlist.txt" "custom"
	  rm -rf reports/db/wordlist.blob.txt
		exit 0
	else
		echo -e "$red Error in save the wordlist $green"
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
  python3 "modules/generator.py" "$1" >> "$save" && \
    ( echo -e "$correct Wordlist been created in $save"; exit 0 ) || \
    echo -e "$incorrect Error fatal, don't create file"; exit 2

}
