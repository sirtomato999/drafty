#
# List: pickle file named list in same dir
# Format: [ [<rank: int>, <first name: str>, <last name: str>, <Jr, Sr, etc: str>, <position: str>] ]
# positions: WR    -
#            RB    -
#            TE    -
#            K     -
#            DEF   D
#            FLEX  Real Position
#
# Draft 4.0.2 by Matthew Wozniak
#

# I need this to live
true = True
false = False

import pickle, time, sys, os

if sys.platform == 'win32': # colorama win32 stuff. osx and linux both have ansi-complient terminals.
    import colorama         # stupid windows. we should all be using linux anyway
    colorama.init()

list = open('list', 'rb')
list = pickle.load(list)

def topten(pos='',last=''):
    global list
    global temp
    if pos:
        temp = []
        for i in list:
           if i[-1] == pos.upper():
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
    for i in range(len(input_list)):
        print(' %-22s %s' % ((str(i+1) if not rank else str(input_list[i][0])) + ' ' + ' '.join(input_list[i][1:-1]), input_list[i][-1]))
    print('\033[0m', end='')

def main():

    global list
    global overallpick
    global pick
    global round
    global index

    command = ''
    while not command == 'quit':
        if not sys.platform == 'win32':
            print("\033c", end="")
        else:
            os.system('cls')
        print("""\033[0;32m
       _            __ _
    __| |_ __ __ _ / _| |_ _   _
  / _` | '__/ _` | |_| __| | | |
 | (_| | | | (_| |  _| |_| |_| |
  \__,_|_|  \__,_|_|  \__|\__, |
                           |___/
        """)
        print("draft v4.0.2\033[0m")


        print('\033[0;34m==========================')
        top = topten()
        fancylist(top)
        print('\033[0;34m==========================\033[0m')

        ### CALCULATE PICK, ROUND, ETC. BASED ON OVERALL PICK


        overallpick = overallpick + 1
        round = (overallpick // teams) + 1

        pick = ((overallpick - teams*round) + teams) + 1

        isevenround = (overallpick // teams) % 2

        if isevenround:
            backwards = true
        else:
            backwards = false

        if backwards:
            index = abs((overallpick - teams*round))
        else:
            index = pick

        addToTeam = false #resets
        if index == picknum:
            addToTeam = True
            print("\nYour turn!\n")
            if not team == []:
                print('Team: ')
                fancylist(team)
                print()

        print('Overall pick: %i' % overallpick)
        print("Round: %i\nPick: %i\nIndex: %i\n"  % (round, pick, index))


        command = input("List number, player pos, or first three letters of last name \nUse rank the the first three letters of a players last name for their rank\n^C to cancel any prompts\n> ").lower()

        ### PARSE COMMAND

        try:
            temp = int(command)
            if temp > 10 or temp < 1:

                print('Between one and ten!')
                temp = between_one_and('List number: ', len(top))

                if temp == 0:
                    continue

            list.remove(top[temp-1])
            if addToTeam:
                team.append(top[temp-1])
            continue
        except ValueError: pass

        if len(command) == 3:
            print('Last Name')
            last = topten(last=command)

            if len(last) == 0:
                input("No such player! Press Enter to continue... ")
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
            list.remove(last[int(number)])
            if addToTeam:
                team.append(last[int(number)])
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
        if command.startswith('rank'):
            command = command.split()
            if not len(command) == 2:
                input("Usage: rank <first 3 letters of player's last name>\nPress Enter...")

            ranks = topten(last=command[1])
            fancylist(ranks, rank=1)
            input('Press Enter... ')

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

team = []

picknum = int(input('What number pick are you? '))
teams = int(input('How many teams are there? '))

overallpick = -1
pick = 1
round = 1

while true:
    try:
        main()
        break
    except KeyboardInterrupt:
        if not sys.platform == 'win32':
            print("\033c", end="")
        else:
            os.system('cls')
        main()
