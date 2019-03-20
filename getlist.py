#!/usr/bin/python
#
# getlist.py downloads and parses a list from https://www.fantasypros.com
#
print('Working...')
try:
    from bs4 import BeautifulSoup
    import requests
    import sys

except ImportError:
    import reqs
    reqs.install()
    import requests
    import sys
    from bs4 import BeautifulSoup

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

    rank = int(str(row_data[0])[4:][:-5])

    name = str(row.find_all('span')[0]) [24:] [:-7] #takes slice from first span object (name)

    pos = str(row_data[3])[4:6]
    if pos.startswith('K'):
        pos = 'K'
    elif pos == 'DS':
        pos = 'D'
        name = name[:-5]
    print(row_data[4])
    bye = int(str(row_data[4])[3:5].strip('<')).lstrip('>')

    name0 = name.split()[0]
    try:
        name1 = name.split()[1]
    except:
        name1 = 0

    try:
        name2 = name.split()[2]
    except:
        name2 = 0

    if name2:
        player = [rank,name0,name1,name2,pos,bye]
    elif name1:
        player = [rank,name0,name1,pos,bye]
    else:
        player = [rank,name0,pos,bye]
    list.append(player)

f = open('list', 'w')
list = json.dumps(list, indent=4, sort_keys=True)
f.write(list)
print('List dumped to file "list" in the current directory')
