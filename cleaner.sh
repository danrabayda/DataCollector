#!/bin/bash
file="___.log"

lines=$(cat $file |grep -n ',' |cut -d':' -f1)
counter=0
last_code=""
for line in $lines
 do
  timestamp=$(sed "${line}q;d" $file |cut -d',' -f2 |cut -d'.' -f1 |cut -d' ' -f2)
  #echo $timestamp
  line2=$(($line + 1))
  code=$(sed "${line2}q;d" $file |tail -1 |cut -d'|' -f2 |cut -d' ' -f2)
  if [ $counter -eq 4 ]; then
   echo "$timestamp  $code  $counter"
   counter=0
  elif [ $last_code = $code ]; then
   let "counter++"
  else
   counter=0
  fi
  last_aircraft=$aircraft
done
