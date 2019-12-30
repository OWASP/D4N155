#!/usr/bin/env bash
# $1 = url

if [  "$agressive" == "0" ] 
then
  printf "$(python3 objetive/objetive.py "$1")"
else
  printf "$(python3 modules/agressive-read.py "$1")"
fi
