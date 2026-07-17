# Tucil3 — Ice Sliding Puzzle Solver

## Deskripsi
Program ini merupakan implementasi algoritma *Pathfinding* (Uniform Cost Search, Greedy Best First Search, dan A*) untuk menyelesaikan permainan **Ice Sliding Puzzle**. Dalam permainan ini, pemain menggerakkan aktor dari titik awal menuju titik keluar di atas permukaan es yang licin — aktor tidak akan berhenti bergerak sampai menabrak dinding atau rintangan. Permainan ini juga memiliki modifikasi berupa petak angka berurutan (0, 1, 2, ...) yang wajib dilalui aktor sesuai urutannya sebelum mencapai titik keluar. Program membaca konfigurasi papan dari berkas `.txt`, mencari solusi menggunakan salah satu algoritma pathfinding yang dipilih pengguna, lalu menampilkan langkah solusi, total cost, jumlah iterasi pencarian, waktu eksekusi, serta playback visualisasi langkah demi langkah di terminal.

## Requirement
- Python 3.10 atau lebih baru (menggunakan modul `typing.NamedTuple`, `heapq`, dan `time` yang merupakan bagian dari standar pustaka Python, tanpa instalasi tambahan)

## Cara Kompilasi
Python adalah bahasa *interpreted*, sehingga tidak memerlukan proses kompilasi terpisah sebelum dijalankan.

## Cara Menjalankan
1. Buka Terminal atau Command Prompt.
2. Arahkan direktori (menggunakan perintah `cd`) ke dalam folder `src`.
3. Jalankan perintah berikut:
   \```
   python main.py
   \```
4. Program akan meminta input nama/path berkas `.txt` yang berisi konfigurasi papan, contoh:
   \```
   >> Masukan file input: ../test/test1_kecil.txt
   \```
5. Program akan menampilkan ukuran papan, posisi start (Z), posisi goal (O), serta visualisasi papan awal.
6. Program akan meminta pemilihan algoritma pathfinding:
   \```
   >> Algoritma apa yang anda pilih? (UCS/GBFS/A*): 
   \```
7. Program menampilkan solusi (urutan gerakan U/D/L/R), total cost, waktu eksekusi (ms), dan jumlah iterasi.
8. Program akan menanyakan apakah ingin melakukan **playback** — jika ya, pengguna dapat memilih step awal playback dan bernavigasi menggunakan:
   - `n` : maju satu step
   - `p` : mundur satu step
   - `q` : keluar dari mode playback
9. Program akan menanyakan apakah solusi ingin disimpan ke berkas `.txt`, contoh:
   \```
   >> Solusi disimpan pada: solusi.txt
   \```

## Format Berkas Input
Baris pertama berisi dua bilangan `N M` (ukuran papan). N baris berikutnya merepresentasikan denah papan, dan N baris setelahnya merepresentasikan cost setiap petak. Simbol yang digunakan:
- `*` : petak yang bisa dilewati
- `X` : rintangan/dinding, aktor berhenti tepat sebelum petak ini
- `L` : lava, menyebabkan game over jika dilewati
- `Z` : posisi awal aktor
- `O` : titik tujuan
- `0`–`9` : petak angka yang wajib dilalui sesuai urutan

## Author
Kholida Rezki Khoiriah (13222071)
