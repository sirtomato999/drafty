#!/usr/bin/python3
#
# List: pickle file named list in same dir
# Format: [ [<rank: int>, <first name: str>, <last name: str>, <Jr, Sr, etc: str>, <position: str>, <bye: int>] ]
# positions: WR    -
#            RB    -
#            TE    -
#            K     -
#            DEF   D
#
# Draft 4.1.4 by Matthew Wozniak
#

import json, time, sys, os
#from pickhelper import pick

if sys.platform == 'win32': # colorama win32 stuff. osx and linux both have ansi-complient terminals.
    import colorama         # stupid windows. we should all be using linux anyway
    colorama.init()

list = open('list', 'r')
list = json.load(list)

def between_one_and(prompt, limit):
    while 1:
        command = input(prompt)
        try:
            command = int(command)
            if command > limit or command < 0:
                raise ValueError
            return int(command)
        except:
            print('A number between 1 and %i!' % limit)
    return int(command)

def topten(pos='',last=''):
    global list
    global temp
    if pos:
        temp = []
        for i in list:
           if i[-2] == pos.upper():
                temp.append(i)
        return temp[:10]
    elif last:
        temp = []
        for i in list:
            if i[2].lower().startswith(last.lower()):
                temp.append(i)
        return temp
    else:
        return list[:10]

def fancylist(input_list, rank=0):
    print('\033[0;34m', end='')
    print('#  Name                   Pos Team Bye')
    for i in range(len(input_list)):
        
        name = ' '.join(input_list[i][1:3])
        pos = input_list[i][-3]
        bye  = input_list[i][-2]
        team = input_list[i][-1]
        rank = input_list[i][0]
        
        if bye == -1:
            bye = 'FA'
        if team == -1:
            team = ''
            
        if not rank:
            print("%-2i %-22s %-3s " % (i + 1, name, pos) + str(bye))
            
        else:
            print("%-2i %-22s %-3s %-4s %s" % (rank, name, pos, team, bye))
    print('\033[0m', end='')

def main(increment=True):

    global list
    global overallpick
    global pick
    global round
    global index
    command = ''
    while True:
        if not sys.platform == 'win32':
            print("\033c", end="")
        else:
            os.system('cls')
        if not '--no-figlet' in sys.argv:
        	print("""\033[0;32m
       _            __ _
    __| |_ __ __ _ / _| |_ _   _
  / _` | '__/ _` | |_| __| | | |
 | (_| | | | (_| |  _| |_| |_| |
  \__,_|_|  \__,_|_|  \__|\__, |
                           |___/
        """)
        print("\033[0;32mdraft v4.1.4\033[0m")
        print('\033[0;34m======================================')
        top = topten()
        fancylist(top)
        print('\033[0;34m======================================\033[0m')

        ### CALCULATE PICK, ROUND, ETC. BASED ON OVERALL PICK

        if increment:
            overallpick = overallpick + 1

        round = (overallpick // teams) + 1

        pick = ((overallpick - teams*round) + teams) + 1

        isevenround = (overallpick // teams) % 2

        if isevenround:
            backwards = True
        else:
            backwards = False

        if backwards:
            index = abs((overallpick - teams*round))
        else:
            index = pick

        increment = True        

        addToTeam = False #resets
        if index == picknum:
            addToTeam = True
            print("\nYour turn!\n")
        if not team == []:
            print('Team: ')
            fancylist(team)
            print()

        print('Overall pick: %i' % overallpick)
        print("Round: %i\nPick: %i\nIndex: %i\n"  % (round, pick, index))


        command = input("Type ? for help\n> ").lower()
        if not command:
            increment = False
            continue
        if command == 'quit':
            sys.exit()
        ### PARSE COMMAND


        try:
            if command == '?': raise ValueError
            temp = int(command)

            if temp > 10 or temp < 1:
                print('Between one and ten!')
                temp = between_one_and('List number: ', len(top))

            list.remove(top[temp-1])
            if addToTeam:
                team.append(top[temp-1])
            continue
        except ValueError: pass


        if command == '?':
            input("""
?		        Show this help message
r <last>	    Show the overall rank of a player (first three letters)
b <bye>		    Search by byeweek
<last>		    Search for the player with that last name (first three letters)
<top ten rank>	Draft top ten player
<position>	    Shows top ten players from that position\n\n\nPress Enter to continue
teams           Shows the team abbreviations for search for `tm`
t  <team abbr> searches for players on a team""")
            increment=False
            input('Press Enter to Continue...')
            continue
        
        # searches by teams #
        if command.startswith('t '): 
            command = command.lstrip('t ').strip().upper()
            print(command)
            temp = []
            for player in list:
                if player[-1] == command:
                    temp.append(player)
            fancylist(temp)
            index = between_one_and("which item on the list would you like? ", len(temp))
            list.remove(temp[index-1])
            if addToTeam:
                team.append(temp[index-1])
        
        # prints teams #
        if command.startswith('teams'):
            print('''
ARI: Arizona Cardinals
ATL: Atlanta Falcons
BAL: Baltimore Ravens
BUF: Buffalo Bills
CAR: Carolina Panthers
CHI: Chicago Bears
CIN: Cincinnati Bengals
CLE: Cleveland Browns
DAL: Dallas Cowboys
DEN: Denver Broncos
DET: Detroit Lions
GB: Green Bay Packers
HOU: Houston Texans
IND: Indianapolis Colts
JAX: Jacksonville Jaguars
KC: Kansas City Chiefs
MIA: Miami Dolphins
MIN: Minnesota Vikings
NE: New England Patriots
NO: New Orleans Saints
NYG: New York Giants
NYJ: New York Jets
OAK: Oakland Raiders
PHI: Philadelphia Eagles
PIT: Pittsburgh Steelers
SD: San Diego Chargers
SEA: Seattle Seahawks
SF: San Francisco 49ers
STL: Saint Louis Rams
TB: Tampa Bay Buccaneers
TEN Tennessee Titans
WAS: Washington Redskins
            ''')
            increment=False
            input('Press Enter to Continue...')
            continue

        # searches by rank #
        if command.startswith('r '):
            command = command.split()
            if not len(command) == 2:
                input("Usage: r <first 3 letters of player's last name>\nPress Enter...")

            ranks = topten(last=command[1])
            fancylist(ranks, rank=1)
            input('Press Enter... ')

        # searches by byeweek # 
        if command.startswith('b '):
            bye = command.lstrip('b')
            bye = bye.lstrip(' ')
            byelist = []
            try:
                for player in list:
                    if player[-2] == int(bye):
                        byelist.append(player)
            except:
                input('a bye is only a number\nPress Enter...')
                increment = False
                continue
            byelist = byelist[:10]
            fancylist(byelist)
            number = between_one_and('List number: ', len(byelist))
            list.remove(byelist[number-1])
        
        # not bye
        if command.startswith('nb'):
            bye = command.lstrip('nb ')
            byelist = []
            try:
                for player in list:
                    if not player[-1] == int(bye):
                        byelist.append(player)
            except:
                input('a bye is only a number\nPress Enter...')
                increment = False
                continue
            byelist = byelist[:10]
            fancylist(byelist)
            number = between_one_and('List number: ', len(byelist))
            list.remove(byelist[number-1])
        # last name
        if len(command) == 3:
            print('Last Name')
            last = topten(last=command)

            if len(last) == 0:
                input("No such player! Press Enter to continue... ")
                increment = False
                continue
            if len(last) == 1:
                fancylist(last)
                input('Hit enter to draft, ^C to cancel... ')
                list.remove(last[0])
                if addToTeam:
                    team.append(last[0])

                continue
            fancylist(last)
            number = between_one_and('List number: ', len(last))
            list.remove(last[int(number)-1])
            if addToTeam:
                team.append(last[int(number)-1])

        #posistion
        if len(command) == 2 or len(command) == 1:
            if not sys.platform == 'win32':
                print("\033c", end="")
            else:
                os.system('cls')
            print('POS: ' + command)

            pos = topten(pos=command)
            fancylist(pos)
            number = between_one_and('List number: ', len(pos))
            list.remove(pos[number-1])
            if addToTeam:
                team.append(pos[number-1])



team = []

picknum = int(input('What is your pick number? '))
teams = int(input('How many teams are there? '))

overallpick = 0
pick = 1
round = 1

while True:
    try:
        main(increment=False)
        break
    except KeyboardInterrupt:
        if not sys.platform == 'win32':
            print("\033c", end="")
        else:
            os.system('cls')
