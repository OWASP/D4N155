#!/usr/bin/env bash
# $1 = url

if [  "$aggressive" == "0" ] 
then
  printf "$(python3 objetive/objetive.py "$1")"
else
  printf "$(python3 modules/aggressive-read.py "$1")"
fi
