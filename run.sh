#!/bin/bash

mkdir -p data/$1

if python3 pull_data.py $1
then
  echo -e "--------------------\n\nSUCCESS: data stored correctly"
else
  rm -r data/$1
fi
