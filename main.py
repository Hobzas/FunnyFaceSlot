import random

# Aktuální data ze slot.html
SYMS = {1: "7", 2: "Bell", 3: "Melon", 4: "Plum", 5: "Orange", 6: "Lemon", 7: "Cherry", 8: "Star", 9: "Joker"}
WILD = 9

# Upravená výplatní tabulka pro RTP ~75%
LINE_PAY = {
    1: [0, 0, 50, 150, 300], # Sedmičky
    2: [0, 0, 25, 75, 150],  # Zvony
    3: [0, 0, 25, 75, 150],  # Melouny
    4: [0, 0, 10, 25, 50],   # Švestky
    5: [0, 0, 10, 25, 50],   # Pomeranče
    6: [0, 0, 10, 25, 50],   # Citrony
    7: [0, 0, 10, 25, 50]    # Třešně
}

BET_LINES = [
    [1,1,1,1,1],[0,0,0,0,0],[2,2,2,2,2],[0,1,2,1,0],[2,1,0,1,2],
    [0,0,1,2,2],[2,2,1,0,0],[1,0,1,2,1],[1,2,1,0,1],[1,0,0,0,1]
]

REELS = [
    [5,8,7,2,4,7,3,9,4,5,2,4,6,1,3,6,4,2,5,6,1,5,4,3,7,2,3,1,6,7,1,6,5,7,1],
    [5,6,4,5,6,1,4,3,6,2,4,1,7,9,4,3,7,2,6,7,3,2,5,6,7,5,1,4,8,2,7,5,1,3],
    [7,5,4,3,5,6,1,4,6,3,1,8,6,2,7,1,2,7,5,4,2,5,3,7,2,3,1,9,4,6],
    [4,5,2,1,3,7,1,4,6,2,1,7,4,5,2,9,6,3,7,5,1,6,4,3,7,4,5,6,3,2,6,8,5,7],
    [5,2,3,6,4,3,7,4,3,2,1,4,5,7,1,6,7,5,3,4,2,6,8,5,6,1,7,2,9,1,5,6,1,7,4]
]

def simulate_spin(total_bet):
    # Náhodné zastavení válců a vytvoření viditelné plochy 5x3
    screen = []
    for reel in REELS:
        stop = random.randint(0, len(reel) - 1)
        # Vezmeme 3 symboly za sebou (cyklicky)
        column = [reel[(stop + i) % len(reel)] for i in range(3)]
        screen.append(column)

    total_win = 0
    bet_per_line = total_bet / 10 # Hra má fixně 10 linií
    
    for line in BET_LINES:
        # První symbol na linii
        active_sym = screen[0][line[0]]
        
        # Logika Wild (Joker) na začátku linie
        if active_sym == WILD:
            for x in range(1, 5):
                if screen[x][line[x]] != WILD:
                    active_sym = screen[x][line[x]]
                    break
        
        # Počítání shod zleva doprava
        matches = 1
        for x in range(1, 5):
            if screen[x][line[x]] == active_sym or screen[x][line[x]] == WILD:
                matches += 1
            else:
                break
        
        # Pokud je celá řada WILD, bere se to jako symbol s ID 1 (Sedmičky)
        pay_sym = 1 if active_sym == WILD else active_sym
        
        # Výpočet výhry podle tabulky
        if pay_sym in LINE_PAY:
            total_win += LINE_PAY[pay_sym][matches-1] * bet_per_line
            
    return total_win

def run_simulation(iterations=1000000):
    bet_per_spin = 10
    total_wagered = iterations * bet_per_spin
    total_returned = 0
    
    print(f"Spouštím simulaci {iterations} otáček pro RTP 75%...")
    
    for i in range(iterations):
        total_returned += simulate_spin(bet_per_spin)
        
        # Průběžný indikátor pro dlouhé simulace
        if i % 250000 == 0 and i > 0:
            current_rtp = (total_returned / (i * bet_per_spin)) * 100
            print(f"  Provedeno {i} otáček... (aktuální RTP: {current_rtp:.2f}%)")

    final_rtp = (total_returned / total_wagered) * 100
    
    print("\n" + "="*30)
    print(f"VÝSLEDEK ANALÝZY")
    print("="*30)
    print(f"Celkem vsazeno:  {total_wagered:,} kr.")
    print(f"Celkem vyhráno:  {total_returned:,.2f} kr.")
    print(f"VÝSLEDNÉ RTP:    {final_rtp:.2f} %")
    print("="*30)

if __name__ == "__main__":
    run_simulation()