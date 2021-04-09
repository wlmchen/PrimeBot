#!/bin/bash

echo "Getting current quantity of Linux Distributions..."
q=$(wget --no-check-certificate -q -O - distrowatch.com/weekly.php?issue=current | grep "all distributions</a> in the database" | awk -F":" '{ print $2 }' | awk -F"<" '{ print $1 }')
echo "There are$q linux distibutions @ $(date +%d.%m.%Y)"

echo "Loading distros list..."
wget  --no-check-certificate -q -O - distrowatch.com | grep -A $q "height: 20%" | awk -F"<" '{ print $1 }' | tail -n  +2 > ./primebot/assets/linux.list
