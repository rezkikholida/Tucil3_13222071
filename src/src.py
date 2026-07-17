from typing import NamedTuple
import heapq
import time

def read_input(filepath):
    f = open(filepath)
    lines = f.readlines()
    f.close()

    # Baris pertama jadikan integer
    baris_pertama = lines[0].split()
    N = int(baris_pertama[0])
    M = int(baris_pertama[1])

    # Baca N baris berikutnya (grid karakter)
    grid = []
    for i in range(1, N + 1):
        baris = lines[i].strip() 
        row = list(baris)         
        grid.append(row)
    
    # Baca N baris berikutnya (grid cost)
    cost_grid = []
    for i in range(N + 1, 2 * N + 1):
        baris = lines[i].strip()
        angka_angka = baris.split()          
        row = [int(x) for x in angka_angka] 
        cost_grid.append(row)
    
    # Cari posisi Z, O, dan angka-angka dengan loop seluruh grid
    start   = None  # akan diisi (baris, kolom) posisi Z
    goal    = None  # akan diisi (baris, kolom) posisi O
    numbers = {}    # akan diisi {angka: (baris, kolom)}

    for r in range(N):
        for c in range(M):
            karakter = grid[r][c]
            if karakter == 'Z':
                start = (r, c)
            elif karakter == 'O':
                goal = (r, c)
            elif karakter.isdigit():
                numbers[int(karakter)] = (r, c)
    total_nums = len(numbers)  # banyak angka di peta
    return N, M, grid, cost_grid, start, goal, numbers, total_nums

class State(NamedTuple):
    row: int       # posisi baris aktor sekarang
    col: int       # posisi kolom aktor sekarang
    next_num: int  # angka berikutnya yang harus diinjak

# Arah gerak sebagai (dr, dc)
atas   = (-1,  0)
bawah  = ( 1,  0)
kiri   = ( 0, -1)
kanan  = ( 0,  1)

def slide(grid, cost_grid, state, direction):
    N = len(grid)
    M = len(grid[0])
    dr, dc = direction
    r        = state.row
    c        = state.col
    next_num = state.next_num
    total_cost = 0
    while True:
        # Hitung posisi satu langkah ke depan
        r_baru = r + dr
        c_baru = c + dc

        # Game over jika keluar batas papan
        if r_baru < 0 or r_baru >= N or c_baru < 0 or c_baru >= M:
            return None
        
        tile = grid[r_baru][c_baru]
        # Jika dinding (X), berhenti di posisi sebelum ini
        if tile == 'X':
            if r == state.row and c == state.col:
                return None
            state_baru = State(row=r, col=c, next_num=next_num)
            return state_baru, total_cost
        # Jika lava (L), game over
        if tile == 'L':
            return None
        # Kalau angka
        if tile.isdigit():
            angka = int(tile)
            if angka == next_num:
                next_num += 1      # angka berhasil diambil, lanjut slide
            elif angka > next_num:
                return None        # urutan dilanggar, game over
            # kalau angka < next_num → sudah pernah diambil, anggap tile biasa, lanjut
        # Tambahkan cost tile yang baru diinjak
        total_cost += cost_grid[r_baru][c_baru]
        # Pindah ke posisi baru, lanjut loop
        r = r_baru
        c = c_baru

def ucs(grid, cost_grid, start, goal, total_nums):
    state_awal = State(row=start[0], col=start[1], next_num=0)
    # Priority queue isinya tuple (g_cost, state, moves_string)
    # heapq selalu pop yang g_cost-nya paling kecil duluan
    pq = []
    heapq.heappush(pq, (0, state_awal, ""))

    # visited: key = state, value = g_cost terkecil yang pernah nyampe ke state itu
    visited = {}
    iterasi = 0
    while pq:
        g_cost, state, moves = heapq.heappop(pq)
        iterasi += 1

        # Cek goal: posisi di O dan semua angka sudah diambil
        if state.row == goal[0] and state.col == goal[1] and state.next_num == total_nums:
            return moves, g_cost, iterasi
        
        # Kalau state ini sudah pernah dikunjungi dengan cost lebih murah, skip
        if state in visited and visited[state] <= g_cost:
            continue

        # Tandai state ini sudah dikunjungi dengan cost ini
        visited[state] = g_cost

        # Expand ke 4 arah
        for nama_arah, arah in [("U", atas), ("D", bawah), ("L", kiri), ("R", kanan)]:
            hasil = slide(grid, cost_grid, state, arah)
            if hasil is None:
                continue   # arah ini invalid, skip
            state_baru, move_cost = hasil
            g_cost_baru = g_cost + move_cost
            # Kalau state baru belum pernah dikunjungi, atau ketemu jalur lebih murah
            if state_baru not in visited or visited[state_baru] > g_cost_baru:
                heapq.heappush(pq, (g_cost_baru, state_baru, moves + nama_arah))

    # Heap kosong, tidak ada solusi
    return None, 0, iterasi

def heuristic(state, goal, numbers, total_nums):
    # Tentukan target dulu: posisi angka berikutnya, atau goal kalau semua sudah diambil
    if state.next_num < total_nums:
        target = numbers[state.next_num]
    else:
        target = goal
    # Manhattan distance dari posisi sekarang ke target
    return abs(state.row - target[0]) + abs(state.col - target[1])

def gbfs(grid, cost_grid, start, goal, numbers, total_nums):
    state_awal = State(row=start[0], col=start[1], next_num=0)
    # Priority queue isinya tuple (h_cost, state, moves_string)
    # GBFS hanya pakai h(n) — estimasi jarak ke goal, tanpa memperhitungkan cost sejauh ini
    pq = []
    h_awal = heuristic(state_awal, goal, numbers, total_nums)
    heapq.heappush(pq, (h_awal, state_awal, ""))
    visited = {}
    iterasi = 0
    while pq:
        h_cost, state, moves = heapq.heappop(pq)
        iterasi += 1
        # Cek goal
        if state.row == goal[0] and state.col == goal[1] and state.next_num == total_nums:
            # GBFS tidak tracking g_cost, jadi hitung ulang total cost dari moves
            total_cost = hitung_total_cost(grid, cost_grid, start, moves)
            return moves, total_cost, iterasi
        if state in visited:
            continue

        visited[state] = True

        for nama_arah, arah in [("U", atas), ("D", bawah), ("L", kiri), ("R", kanan)]:
            hasil = slide(grid, cost_grid, state, arah)
            if hasil is None:
                continue

            state_baru, move_cost = hasil

            if state_baru not in visited:
                h_baru = heuristic(state_baru, goal, numbers, total_nums)
                heapq.heappush(pq, (h_baru, state_baru, moves + nama_arah))
    return None, 0, iterasi

def astar(grid, cost_grid, start, goal, numbers, total_nums):
    state_awal = State(row=start[0], col=start[1], next_num=0)
    # Priority queue isinya tuple (f_cost, state, g_cost, moves_string)
    # A* pakai f(n) = g(n) + h(n) sebagai prioritas
    pq = []
    h_awal = heuristic(state_awal, goal, numbers, total_nums)
    f_awal = 0 + h_awal   # g=0 di awal
    heapq.heappush(pq, (f_awal, state_awal, 0, ""))

    # visited: key = state, value = g_cost terkecil (sama seperti UCS)
    visited = {}
    iterasi = 0

    while pq:
        f_cost, state, g_cost, moves = heapq.heappop(pq)
        iterasi += 1

        # Cek goal
        if state.row == goal[0] and state.col == goal[1] and state.next_num == total_nums:
            return moves, g_cost, iterasi
        
        if state in visited and visited[state] <= g_cost:
            continue

        visited[state] = g_cost

        for nama_arah, arah in [("U", atas), ("D", bawah), ("L", kiri), ("R", kanan)]:
            hasil = slide(grid, cost_grid, state, arah)
            if hasil is None:
                continue
            state_baru, move_cost = hasil
            g_baru = g_cost + move_cost
            h_baru = heuristic(state_baru, goal, numbers, total_nums)
            f_baru = g_baru + h_baru
            if state_baru not in visited or visited[state_baru] > g_baru:
                heapq.heappush(pq, (f_baru, state_baru, g_baru, moves + nama_arah))
 
    return None, 0, iterasi

def hitung_total_cost(grid, cost_grid, start, moves):
    """Bantu GBFS: hitung ulang total cost dari string moves."""
    arah_map = {"U": atas, "D": bawah, "L": kiri, "R": kanan}
    state = State(row=start[0], col=start[1], next_num=0)
    total = 0
    for m in moves:
        hasil = slide(grid, cost_grid, state, arah_map[m])
        if hasil is None:
            break
        state, move_cost = hasil
        total += move_cost
    return total

if __name__ == '__main__':
 
    # Input dari user
    nama_file = input(">> Masukan file input: ")
    N, M, grid, cost_grid, start, goal, numbers, total_nums = read_input(nama_file)
    
    print(f"\nUkuran papan : {N} baris x {M} kolom")
    print(f"Start (Z)    : baris {start[0]}, kolom {start[1]}")
    print(f"Goal  (O)    : baris {goal[0]}, kolom {goal[1]}")
    print(f"Angka di peta: {numbers}")

    print("\n--- Grid ---")
    for row in grid:
        print(''.join(row))

    algoritma = input("\n>> Algoritma apa yang anda pilih? (UCS/GBFS/A*): ")
    algoritma = algoritma.upper()   # biar "ucs" dan "UCS" sama-sama diterima

    # Jalankan algoritma — timer hanya membungkus bagian ini,
    # tidak termasuk baca file atau tampilkan output
    if algoritma == "UCS":
        t_mulai = time.time()
        moves, total_cost, iterasi = ucs(grid, cost_grid, start, goal, total_nums)
        t_selesai = time.time()

    elif algoritma == "GBFS":
        t_mulai = time.time()
        moves, total_cost, iterasi = gbfs(grid, cost_grid, start, goal, numbers, total_nums)
        t_selesai = time.time()

    elif algoritma == "A*":
        t_mulai = time.time()
        moves, total_cost, iterasi = astar(grid, cost_grid, start, goal, numbers, total_nums)
        t_selesai = time.time()

    else:
        print(f"Algoritma '{algoritma}' tidak dikenal. Pilih UCS, GBFS, atau A*.")
        exit()   # berhenti di sini — moves/total_cost/iterasi belum terdefinisi

    waktu_ms = (t_selesai - t_mulai) * 1000

    # Tampilkan output solusi
    print()
    if moves is None:
        print("Tidak ada solusi!")
    else:
        print(f">> Solusi       : {moves}")
        print(f">> Total cost   : {total_cost}")
    print(f">> Waktu eksekusi: {waktu_ms:.2f} ms")
    print(f">> Banyak iterasi yang dilakukan: {iterasi} iterasi")

    if moves is None:
        exit()

    # Playback
    jawab_playback = input("\n>> Apakah Anda ingin melakukan playback? (Ya/Tidak): ")

    if jawab_playback.strip().lower() in ("ya", "y"):
        step_minta = input(f">> Pada step berapa anda ingin melakukan playback (0-{len(moves)}): ")
        step_minta = int(step_minta)

        # Bangun list snapshot: replay ulang moves satu per satu
        arah_map = {"U": atas, "D": bawah, "L": kiri, "R": kanan}
        snapshots = []

        state_sekarang = State(row=start[0], col=start[1], next_num=0)
        snapshots.append((0, "-", state_sekarang))   # step 0 = posisi awal

        for i, m in enumerate(moves):
            hasil = slide(grid, cost_grid, state_sekarang, arah_map[m])
            state_sekarang, _ = hasil
            snapshots.append((i + 1, m, state_sekarang))   # step 1, 2, 3, ...

        # Fungsi bantu: gambar grid dengan posisi aktor ditandai @
        def gambar_grid(grid, state):
            for r in range(len(grid)):
                baris = ""
                for c in range(len(grid[0])):
                    if r == state.row and c == state.col:
                        baris += "@"
                    else:
                        baris += grid[r][c]
                print(baris)

        # Mulai dari step yang diminta, bisa navigasi n/p/q
        idx = step_minta
        print("\nPerintah: [n] next  [p] prev  [q] keluar\n")

        while True:
            step, move, state = snapshots[idx]
            print(f"\n[Step {step}/{len(moves)}] Move: {move}  |  Posisi: ({state.row}, {state.col})  |  Next angka: {state.next_num}")
            gambar_grid(grid, state)
            cmd = input("\n[n/p/q] > ").strip().lower()
            if cmd == "n" and idx < len(snapshots) - 1:
                idx += 1
            elif cmd == "p" and idx > 0:
                idx -= 1
            elif cmd == "q":
                break

    # Simpan solusi ke file
    jawab_simpan = input("\n>> Apakah Anda ingin menyimpan solusi? (Ya/Tidak): ")

    if jawab_simpan.strip().lower() in ("ya", "y"):
        path_simpan = input(">> Solusi disimpan pada: ")
        f_out = open(path_simpan, "w")
        f_out.write(f"File input : {nama_file}\n")
        f_out.write(f"Algoritma  : {algoritma}\n")
        f_out.write(f"Solusi     : {moves}\n")
        f_out.write(f"Total cost : {total_cost}\n")
        f_out.write(f"Waktu eksekusi: {waktu_ms:.2f} ms\n")
        f_out.write(f"Banyak iterasi yang dilakukan: {iterasi} iterasi\n")
        f_out.close()
        print(f">> Solusi disimpan pada {path_simpan}")