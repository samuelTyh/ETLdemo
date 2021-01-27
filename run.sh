#!/bin/bash
set -e

mkdir -p data/"$1"

echo -e "START: Pulling the weather data of ""$1""\n"
if python3 pull_data.py "$1"
then
  echo -e "\n\nSUCCESS: Data stored correctly\n--------------------"
else
  rm -r data/"$1"
fi

echo -e "\nSTART: ETL process"
echo -e "START: Create tables"
if python3 create_table.py
then
  echo -e "\nSUCCESS: Tables created successfully"
else
  echo -e "\nFAILURE: Failed to create tables"
fi

echo -e "START: Insert data"
if python3 etl.py
then
  echo -e "\nSUCCESS: Data processed completely"
else
  echo -e "\nFAILURE: Failed to process data"
fi