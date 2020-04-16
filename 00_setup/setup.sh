#!/bin/sh

export ENV_BUCKET='s3a://demo-aws-2'

if [[ -z "${STORAGE}" ]]; then
  export STORAGE=$ENV_BUCKET
fi

hdfs dfs -mkdir -p $STORAGE/datalake/tmp/airlines/airports/
hdfs dfs -mkdir -p $STORAGE/datalake/tmp/airlines/carriers/
hdfs dfs -mkdir -p $STORAGE/datalake/tmp/airlines/flights/

hdfs dfs -copyFromLocal -f /home/cdsw/airlines/airports/airports.csv $STORAGE/datalake/tmp/airlines/airports/airports.csv
hdfs dfs -copyFromLocal -f /home/cdsw/airlines/carriers/carriers.csv $STORAGE/datalake/tmp/airlines/carriers/carriers.csv
hdfs dfs -copyFromLocal -f /home/cdsw/airlines/flights/1988.csv.bz2 $STORAGE/datalake/tmp/airlines/flights/1988.csv.bz2

#python3 /home/cdsw/00_setup/create_tables.py

#pip3 install -r /home/cdsw/requirements.txt