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
# Draft 3.1.0 by Matthew Wozniak
#

import pickle, time

print("\033c", end="")

print("""
     _            __ _         
  __| |_ __ __ _ / _| |_ _   _ 
 / _` | '__/ _` | |_| __| | | |
| (_| | | | (_| |  _| |_| |_| |
 \__,_|_|  \__,_|_|  \__|\__, |
                         |___/ 
""")
print("draft v3.1.0")

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


def fancylist(input_list):
    for i in range(len(input_list)):
        print(' %-22s %s' % (str(i+1) + ' ' + ' '.join(input_list[i][1:-1]), input_list[i][-1]))


def main():
    global list
    command = ''
    while not command == 'quit':
        print('==========================')
        top = topten()
        fancylist(top)
        print('==========================')
        command = input("List number, player pos, or first three letters of last name \n^C to cancel any prompts\n> ").lower()

                ############################## COMMAND PARSING #############################

        try:
            temp = int(command)
            if temp > 10 or temp < 1:

                print('Between one and ten!')
                temp = between_one_and('List number: ', len(top))

                if temp == 0:
                    print("\033c", end="")
                    continue

            list.remove(top[temp-1])
            print("\033c", end="")
            continue
        except ValueError: pass
        if len(command) == 3:
            print('Last Name')
            last = topten(last=command)

            if len(last) == 0:
                continue
            if len(last) == 1:
                print("\033c", end='')
                fancylist(last)
                input('Hit enter to draft, ^C to cancel... ')
                list.remove(last[0])
                continue
            print("\033c", end="")
            fancylist(last)
            number = between_one_and('List number: ', len(last))
            list.remove(last[int(number)])
            print("\033c", end="")
        if len(command) == 2 or len(command) == 1:
            print("\033c", end="")
            print('POS: ' + command)

            pos = topten(pos=command)
            fancylist(pos)
            number = between_one_and('List number: ', len(pos))
            list.remove(pos[number-1])
            print("\033c", end="")


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
    except: pass
