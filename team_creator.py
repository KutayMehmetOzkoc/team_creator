import random
import os
from itertools import combinations


def createRandomTeam(city_name):
    file_path = os.path.join(city_name.lower(), 'teams.txt')
    all_players = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for row in f:
                parts = row.strip().split()
                if len(parts) == 4:
                    name, point, role, status = parts
                    if status.upper() == 'O':
                        all_players.append({
                            'name': name,
                            'point': float(point),
                            'role': role.upper()
                        })
    except FileNotFoundError:
        print(f"Hata: {file_path} dosyası bulunamadı.")
        return None

    if len(all_players) < 14:
        print(f"Hata: Yetersiz oyuncu sayısı ({len(all_players)}). 14 oyuncu gerekli.")
        return None

    squad = all_players[:14]

    all_possible_teams = list(combinations(squad, 7))
    total_squad_point = sum(p['point'] for p in squad)

    best_diff = float('inf')
    best_team1 = []

    for combo in all_possible_teams:
        team1 = list(combo)
        team1_point = sum(p['point'] for p in team1)
        team2_point = total_squad_point - team1_point
        diff = abs(team1_point - team2_point)

        if diff < best_diff:
            best_diff = diff
            best_team1 = team1
            if diff == 0: break

    team2 = [p for p in squad if p not in best_team1]

    if random.random() > 0.5:
        return best_team1, team2
    else:
        return team2, best_team1


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

    df_line = " ".join([f(n) for n in dfs]).center(37)
    print(f" |{df_line}| ")

    print(" |                                     | ")

    mf_line = " ".join([f(n) for n in mfs]).center(37)
    print(f" |{mf_line}| ")

    print(" |                  _                  | ")
    print(" |_________________( )_________________| ")

    print(" |                                     | ")

    st_line = " ".join([f(n) for n in sts]).center(37)
    print(f" |{st_line}| ")

    print(" |                                     | ")
    print(" |_____________________________________| ")


# Main
city = input("Match Name (Match Group Folder): ").strip()
res = createRandomTeam(city)
if res:
    t1, t2 = res
    drawPitch("A TEAM", t1)
    drawPitch("B TEAM", t2)