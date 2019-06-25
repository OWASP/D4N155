#!/usr/bin/env bash

__expect(){
  eval "$1"
  if [ "$?" != "0" ];
  then
    echo "Error in run: $2"
  else
    echo "Success in run: $2"
  fi
}
