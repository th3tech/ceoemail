#!/bin/bash

mkdir payload
rm payload/*

IFS=$'\n'
proxies=$(cat proxy.list)
sites=$(cat sites.list)
loop=0
for site in ${sites}
do
  # Grab a random proxy
  proxy=`grep -n $ proxy.list | grep $(echo ${RANDOM} | cut -c1) | cut -d: -f2`
  echo "Examaning site ${site}"
  python ceoemail.py --proxy none-ip.info --url ${site} > output.txt
  links=$(cat output.txt | sed 's/href=\"/\n/g')
  links=$(cat output.txt | grep href=\"s.php output.txt | sed 's/href=\"/\n/g' | cut -d'"' -f1 | grep ceo)
  for link in ${links}
  do
    echo "Scraping ${link}"
    python ceoemail.py --proxy none-ip.info --url "http://ceoemail.com/${link}" > payload/${loop}.txt
    loop=`expr ${loop} + 1`
  done
  sleep 30
done
