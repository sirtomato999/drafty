#!/usr/bin/python
#
# getlist.py downloads and parses a list from https://www.fantasypros.com
#
print('working...')

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
    if rows.index(row) in [49, 75, 101, 202]:
        continue
    
    row_data = row.find_all('td')

    print(f'\r{rows.index(row)+1}/399', end='')

    rank = int(row_data[0].get_text())
    name = row.find_all('span')[0].get_text() 
    pos = row_data[3].get_text()
    pos = ''.join([i for i in pos if not i.isdigit()])

    if pos.startswith('K'):
        pos = 'K'
    elif pos == 'DST':
        pos = 'D'
        name = name[:-5]
        
    team = row.find_all('small')[0].get_text()

    if "FA" in team:
        team = -1
    elif "a href" in team:
        team = -1

    try:
        bye = int(row_data[4].get_text())
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

print()

f = open('list.json', 'w')
json_dump = json.dumps(list, sort_keys=True)
f.write(json_dump)
f.close()

f = open('list', 'w')

for p in list:
    player = '{:4} {:25} {:2} {:2} {}'.format(p[0], f'{p[1]} {p[2]} {p[3]}', p[4], p[5], p[6])
    f.write(f'{player}\n')
    f.flush()

print(' done!')
