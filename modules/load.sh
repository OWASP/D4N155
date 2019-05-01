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
  done & trap "kill $!" EXIT  #Die with parent if we die prematurely
  eval "$2"
  kill $! && trap " " EXIT 
}

