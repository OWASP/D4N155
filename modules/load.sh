#!/bin/bash

sp="⡿⣟⣯⣷⣾⣽⣻⢿"
sc=0
spin() {
  printf "\r${sp:sc++:1} $1 "
  ((sc==${#sp})) && sc=0
}

_load(){
  while :;do
    spin "$1"
  done & trap "kill -9 $! 2> /dev/null" exit 2> /dev/null
  eval "$2" > /dev/null
}
