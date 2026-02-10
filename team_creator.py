import random
import os
from itertools import combinations

# --- DOSYA İŞLEMLERİ ---

def load_players(city_name):
    """Dosyadan oyuncuları yükler."""
    file_path = os.path.join(city_name.lower(), 'teams.txt')
    players = []
    if not os.path.exists(file_path):
        os.makedirs(city_name.lower(), exist_ok=True)
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
    """Oyuncuları dosyaya kaydeder."""
    file_path = os.path.join(city_name.lower(), 'teams.txt')
    with open(file_path, 'w', encoding='utf-8') as f:
        for p in players:
            f.write(f"{p['name']} {p['point']} {p['role']} {p['status']}\n")
    print("\n[+] Liste başarıyla güncellendi.")

# --- ANA FONKSİYONLAR ---

def add_player(city_name):
    print("\n--- Yeni Oyuncu Ekle ---")
    name = input("İsim: ").strip().replace(" ", "_")
    point = input("Puan (1-10): ")
    role = input("Rol (GK, DF, MF, ST): ").upper()
    status = input("Durum (O: Oynuyor, Y: Yedek): ").upper()
    
    players = load_players(city_name)
    players.append({'name': name, 'point': float(point), 'role': role, 'status': status})
    save_players(city_name, players)

def update_player(city_name):
    players = load_players(city_name)
    if not players:
        print("Güncellenecek oyuncu bulunamadı.")
        return

    name_to_find = input("\nGüncellemek istediğiniz oyuncunun adı: ").strip()
    found = False
    for p in players:
        if p['name'].lower() == name_to_find.lower():
            print(f"Mevcut Bilgiler: {p}")
            p['point'] = float(input(f"Yeni Puan ({p['point']}): ") or p['point'])
            p['role'] = input(f"Yeni Rol ({p['role']}): ").upper() or p['role']
            p['status'] = input(f"Yeni Durum ({p['status']}): ").upper() or p['status']
            found = True
            break
    
    if found:
        save_players(city_name, players)
    else:
        print("Oyuncu bulunamadı.")

# --- GÖRSELLEŞTİRME VE TAKIM KURMA ---

def create_and_show_teams(city_name):
    players = load_players(city_name)
    playing = [p for p in players if p['status'] == 'O']
    not_playing = [p for p in players if p['status'] != 'O']

    if len(playing) < 14:
        print(f"\nHata: Yetersiz oyuncu ({len(playing)}/14). Lütfen oyuncu durumlarını güncelleyin.")
        return

    match_squad = playing[:14]
    extras = playing[14:] + not_playing

    all_possible_teams = list(combinations(match_squad, 7))
    total_point = sum(p['point'] for p in match_squad)
    
    best_diff = float('inf')
    best_team1 = []

    for combo in all_possible_teams:
        t1_point = sum(p['point'] for p in combo)
        diff = abs(t1_point - (total_point - t1_point))
        if diff < best_diff:
            best_diff = diff
            best_team1 = list(combo)
            if diff == 0: break

    team2 = [p for p in match_squad if p not in best_team1]
    
    drawPitch("A TAKIMI", best_team1)
    drawPitch("B TAKIMI", team2)
    listExtras(extras)

# --- ANA MENÜ ---

def main_menu():
    city = input("Match Name (Match Folder): ").strip()
    if not city: city = "default_match"

    while True:
        print(f"\n--- {city.upper()} YÖNETİM PANELİ ---")
        print("1. Kadroları Oluştur (Sahayı Çiz)")
        print("2. Yeni Oyuncu Ekle")
        print("3. Oyuncu Bilgilerini Güncelle")
        print("4. Oyuncu Listesini Gör")
        print("5. Şehir Değiştir")
        print("0. Çıkış")
        
        choice = input("\nSeçiminiz: ")

        if choice == '1':
            create_and_show_teams(city)
        elif choice == '2':
            add_player(city)
        elif choice == '3':
            update_player(city)
        elif choice == '4':
            players = load_players(city)
            for p in players: print(f"{p['name']} - {p['role']} - {p['point']} - {p['status']}")
        elif choice == '5':
            city = input("Yeni Match Name: ").strip()
        elif choice == '0':
            print("Görüşürüz!")
            break
        else:
            print("Geçersiz seçim.")

if __name__ == "__main__":
    main_menu()