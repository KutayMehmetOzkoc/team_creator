import random
import os
from itertools import combinations

# --- DOSYA VE VERİ YÖNETİMİ ---

def load_players(city_name):
    """Dosyadan oyuncuları yükler, dosya yoksa boş liste döner."""
    file_path = os.path.join(city_name.lower(), 'teams.txt')
    players = []
    
    if not os.path.exists(city_name.lower()):
        os.makedirs(city_name.lower(), exist_ok=True)
        
    if not os.path.exists(file_path):
        return []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for row in f:
            parts = row.strip().split()
            if len(parts) == 4:
                players.append({
                    'name': parts[0],
                    'point': float(parts[1]),
                    'role': parts[2].upper(),
                    'status': parts[3].upper()
                })
    return players

def save_players(city_name, players):
    """Oyuncu listesini belirtilen klasördeki teams.txt dosyasına yazar."""
    file_path = os.path.join(city_name.lower(), 'teams.txt')
    with open(file_path, 'w', encoding='utf-8') as f:
        for p in players:
            f.write(f"{p['name']} {p['point']} {p['role']} {p['status']}\n")
    print(f"\n[OK] {file_path} güncellendi.")

# --- OYUNCU İŞLEMLERİ ---

def add_player(city_name):
    print("\n--- Yeni Oyuncu Ekle ---")
    name = input("İsim: ").strip().replace(" ", "_")
    point = float(input("Puan (örn: 70): ") or 70)
    role = input("Rol ( DF, MF, ST): ").upper()
    status = input("Durum (O: Oynuyor, Y: Yedek): ").upper()
    
    players = load_players(city_name)
    players.append({'name': name, 'point': point, 'role': role, 'status': status})
    save_players(city_name, players)

def update_player(city_name):
    players = load_players(city_name)
    if not players:
        print("\n[!] Güncellenecek oyuncu yok.")
        return

    name_to_find = input("\nGüncellenecek oyuncu adı: ").strip()
    found = False
    for p in players:
        if p['name'].lower() == name_to_find.lower():
            print(f"Mevcut: {p['name']} | Puan: {p['point']} | Rol: {p['role']} | Durum: {p['status']}")
            p['point'] = float(input(f"Yeni Puan ({p['point']}): ") or p['point'])
            p['role'] = input(f"Yeni Rol ({p['role']}): ").upper() or p['role']
            p['status'] = input(f"Yeni Durum ({p['status']}): ").upper() or p['status']
            found = True
            break
    
    if found:
        save_players(city_name, players)
    else:
        print("\n[!] Oyuncu bulunamadı.")

# --- GÖRSELLEŞTİRME ---

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
        print(f"{'MAÇ DIŞI KALANLAR'.center(41)}")
        print(f"{'#' * 41}")
        for p in extras:
            print(f"- {p['name']:<15} | Rol: {p['role']:<3} | Puan: {p['point']}")
        print(f"{'#' * 41}")

# --- TAKIM KURMA MANTIĞI ---

def create_and_show_teams(city_name):
    players = load_players(city_name)
    playing = [p for p in players if p['status'] == 'O']
    not_playing = [p for p in players if p['status'] != 'O']

    if len(playing) < 14:
        print(f"\n[!] Hata: Oynayacak (O) kişi sayısı yetersiz ({len(playing)}/14).")
        return

    match_squad = playing[:14]
    extras = playing[14:] + not_playing

    all_possible_teams = list(combinations(match_squad, 7))
    total_squad_point = sum(p['point'] for p in match_squad)

    best_diff = float('inf')
    best_team1 = []

    for combo in all_possible_teams:
        team1_point = sum(p['point'] for p in combo)
        team2_point = total_squad_point - team1_point
        diff = abs(team1_point - team2_point)

        if diff < best_diff:
            best_diff = diff
            best_team1 = list(combo)
            if diff == 0: break

    team2 = [p for p in match_squad if p not in best_team1]
    
    t1, t2 = (best_team1, team2) if random.random() > 0.5 else (team2, best_team1)
    
    drawPitch("A TAKIMI", t1)
    drawPitch("B TAKIMI", t2)
    listExtras(extras)

# --- ANA MENÜ ---

def main_menu():
    print("--- Kadro Kurucu v2.0 ---")
    city = input("Maç Adı (Klasör İsmi): ").strip()
    if not city: city = "mac_gunu"

    while True:
        print(f"\n>> ŞEHİR/MAÇ: {city.upper()}")
        print("1. Kadroları Oluştur ve Sahayı Çiz")
        print("2. Yeni Oyuncu Ekle")
        print("3. Oyuncu Bilgilerini Güncelle")
        print("4. Tüm Oyuncu Listesini Gör")
        print("5. Maç/Şehir Değiştir")
        print("0. Çıkış")
        
        secim = input("\nSeçiminiz: ")

        if secim == '1':
            create_and_show_teams(city)
        elif secim == '2':
            add_player(city)
        elif secim == '3':
            update_player(city)
        elif secim == '4':
            players = load_players(city)
            print(f"\n--- {city.upper()} Oyuncu Listesi ---")
            for p in players:
                print(f"{p['name']:<12} | {p['role']:<3} | Puan: {p['point']:.1f} | Durum: {p['status']}")
        elif secim == '5':
            city = input("Yeni Maç Adı: ").strip() or city
        elif secim == '0':
            print("Uygulama kapatılıyor...")
            break
        else:
            print("Geçersiz seçim, tekrar deneyin.")

if __name__ == "__main__":
    main_menu()