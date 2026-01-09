import streamlit as st
import random

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Colour Match Master", layout="centered")

# --- 2. CSS CUSTOM (KARTU ADALAH TOMBOL) ---
st.markdown("""
<style>
    #MainMenu, footer, header {visibility: hidden;}
    .title-text {text-align: center; font-size: 30px; font-weight: bold; color: white; margin-bottom: 20px;}
    
    /* Container utama kartu */
    .card-slot {
        position: relative;
        height: 120px;
        width: 100%;
        border-radius: 12px;
        border: 2px solid #555;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    /* Membuat tombol Streamlit transparan menutupi seluruh kartu */
    .stButton > button {
        position: absolute;
        top: 0;
        left: 0;
        height: 120px !important;
        width: 100% !important;
        background-color: transparent !important;
        border: none !important;
        color: transparent !important;
        z-index: 10;
        cursor: pointer;
    }
    
    .stButton > button:hover {
        background-color: rgba(255,255,255,0.1) !important;
    }

    .feedback-box {
        background-color: #1e1e1e;
        padding: 12px;
        border-radius: 8px;
        border-left: 5px solid #FFA500;
        margin-top: 15px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. LOGIKA GAME ---
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
    t_temp = list(target)
    g_temp = list(guess)
    benar_posisi, salah_posisi = 0, 0
    
    for i in range(len(t_temp)):
        if g_temp[i] == t_temp[i]:
            benar_posisi += 1
            t_temp[i], g_temp[i] = "DONE_T", "DONE_G"
            
    for i in range(len(g_temp)):
        if g_temp[i] != "DONE_G" and g_temp[i] in t_temp:
            salah_posisi += 1
            t_temp[t_temp.index(g_temp[i])] = "DONE_T"
                
    salah_warna = len(target) - (benar_posisi + salah_posisi)
    return f"{benar_posisi} warna benar, {salah_posisi} warna salah posisi, {salah_warna} warna salah"

# --- 4. TAMPILAN ---
st.markdown('<div class="title-text">COLOUR MATCH</div>', unsafe_allow_html=True)

if not st.session_state.game_active:
    st.write("### Pilih Tingkat Kesulitan:")
    c1, c2, c3 = st.columns(3)
    if c1.button("Mudah", key="m_btn"): start_game("Mudah")
    if c2.button("Sedang", key="s_btn"): start_game("Sedang")
    if c3.button("Sulit", key="sl_btn"): start_game("Sulit")
else:
    if st.sidebar.button("Ganti Level / Reset"):
        st.session_state.game_active = False
        st.rerun()

    st.write(f"Warna yang mungkin muncul ({st.session_state.max_k} kartu):")
    h_cols = st.columns(len(st.session_state.pool))
    for idx, h in enumerate(st.session_state.pool):
        h_cols[idx].markdown(f"<div style='background-color:{WARNA_HEX[h]}; height:20px; border:1px solid white;'></div>", unsafe_allow_html=True)

    st.write("---")

    # SLOT KARTU (KARTU ADALAH TOMBOL)
    cols = st.columns(st.session_state.max_k)
    for i in range(st.session_state.max_k):
        with cols[i]:
            # Visual Warna Kartu
            current_color = WARNA_HEX[st.session_state.guesses[i]]
            st.markdown(f'<div class="card-slot" style="background-color:{current_color};"></div>', unsafe_allow_html=True)
            # Tombol Transparan menimpa visual di atas
            st.button("", key=f"slot_btn_{i}", on_click=ganti_warna, args=(i,))

    st.write("")
    if st.button("OK ✅", key="final_ok_btn", use_container_width=True):
        if "Kosong" not in st.session_state.guesses:
            teks = hitung_feedback(st.session_state.guesses, st.session_state.target)
            st.session_state.history.append({'g': list(st.session_state.guesses), 'f': teks})
            if st.session_state.guesses == st.session_state.target:
                st.balloons()
                st.success("JACKPOT! Kamu Berhasil!")

    if st.session_state.history:
        st.write("### Riwayat:")
        for h in reversed(st.session_state.history):
            st.markdown(f'<div class="feedback-box"><p style="color:#FFA500; font-weight:bold; margin:0;">{h["f"]}</p></div>', unsafe_allow_html=True)
            card_row = "".join([f'<div style="display:inline-block; width:20px; height:30px; background-color:{WARNA_HEX[c]}; margin-right:5px; border:1px solid white;"></div>' for c in h['g']])
            st.markdown(card_row, unsafe_allow_html=True)
            st.write("")
