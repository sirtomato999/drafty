#
# List: pickle file named list in same dir
# Format: [[<rank: int>, <first name: str>, <last name: str>, <Jr, Sr, etc: str>, <position: str>]]
# positions: WR    WR
#            RB    RB
#            TE    TE
#            K     K
#            DEF   D
#            FLEX  Real Position
#
# Draft 3.9.0 by Matthew Wozniak
#

import pickle, time

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
    command = ''
    while not command == 'quit':
        print("\033c", end="")
        print("""\033[0;32m
       _            __ _         
    __| |_ __ __ _ / _| |_ _   _ 
  / _` | '__/ _` | |_| __| | | |
 | (_| | | | (_| |  _| |_| |_| |
  \__,_|_|  \__,_|_|  \__|\__, |
                           |___/ 
        """)
        print("draft v3.9.0\033[0m")


        print('\033[0;34m==========================')
        top = topten()
        fancylist(top)
        print('\033[0;34m==========================\033[0m')
        command = input("List number, player pos, or first three letters of last name \nUse rank the the first three letters of a players last name for their rank\n^C to cancel any prompts\n> ").lower()

                ############################## COMMAND PARSING #############################

        try:
            temp = int(command)
            if temp > 10 or temp < 1:

                print('Between one and ten!')
                temp = between_one_and('List number: ', len(top))

                if temp == 0:
                    continue

            list.remove(top[temp-1])

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
                continue
            fancylist(last)
            number = between_one_and('List number: ', len(last))
            list.remove(last[int(number)])
        if len(command) == 2 or len(command) == 1:
            print("\033c", end="")
            print('POS: ' + command)

            pos = topten(pos=command)
            fancylist(pos)
            number = between_one_and('List number: ', len(pos))
            list.remove(pos[number-1])

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
while 1:
    try:
        main()
        break
    except: print("\033c", end="")
