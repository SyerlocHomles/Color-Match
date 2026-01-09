import streamlit as st
import random

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Colour Match Master", layout="centered")

# --- 2. CSS CUSTOM (STABILISASI TOMBOL & FONT) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee+Shade&family=Space+Mono:wght@400;700&display=swap');

    #MainMenu, footer, header {visibility: hidden;}
    
    .title-text {
        text-align: center; 
        font-family: 'Bungee Shade', cursive; 
        font-size: 35px; 
        color: white; 
        margin-bottom: 20px;
    }

    .desc-text {
        font-family: 'Space Mono', monospace;
        color: white;
        background-color: rgba(255, 255, 255, 0.1);
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #555;
        margin-bottom: 20px;
        font-size: 14px;
        line-height: 1.5;
    }

    /* Styling tombol level agar terlihat jelas */
    .stButton > button {
        border-radius: 10px !important;
        font-weight: bold !important;
        height: 50px !important;
    }

    /* Khusus untuk tombol kartu di dalam game */
    .game-card-btn > div > button {
        position: absolute;
        top: 0;
        left: 0;
        height: 120px !important;
        width: 100% !important;
        background-color: transparent !important;
        border: none !important;
        color: transparent !important;
        z-index: 10;
    }

    .card-slot {
        height: 120px;
        width: 100%;
        border-radius: 12px;
        border: 2px solid #555;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. FUNGSI LOGIKA ---
WARNA_LIST = ["Merah", "Oren", "Kuning", "Hijau", "Biru"]
WARNA_HEX = {"Kosong": "#333333", "Merah": "#FF0000", "Oren": "#FFA500", "Kuning": "#FFFF00", "Hijau": "#00FF00", "Biru": "#0000FF"}

if 'game_active' not in st.session_state:
    st.session_state.game_active = False
    st.session_state.history = []

def start_game(mode):
    if mode == "Mudah": k, w_count = 3, 3
    elif mode == "Sedang": k, w_count = 4, 4
    else: k, w_count = 5, 5
    
    pool = random.sample(WARNA_LIST, w_count)
    st.session_state.target = [random.choice(pool) for _ in range(k)]
    st.session_state.pool = pool
    st.session_state.max_k = k
    st.session_state.guesses = ["Kosong"] * k
    st.session_state.history = []
    st.session_state.game_active = True

def ganti_warna(i):
    cur = st.session_state.guesses[i]
    pool = st.session_state.pool
    next_idx = (pool.index(cur) + 1) % len(pool) if cur in pool else 0
    st.session_state.guesses[i] = pool[next_idx]

def hitung_feedback(guess, target):
    t_temp, g_temp = list(target), list(guess)
    b, s = 0, 0
    for i in range(len(t_temp)):
        if g_temp[i] == t_temp[i]:
            b += 1
            t_temp[i], g_temp[i] = "DONE_T", "DONE_G"
    for i in range(len(g_temp)):
        if g_temp[i] != "DONE_G" and g_temp[i] in t_temp:
            s += 1
            t_temp[t_temp.index(g_temp[i])] = "DONE_T"
    return f"{b} warna benar, {s} salah posisi, {len(target)-(b+s)} salah"

# --- 4. TAMPILAN ---
st.markdown('<div class="title-text">COLOUR MATCH</div>', unsafe_allow_html=True)

if not st.session_state.game_active:
    # Deskripsi Cara Bermain
    st.markdown("""
    <div class="desc-text">
        <strong>🎯 CARA BERMAIN:</strong><br>
        1. Pilih level di bawah untuk memulai.<br>
        2. Klik kotak kartu untuk ganti warna.<br>
        3. Tebak kombinasi warna rahasia.<br>
        4. Gunakan feedback riwayat untuk menang!
    </div>
    """, unsafe_allow_html=True)

    st.write("### 🕹️ PILIH TINGKAT KESULITAN:")
    
    # Tombol dibuat satu-satu tanpa kolom agar tidak tertutup CSS transparan
    if st.button("🟢 MUDAH (3 KARTU)", use_container_width=True, key="m_btn"):
        start_game("Mudah")
        st.rerun()
    if st.button("🟡 SEDANG (4 KARTU)", use_container_width=True, key="s_btn"):
        start_game("Sedang")
        st.rerun()
    if st.button("🔴 SULIT (5 KARTU)", use_container_width=True, key="sl_btn"):
        start_game("Sulit")
        st.rerun()
else:
    if st.sidebar.button("🔙 GANTI LEVEL"):
        st.session_state.game_active = False
        st.rerun()

    st.write(f"**Warna mungkin muncul:**")
    h_cols = st.columns(len(st.session_state.pool))
    for idx, h in enumerate(st.session_state.pool):
        h_cols[idx].markdown(f"<div style='background-color:{WARNA_HEX[h]}; height:15px; border:1px solid white;'></div>", unsafe_allow_html=True)

    st.write("---")

    # KARTU GAME (Hanya di sini CSS transparan bekerja)
    cols = st.columns(st.session_state.max_k)
    for i in range(st.session_state.max_k):
        with cols[i]:
            current_color = WARNA_HEX[st.session_state.guesses[i]]
            st.markdown(f'<div class="card-slot" style="background-color:{current_color};"></div>', unsafe_allow_html=True)
            # Menggunakan class khusus agar tidak merusak tombol level di depan
            st.markdown('<div class="game-card-btn">', unsafe_allow_html=True)
            st.button(" ", key=f"slot_btn_{i}", on_click=ganti_warna, args=(i,))
            st.markdown('</div>', unsafe_allow_html=True)

    st.write("")
    if st.button("CEK JAWABAN (OK) ✅", key="ok_main", use_container_width=True):
        if "Kosong" not in st.session_state.guesses:
            teks = hitung_feedback(st.session_state.guesses, st.session_state.target)
            st.session_state.history.append({'g': list(st.session_state.guesses), 'f': teks})
            if st.session_state.guesses == st.session_state.target:
                st.balloons()
                st.success("🎉 JACKPOT! MENANG!")

    if st.session_state.history:
        st.write("### 📜 RIWAYAT:")
        for h in reversed(st.session_state.history):
            st.info(h['f'])
            card_row = "".join([f'<div style="display:inline-block; width:15px; height:20px; background-color:{WARNA_HEX[c]}; margin-right:5px; border:1px solid white;"></div>' for c in h['g']])
            st.markdown(card_row, unsafe_allow_html=True)
