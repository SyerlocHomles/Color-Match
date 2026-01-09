import streamlit as st
import random

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Colour Match Master", layout="centered")

# --- 2. CSS CUSTOM ---
st.markdown("""
<style>
    #MainMenu, footer, header {visibility: hidden;}
    .title-text {text-align: center; font-size: 32px; font-weight: bold; color: white; margin-bottom: 10px;}
    .stButton > button {border: 2px solid #555 !important; border-radius: 10px !important; height: 60px !important; width: 100% !important;}
    .feedback-box {background-color: #1e1e1e; padding: 10px; border-radius: 8px; margin-bottom: 10px; border-left: 5px solid #FFA500;}
    .feedback-text {font-weight: bold; color: #FFA500; font-size: 14px; margin: 0;}
</style>
""", unsafe_allow_html=True)

# --- 3. LOGIKA UTAMA (FEEDBACK PRESISI) ---
WARNA_LIST = ["Merah", "Oren", "Kuning", "Hijau", "Biru"]
WARNA_HEX = {"Kosong": "#333333", "Merah": "#FF0000", "Oren": "#FFA500", "Kuning": "#FFFF00", "Hijau": "#00FF00", "Biru": "#0000FF"}

if 'game_active' not in st.session_state:
    st.session_state.game_active = False
    st.session_state.history = []

def start_game(mode):
    # Logika Level sesuai permintaan
    if mode == "Mudah": k, w_count = 3, 3
    elif mode == "Sedang": k, w_count = 4, 4
    else: k, w_count = 5, 5
    
    # Ambil pool warna acak dari 5 pilihan yang ada
    pool = random.sample(WARNA_LIST, w_count)
    # Tentukan target jawaban rahasia
    st.session_state.target = [random.choice(pool) for _ in range(k)]
    st.session_state.pool = pool
    st.session_state.max_k = k
    st.session_state.guesses = ["Kosong"] * k
    st.session_state.history = []
    st.session_state.game_active = True

def hitung_feedback(guess, target):
    t_temp = list(target)
    g_temp = list(guess)
    benar_posisi = 0
    salah_posisi = 0
    
    # LANGKAH 1: Cek Benar Posisi (Warna & Letak PAS)
    for i in range(len(t_temp)):
        if g_temp[i] == t_temp[i]:
            benar_posisi += 1
            t_temp[i] = "MARK_T" # Tandai target sudah terpakai
            g_temp[i] = "MARK_G" # Tandai tebakan sudah terhitung
            
    # LANGKAH 2: Cek Salah Posisi (Warna ada, tapi posisi beda)
    for i in range(len(g_temp)):
        if g_temp[i] != "MARK_G": # Hanya cek yang belum dapet poin Benar Posisi
            if g_temp[i] in t_temp:
                salah_posisi += 1
                t_temp[t_temp.index(g_temp[i])] = "MARK_T" # Buang satu warna dari target
                
    salah_warna = len(target) - (benar_posisi + salah_posisi)
    return f"{benar_posisi} warna benar, {salah_posisi} warna salah posisi, {salah_warna} warna salah"

# --- 4. TAMPILAN ANTARMUKA ---
st.markdown('<div class="title-text">COLOUR MATCH</div>', unsafe_allow_html=True)

if not st.session_state.game_active:
    st.write("### Pilih Tingkat Kesulitan:")
    # Pakai columns untuk pilihan level agar tidak duplikasi ID
    c1, c2, c3 = st.columns(3)
    if c1.button("Mudah"): start_game("Mudah")
    if c2.button("Sedang"): start_game("Sedang")
    if c3.button("Sulit"): start_game("Sulit")
else:
    # Sidebar untuk reset
    if st.sidebar.button("Ganti Level / Reset"):
        st.session_state.game_active = False
        st.rerun()

    # Hint warna yang aktif di level ini
    st.write(f"Warna yang mungkin muncul ({st.session_state.max_k} kartu):")
    h_cols = st.columns(len(st.session_state.pool))
    for idx, h in enumerate(st.session_state.pool):
        h_cols[idx].markdown(f"<div style='background-color:{WARNA_HEX[h]}; height:20px; border:1px solid white;'></div>", unsafe_allow_html=True)

    st.write("---")

    # Slot Kartu (Klik untuk ganti warna)
    cols = st.columns(st.session_state.max_k)
    for i in range(st.session_state.max_k):
        with cols[i]:
            # Paki key unik 'slot_' + index agar tidak error duplicate ID
            if st.button("🔄", key=f"slot_{i}"):
                cur = st.session_state.guesses[i]
                pool = st.session_state.pool
                next_idx = (pool.index(cur) + 1) % len(pool) if cur in pool else 0
                st.session_state.guesses[i] = pool[next_idx]
            
            # Visual warna
            st.markdown(f"<div style='background-color:{WARNA_HEX[st.session_state.guesses[i]]}; height:80px; border-radius:10px; border:2px solid #555;'></div>", unsafe_allow_html=True)

    st.write("")
    # Tombol OK dengan Key Unik
    if st.button("OK ✅", key="main_ok_btn", use_container_width=True):
        if "Kosong" not in st.session_state.guesses:
            teks = hitung_feedback(st.session_state.guesses, st.session_state.target)
            st.session_state.history.append({'g': list(st.session_state.guesses), 'f': teks})
            
            if st.session_state.guesses == st.session_state.target:
                st.balloons()
                st.success("JACKPOT! Kamu Menang!")

    # --- 5. RIWAYAT KALIMAT ---
    if st.session_state.history:
        st.write("### Riwayat:")
        for h in reversed(st.session_state.history):
            st.markdown(f"""
                <div class="feedback-box">
                    <p class="feedback-text">{h['f']}</p>
                </div>
            """, unsafe_allow_html=True)
            # Menampilkan baris kartu kecil
            card_row = "".join([f'<div style="display:inline-block; width:20px; height:30px; background-color:{WARNA_HEX[c]}; margin-right:5px; border:1px solid white;"></div>' for c in h['g']])
            st.markdown(card_row, unsafe_allow_html=True)
            st.write("")
