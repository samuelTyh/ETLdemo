#!/bin/bash
set -e

mkdir -p data/"$1"

echo -e "START: Pulling the weather data of ""$1""\n"
if python3 etl/utils/pull_data.py "$1"
then
  echo -e "\n\nSUCCESS: Data stored correctly\n--------------------"
else
  rm -r data/"$1"
fi
