#!/bin/bash

sp="⡿⣟⣯⣷⣾⣽⣻⢿"
sc=0
spin() {
   printf "\r\b${sp:sc++:1} $1 "
   ((sc==${#sp})) && sc=0
}

_load(){
  while :;do
    spin "$1"
  done & trap "kill $!" EXIT 2> /dev/null
  eval "$2"
  kill $! && trap " " EXIT 2> /dev/null 
}

