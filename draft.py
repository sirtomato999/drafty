#!/usr/bin/env python3
import subprocess

def display_teams(team, my_pick):
    for t in range(teams):
        style = ''
        if t == team:
            style += "\033[1m\033[33m"
        if t == my_pick:
            style += "\033[34m"

        print(f'{style}{t} \033[0m', end='')
    print()



if __name__ == '__main__':
    with open('list') as f:
        playerlist = f.readlines()

    print(" == drafty fzf edition == ")
    
    my_pick = int(input("what is your pick number? ")) - 1
    teams = int(input("how many teams are there? "))

    cmd = ''
    players = []
    for i in range(teams): players.append([])

    overall_pick = 0
    last_teams = [2, 1, 0]
    add = -1

    while 1:
        last_teams.append(last_teams[2] + add)
        last_teams.pop(0)

        for i in range(3):
            if last_teams[i] > teams - 1:
                last_teams[i] = teams - 1

            elif last_teams[i] < 0:
                last_teams[i] = 0

        if last_teams[1] == teams - 1:
            add = -1
        elif last_teams[1] == 0:
            add = 1

        print('\033[2J\033[H', end='')
        display_teams(last_teams[-1], my_pick)
        print()

        print("\033[1m" + ('your' if my_pick == last_teams[-1] else 'their') + ' team\033[0m')
        print(''.join(players[last_teams[-1]]))

        input('press enter to select player')

        process = subprocess.run(['fzf'], stdout=subprocess.PIPE,\
                input=''.join(playerlist).encode('utf-8')).stdout.decode()

        playerlist.remove(process)
        players[last_teams[-1]].append(process)


        

