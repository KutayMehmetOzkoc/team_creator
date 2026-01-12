import random
import os
from itertools import combinations


def createRandomTeam(city_name):
    file_path = os.path.join(city_name.lower(), 'teams.txt')
    playing = []
    not_playing = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for row in f:
                parts = row.strip().split()
                if len(parts) == 4:
                    name, point, role, status = parts
                    player_data = {'name': name, 'point': float(point), 'role': role.upper()}

                    if status.upper() == 'O':
                        playing.append(player_data)
                    else:
                        not_playing.append(player_data)
    except FileNotFoundError:
        print(f"Hata: {file_path} bulunamadı.")
        return None

    if len(playing) < 14:
        print(f"Hata: Oynayacak (O) kişi sayısı yetersiz ({len(playing)}).")
        return None

    match_squad = playing[:14]
    extras = playing[14:] + not_playing

    all_possible_teams = list(combinations(match_squad, 7))
    total_squad_point = sum(p['point'] for p in match_squad)

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

    team2 = [p for p in match_squad if p not in best_team1]

    t1, t2 = (best_team1, team2) if random.random() > 0.5 else (team2, best_team1)
    return t1, t2, extras


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


def listExtras(extras):
    if extras:
        print(f"\n{'#' * 41}")
        print(f"{'Out Of Match'.center(41)}")
        print(f"{'#' * 41}")
        for p in extras:
            print(f"- {p['name']:<15} | Rol: {p['role']:<3} | Point: {p['point']}")
        print(f"{'#' * 41}")


# Main
city = input("Match Name (City Folder): ").strip()
res = createRandomTeam(city)
if res:
    team_a, team_b, out_players = res
    drawPitch("A TEAM", team_a)
    drawPitch("B TEAM", team_b)
    listExtras(out_players)