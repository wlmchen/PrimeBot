#!/bin/bash
# Script helps you to download Distrowatch.com Linux database, sorts and saves it locally.
# This script can help you in classifying content on the web, build analytics, infographics etc.
# It's description and information on how to use it is in official github - welcome:
# https://github.com/sxiii/distrowatch-scraper

echo "Getting current quantity of Linux Distributions..." 
q=$(wget --no-check-certificate -q -O - distrowatch.com/weekly.php?issue=current | grep "all distributions</a> in the database" | awk -F":" '{ print $2 }' | awk -F"<" '{ print $1 }')
echo "There are$q linux distibutions @ $(date +%d.%m.%Y)"

echo "Loading distros list..." 
wget  --no-check-certificate -q -O - distrowatch.com | grep -A $q "height: 20%" | awk -F"<" '{ print $1 }' > linux.list
