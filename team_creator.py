import random
import os
from itertools import combinations


def createRandomTeam(city_name):
    file_path = os.path.join(city_name.lower(), 'teams.txt')
    roles = {'DF': [], 'MF': [], 'ST': []}

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for row in f:
                parts = row.strip().split()
                if len(parts) == 4:
                    name, point, role, status = parts
                    if status.upper() == 'O':
                        roles[role.upper()].append({'name': name, 'point': float(point), 'role': role.upper()})
    except FileNotFoundError:
        return None

    def get_best_split(players, count_per_team):
        all_combos = list(combinations(players, count_per_team))
        best_diff = float('inf')
        best_pair = ([], [])

        total_puan = sum(p['point'] for p in players)

        for combo in all_combos:
            team1_puan = sum(p['point'] for p in combo)
            team2_puan = total_puan - team1_puan
            diff = abs(team1_puan - team2_puan)

            if diff < best_diff:
                best_diff = diff
                team2 = [p for p in players if p not in combo]
                best_pair = (list(combo), team2)

        return best_pair

    df1, df2 = get_best_split(roles['DF'][:6], 3)
    mf1, mf2 = get_best_split(roles['MF'][:4], 2)
    st1, st2 = get_best_split(roles['ST'][:4], 2)

    t1 = df1 + mf1 + st1
    t2 = df2 + mf2 + st2

    return (t1, t2) if random.random() > 0.5 else (t2, t1)


def drawPitch(team_name, team):
    dfs = [o['name'] for o in team if o['role'] == 'DF']
    mfs = [o['name'] for o in team if o['role'] == 'MF']
    sts = [o['name'] for o in team if o['role'] == 'ST']
    total_point = sum(o['point'] for o in team)

    def f(name): return f"{name[:10]:^10}"

    print(f"\n{'=' * 41}")
    print(f"{team_name.center(41)}")
    print(f"Total Team Point: {total_point:.1f}".center(41))
    print(f"{'=' * 41}")
    print("                 [ GK ]                ")
    print("  _____________________________________  ")
    print(" |                                     | ")
    print(f" |  {f(dfs[0])} {f(dfs[1])} {f(dfs[2])}  | ")
    print(" |                                     | ")
    print(f" |       {f(mfs[0])}   {f(mfs[1])}       | ")
    print(" |                  _                  | ")
    print(" |_________________( )_________________| ")
    print(" |                                     | ")
    print(f" |       {f(sts[0])}   {f(sts[1])}       | ")
    print(" |                                     | ")
    print(" |_____________________________________| ")


city = input("Match Name: ").strip()
res = createRandomTeam(city)
if res:
    t1, t2 = res
    drawPitch("A Team", t1)
    drawPitch("B Team", t2)