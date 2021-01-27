#!/bin/bash

mkdir -p data/"$1"

echo -e "START: Pull the weather data of ""$1""\n"
if python3 pull_data.py "$1"
then
  echo -e "\n\nSUCCESS: data stored correctly\n--------------------"
else
  rm -r data/"$1"
fi

echo -e "\nSTART: ETL process"
if python3 etl.py
then
  echo -e "\nSUCCESS: data processed completely"
fi