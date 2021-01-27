#!/bin/bash
set -e

echo -e "\nSTART: ETL process"
echo -e "START: Create tables"
if python3 etl/create_table.py
then
  echo -e "\nSUCCESS: Tables created successfully"
else
  echo -e "\nFAILURE: Failed to create tables"
fi

echo -e "START: Insert data"
if python3 etl/process.py
then
  echo -e "\nSUCCESS: Data processed completely"
else
  echo -e "\nFAILURE: Failed to process data"
fi
