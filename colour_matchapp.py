import streamlit as st
import random

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Colour Match Master", layout="centered")

# --- 2. CSS CUSTOM ---
st.markdown("""
<style>
    #MainMenu, footer, header {visibility: hidden;}
    .title-text {text-align: center; font-size: 30px; font-weight: bold; color: white; margin-bottom: 20px;}
    .stButton > button {border: 2px solid #555 !important; border-radius: 10px !important; height: 75px !important; width: 100% !important;}
    .feedback-text {font-weight: bold; color: #FFA500; font-size: 14px;}
    .history-container {background-color: #262730; padding: 15px; border-radius: 10px; margin-top: 20px;}
</style>
""", unsafe_allow_html=True)

# --- 3. LOGIKA GAME ---
WARNA_LIST = ["Merah", "Oren", "Kuning", "Hijau", "Biru"]
WARNA_HEX = {"Kosong": "#333333", "Merah": "#FF0000", "Oren": "#FFA500", "Kuning": "#FFFF00", "Hijau": "#00FF00", "Biru": "#0000FF"}

# Inisialisasi awal
if 'game_active' not in st.session_state:
    st.session_state.game_active = False
    st.session_state.history = []

# Fungsi untuk memulai game baru berdasarkan level
def start_game(mode):
    if mode == "Mudah":
        k, w_count = 3, 3
    elif mode == "Sedang":
        k, w_count = 4, 4
    else: # Sulit
        k, w_count = 5, 5
    
    # Ambil warna acak dari 5 warna yang tersedia
    pool_warna = random.sample(WARNA_LIST, w_count)
    st.session_state.target = [random.choice(pool_warna) for _ in range(k)]
    st.session_state.max_k = k
    st.session_state.pool = pool_warna
    st.session_state.guesses = ["Kosong"] * k
    st.session_state.history = []
    st.session_state.game_active = True

def ganti_warna(i):
    cur = st.session_state.guesses[i]
    # Hanya berputar di warna yang ada dalam pool level tersebut
    pool = st.session_state.pool
    idx = (pool.index(cur) + 1) % len(pool) if cur in pool else 0
    st.session_state.guesses[i] = pool[idx]

def hitung_feedback(guess, target):
    # Pastikan kita membandingkan list dengan panjang yang sama
    t_temp = list(target)
    g_temp = list(guess)
    
    benar_posisi = 0
    salah_posisi = 0
    
    # LANGKAH 1: Cek Benar Posisi (Warna & Letak Sama)
    for i in range(len(t_temp)):
        if g_temp[i] == t_temp[i]:
            benar_posisi += 1
            t_temp[i] = "DONE_T" # Tandai agar tidak dihitung lagi
            g_temp[i] = "DONE_G"
            
    # LANGKAH 2: Cek Salah Posisi (Warna Ada di Target tapi beda letak)
    for i in range(len(g_temp)):
        if g_temp[i] != "DONE_G": # Hanya cek yang belum dapat poin Benar Posisi
            if g_temp[i] in t_temp:
                salah_posisi += 1
                # Hapus satu warna yang cocok dari target temp agar tidak double hitung
                t_temp[t_temp.index(g_temp[i])] = "DONE_T"
                
    # LANGKAH 3: Sisa kartu adalah Salah Warna
    salah_warna = len(target) - (benar_posisi + salah_posisi)
    
    return f"{benar_posisi} warna benar, {salah_posisi} warna salah posisi, {salah_warna} warna salah"

# --- BAGIAN TOMBOL OK (Update Logika Rerun) ---
if st.button("OK", use_container_width=True):
    if "Kosong" not in st.session_state.guesses:
        # PENTING: Gunakan slice [:] agar tidak merusak data asli saat pengecekan
        hasil_teks = hitung_feedback(st.session_state.guesses[:st.session_state.max_k], st.session_state.target)
        
        st.session_state.history.append({
            'g': list(st.session_state.guesses[:st.session_state.max_k]), 
            'f': hasil_teks
        })
        
        # Cek Kemenangan
        if st.session_state.guesses[:st.session_state.max_k] == st.session_state.target:
            st.balloons()
            st.success("JACKPOT! Semua Benar!")

# --- 4. TAMPILAN ---
st.markdown('<div class="title-text">COLOUR MATCH</div>', unsafe_allow_html=True)

# Pilihan Level (Hanya muncul jika game belum mulai atau ingin reset)
if not st.session_state.game_active:
    st.write("### Pilih Tingkat Kesulitan:")
    col_l1, col_l2, col_l3 = st.columns(3)
    if col_l1.button("Mudah (3 Kartu)"): start_game("Mudah")
    if col_l2.button("Sedang (4 Kartu)"): start_game("Sedang")
    if col_l3.button("Sulit (5 Kartu)"): start_game("Sulit")
else:
    # Tombol Reset/Ganti Level
    if st.sidebar.button("Ganti Level"):
        st.session_state.game_active = False
        st.rerun()

    # Hints Warna yang ada di pool level ini
    st.write(f"Warna yang mungkin muncul ({st.session_state.max_k} kartu):")
    h_cols = st.columns(len(st.session_state.pool))
    for idx, h in enumerate(st.session_state.pool):
        h_cols[idx].markdown(f"<div style='background-color:{WARNA_HEX[h]}; height:18px; border:1px solid white;'></div>", unsafe_allow_html=True)

    st.write("---")

    # Tombol Tebakan
    cols = st.columns(st.session_state.max_k)
    for i in range(st.session_state.max_k):
        with cols[i]:
            st.button(" ", key=f"b{i}", on_click=ganti_warna, args=(i,), use_container_width=True)
            st.markdown(f"<div style='background-color:{WARNA_HEX[st.session_state.guesses[i]]}; height:10px; border-radius:5px;'></div>", unsafe_allow_html=True)

    st.write("")
    if st.button("OK", use_container_width=True):
        if "Kosong" not in st.session_state.guesses:
            teks_hasil = hitung_feedback(st.session_state.guesses, st.session_state.target)
            st.session_state.history.append({'g': list(st.session_state.guesses), 'f': teks_hasil})
            
            if st.session_state.guesses == st.session_state.target:
                st.balloons()
                st.success("Kamu Berhasil Menebak Semua!")
                # Game akan tetap aktif agar bisa melihat riwayat, atau bisa reset otomatis

    # --- 5. RIWAYAT (SISTEM KALIMAT) ---
    if st.session_state.history:
        st.write("### Riwayat:")
        for h in reversed(st.session_state.history):
            with st.container():
                st.markdown(f'<p class="feedback-text">{h["f"]}</p>', unsafe_allow_html=True)
                # Menampilkan barisan kartu tebakan secara kecil
                h_cards = "".join([f'<div style="display:inline-block; width:15px; height:20px; background-color:{WARNA_HEX[c]}; margin-right:5px; border:1px solid white;"></div>' for c in h['g']])
                st.markdown(h_cards, unsafe_allow_html=True)
                st.write("---")
