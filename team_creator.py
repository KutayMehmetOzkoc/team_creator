import random
import os

def createRandomTeam(file_name):
    players = []
    notplayers = []
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            for row in f:
                parts = row.strip().split()
                if len(parts) == 3:
                    name, point, status = parts
                    if status.upper() == 'O':
                        players.append({'name': name, 'puan': float(point)})
                    else :
                        notplayers.append({'name': name, 'puan': float(point)})
    except FileNotFoundError:
        print("File Not Found!")
        return None

    if len(players) < 14:
        print(f"Not Enough Player For Match: {len(players)}")
        return None

    squad = sorted(players[:14], key=lambda x: x['puan'], reverse=True)
    squad1 = []
    squad2 = []

    for i in range(0, 14, 2):
        ikili = [squad[i], squad[i + 1]]
        random.shuffle(ikili)

        squad1.append(ikili[0])
        squad2.append(ikili[1])

    return squad1, squad2, notplayers


def printerFunction(team_name, team):
    total_point = sum(o['puan'] for o in team)
    print(f"\n--- {team_name} (Total Point: {total_point:.1f}) ---")
    for o in team:
        print(f"- {o['name']} ({o['puan']})")

#main
matchName = input("Please enter match name: ").strip()

file_path = os.path.join(matchName.lower(), 'teams.txt')
res = createRandomTeam(file_path)

if res:
    t1, t2, t3 = res
    printerFunction("A TEAM", t1)
    printerFunction("B TEAM", t2)
    printerFunction("NOT IN GAME", t3)