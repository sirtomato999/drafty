#!/usr/bin/python
#
# getlist.py downloads and parses a list from https://www.fantasypros.com
#
print('Working...')

from bs4 import BeautifulSoup
import requests
import sys
import json

if "--ppr" in sys.argv:
    soup = BeautifulSoup(requests.get\
        ('https://www.fantasypros.com/nfl/rankings/ros-ppr-overall.php').text, 'lxml')
else:
    soup = BeautifulSoup(requests.get\
        ('https://www.fantasypros.com/nfl/rankings/ros-overall.php').text, 'lxml')
table = soup.find_all('tbody')[0]
rows = table.find_all('tr')
list = []


for row in rows:
    if rows.index(row) == 50:
        continue
    row_data = row.find_all('td')

    rank = int(str(row_data[0])[40:][:-5])
    name = str(row.find_all('span')[0]) [24:] [:-7] #takes slice from first span object (name)
    pos = str(row_data[3])[4:6]

    if pos.startswith('K'):
        pos = 'K'
    elif pos == 'DS':
        pos = 'D'
        name = name[:-5]
        
    team = str(row.find_all('small')[0]).strip('</small>').lstrip('<small class="grey">')

    if "FA" in team:
        team = -1
    elif "a href" in team:
        team = -1
    try:
        bye = int(str(row_data[4]).strip('</td>').lstrip('<td>'))
    except ValueError:
        bye = -1

    name0 = name.split()[0]
    try:
        name1 = name.split()[1]
    except:
        name1 = ""

    try:
        name2 = name.split()[2]
    except:
        name2 = ""

    player = [rank, name0, name1, name2, pos, bye, team]
    list.append(player)

f = open('list', 'w')
list = json.dumps(list, indent=2, sort_keys=True)
f.write(list)
print('List dumped to file "list" in the current directory')
