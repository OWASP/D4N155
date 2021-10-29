#!/usr/bin/env bash

# $1 = url
_set_method(){
  if [ "$aggressive" == "0" ]
  then
    printf '0'
  else
    printf '1'
  fi
}

printf "$(python3 'modules/read.py' "$1" $(_set_method))"
