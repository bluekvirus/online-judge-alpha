#!/bin/bash
echo "Started"
var=`phantomjs hackerrank.js`
echo $var
if [[ "$var" == "Unable to access network" ]]; then
	echo "invalid"
	sleep 1m
	exec bash "$0"
else
	trimmed=$(echo "$var"|/bin/grep -Po '(?<=hrank:).*')
	echo $trimmed  > '/home/cherie/Desktop/myhackerrank/myhackerrank/hrank.txt'
fi

