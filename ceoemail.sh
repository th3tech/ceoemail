#!/bin/bash

mkdir payload
rm payload/*

IFS=$'\n'
proxies=$(cat proxy.list)
sites=$(cat sites.list)
loop=3
for site in ${sites}
do
  # Grab a random proxy
  rnd=$(echo ${RANDOM})
  proxy=$(grep -n $ proxy.list | grep "^$(echo ${rnd} | cut -c1):" | cut -d: -f2)
  port=$(grep -n $ proxy.list | grep "^$(echo ${rnd} | cut -c1):" | cut -d: -f3)
  echo "Examaning site ${site}"
  echo "python ceoemail.py --proxy "${proxy}" --port ${port} --loop ${loop} --url ${site}"
  python ceoemail.py --proxy "${proxy}" --port ${port} --loop ${loop} --url ${site} > output.txt
  links=$(cat output.txt | sed 's/href=\"/\n/g')
  links=$(cat output.txt | grep href=\"s.php output.txt | sed 's/href=\"/\n/g' | cut -d'"' -f1 | grep ceo)
  for link in ${links}
  do
    echo "Scraping ${link}"
    proxy=`grep -n $ proxy.list | grep $(echo ${RANDOM} | cut -c1) | cut -d: -f2`
    python ceoemail.py --proxy "${proxy}" --port ${port} --loop ${loop} --url "http://ceoemail.com/${link}" > payload/${loop}.txt
    loop=`expr ${loop} + 1`
  done
  sleep 30
done
