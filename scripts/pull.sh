#!/bin/bash

ETL_SOURCE=data/

set -e

mkdir -p $ETL_SOURCE"$1"

echo -e "START: Pulling the weather data of ""$1""\n"
if python3 etl/utils/pull_data.py $ETL_SOURCE "$1"
then
  echo -e "\n\nSUCCESS: Data stored correctly\n--------------------"
else
  rm -r $ETL_SOURCE"$1"
fi
