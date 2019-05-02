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

# Run the pagodo
_checkVul(){
  cd pagodo/
	# It's good? Then go go go go
	_load "$orange Find vulners urls $green " "python3 pagodo.py -d $target -g google_dorks.txt -l 40 -s -e 1"
	if [ "$?" = "0" ]
	then
		mv $target.txt ../reports/
    if [ "$?" == "0" ]
    then
			echo "Finalized attack to $target, see in reports/$target.txt"
    else
      echo -e "$green The file dont has been saved, The result are found?$green"
      exit 2
    fi
	else
		echo -e "Error: in $green pagodo.py$orange\nrun: pip3 install -r requirements.txt$green"
	fi
	cd ../
}

# Run operations
_calc(){
  # 1: Source
  # 2: Target
  # 3: Output

  cat  $1 |\
		while read url || exit 2
		do
			echo "$url";
			python3 "objetive/objetive.py" "$url" \
				>> "reports/db/$2.blob.txt" && \
				echo -e ":.........................................$correct" || \
				echo -e ":.........................................$incorrect"
      sleep $time
		done && \   
			_load "Make operations" "python3 'modules/generator.py' \"reports/db/$2.blob.txt\" > \"$3\"
      if [ \"$?\" != \"0\" ]
      then
        echo -e \"\n$red Error fatal$green\"
        exit 2
      fi"
}

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
  # Update list of dork
  _updateDB

	# Make the attack
	echo -e "$orange Benning attack using diferents user agents ;)$green"
	echo "It will to delay..."
  # Attack
  _checkVul  
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
	echo -e "$orange Beginning attack, with Google indexations$green"
	
  # Run pagodo for get all urls
  cd pagodo/
	_load "" "python3 pagodo.py -d $target -g blank.txt -l 300 -s -e 1"
  cd ../

  # If get all ok then:
	if [ "$?" = "0" ]
	then
		mv "pagodo/$target.txt" "reports/db/"
    
    if [ "$?" == "0" ]
    then
			echo -e "Finalized search to $target, database\nhas been saved in$orange reports/db/$target.txt$green"
    else
      echo -e "$red The file dont has been saved, the result are found?$green"
      exit 2
    fi

		echo "Make the wordlist *-*"
#		cat reports/db/$target.txt | \
#			while read url
#			do
#				echo "$url";
#				python3 "objetive/objetive.py" "$url" \
#				>> reports/db/$target.blob.txt && \
#				echo -e ":.........................................$correct" || \
#				echo -e ":.........................................$incorrect"
#        sleep $time
#			done && \
#				\
#			_load 'Make operations' "python3 'modules/generator.py' \"reports/db/$target.blob.txt\" \
#				> $dest
#        if [ \"$?\" != \"0\" ]
#        then
#          echo -e \"$red Error fatal$green\"
#          exit 2
#        fi"
    _calc "reports/db/$target.txt" "$target" "$dest"

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
		echo -e "Error: in$red pagodo.py$orange \nrun: pip3 install -r requirements.txt$green"
	fi
}

# _fwordlist
# means file wordlist
# This function are main for get targets based in file
# root directory
__fwordlist (){

  [ "$3" != ""  ] && export time="$3" || export time="0"

	cat  $1 |\
		while read url || exit 2
		do
			echo "$url";
			python3 "objetive/objetive.py" "$url" \
				>> reports/db/wordlist.blob.txt && \
				echo -e ":.........................................$correct" || \
				echo -e ":.........................................$incorrect"
      sleep $time
		done && \   
			_load "Make operations" "python3 'modules/generator.py' \"reports/db/wordlist.blob.txt\" > 'reports/wordlist/wordlist.txt'
      if [ \"$?\" != \"0\" ]
      then
        echo -e \"\n$red Error fatal$green\"
        exit 2
      fi"
	
		if [ "$?" == "0" ]
		then
			echo -e "$green Wordlist has been saved in\n$orange./reports/wordlist/wordlist.txt$end"
			# clear trash files
      # Report in pdf
      # pagodo, default of script
      cd pagodo/ 
      . ../modules/report/main.sh "../$1" "../reports/db/wordlist.blob.txt" \
          "../reports/wordlist/wordlist.txt"  "custom"
      cd ..
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
  python3 "modules/generator.py" "$(cat $1 | awk '{ gsub("['–',',']","");print }')"  >> "$save" && \
    ( echo -e "$correct Wordlist been created in $save"; exit 0 ) || \
    echo -e "$incorrect Error fatal, don't create file"; exit 2

}
