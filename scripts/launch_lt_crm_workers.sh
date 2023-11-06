#!/bin/bash
if [ -z "$3" ]
  then
      echo "No argument supplied"
      echo "start_workers.sh nbr_workers concurrency time"
      exit 1
fi
x=1
while [ $x -le $1 ]
do
  locust -f lt_crm.py --worker --only-summary > /dev/null 2>&1 &
  x=$(( $x + 1 ))
done
locust -f lt_crm.py --headless --users $2 --spawn-rate $2 --run-time $3m --master --expect-workers=$1