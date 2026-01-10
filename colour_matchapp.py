import streamlit as st
import random

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Colour Match Master", layout="centered")

# --- 2. CSS CUSTOM (FIX JARAK 0.25CM & ICON POS) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee+Shade&family=Space+Mono:wght@400;700&display=swap');
    #MainMenu, footer, header {visibility: hidden;}
    
    /* JARAK ANTAR KOTAK 0.25CM (~10px) */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 10px !important; 
        overflow-x: auto !important;
        padding-bottom: 10px;
        justify-content: center !important;
    }

    [data-testid="column"] {
        flex-shrink: 0 !important;
        width: 95px !important; 
    }

    .title-text {
        text-align: center; font-family: 'Bungee Shade', cursive; 
        font-size: 24px; color: white; margin-bottom: 20px;
    }

    /* KOTAK WARNA: Lebar 2.5cm & Tinggi 3cm */
    .card-slot {
        width: 95px !important;
        height: 115px !important;
        border-radius: 8px;
        border: 2px solid #fff;
        margin-bottom: 8px;
    }

    /* TOMBOL GANTI WARNA */
    .stButton > button {
        width: 95px !important;
        font-size: 11px !important;
        height: 40px !important;
        border-radius: 6px !important;
    }

    /* TOMBOL MENU (ICON DI ATAS) */
    .menu-btn-container {
        text-align: center;
        margin-bottom: 20px;
    }

    .chance-text {
        text-align: center; font-size: 18px; font-weight: bold;
        color: #FF4B4B; margin-bottom: 15px; font-family: 'Space Mono', monospace;
    }

    .pool-slot {
        height: 12px; width: 35px; border-radius: 2px; border: 1px solid white;
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
    k = 3 if mode == "Mudah" else 4 if mode == "Sedang" else 5
    pool = random.sample(WARNA_LIST, k)
    st.session_state.target = [random.choice(pool) for _ in range(k)]
    st.session_state.pool = pool
    st.session_state.max_k = k
    st.session_state.guesses = ["Kosong"] * k
    st.session_state.history = []
    st.session_state.chances = 5
    st.session_state.game_active = True
    st.session_state.game_over = False

def ganti_warna(i):
    if not st.session_state.game_over:
        pool = st.session_state.pool
        cur = st.session_state.guesses[i]
        next_idx = (pool.index(cur) + 1) % len(pool) if cur in pool else 0
        st.session_state.guesses[i] = pool[next_idx]

def hitung_feedback(guess, target):
    t_temp, g_temp = list(target), list(guess)
    b_pos, b_warna = 0, 0
    for i in range(len(t_temp)):
        if g_temp[i] == t_temp[i]:
            b_pos += 1
            t_temp[i], g_temp[i] = "DONE", "USED"
    for i in range(len(g_temp)):
        if g_temp[i] != "USED" and g_temp[i] in t_temp:
            b_warna += 1
            t_temp[t_temp.index(g_temp[i])] = "DONE"
    salah = len(target) - (b_pos + b_warna)
    return f"{b_pos} benar posisi, {b_warna} benar warna, {salah} salah"

# --- 4. TAMPILAN ---
st.markdown('<div class="title-text">COLOUR MATCH</div>', unsafe_allow_html=True)

if not st.session_state.game_active:
    st.markdown('<div style="color:white; text-align:center; margin-bottom:20px;">PILIH LEVEL UNTUK MULAI:</div>', unsafe_allow_html=True)
    
    # Tombol Menu dengan Simbol di Atas
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        if st.button("🟢\nMUDAH", use_container_width=True): start_game("Mudah"); st.rerun()
    with col_m2:
        if st.button("🟡\nSEDANG", use_container_width=True): start_game("Sedang"); st.rerun()
    with col_m3:
        if st.button("🔴\nSULIT", use_container_width=True): start_game("Sulit"); st.rerun()
else:
    # Game Aktif
    st.markdown(f'<div class="chance-text">Sisa Tebakan: {st.session_state.chances}x</div>', unsafe_allow_html=True)

    # Petunjuk Warna
    st.write("Warna Rahasia Terdiri Dari:")
    p_cols = st.columns(len(st.session_state.pool))
    for idx, p_color in enumerate(st.session_state.pool):
        p_cols[idx].markdown(f'<div class="pool-slot" style="background-color:{WARNA_HEX[p_color]};"></div>', unsafe_allow_html=True)

    st.write("---")

    # AREA TEBAKAN (JARAK 0.25CM)
    cols = st.columns(st.session_state.max_k)
    for i in range(st.session_state.max_k):
        with cols[i]:
            st.markdown(f'<div class="card-slot" style="background-color:{WARNA_HEX[st.session_state.guesses[i]]};"></div>', unsafe_allow_html=True)
            st.button("Ganti", key=f"btn_{i}", on_click=ganti_warna, args=(i,))

    st.write("---")
    
    if not st.session_state.game_over:
        if st.button("CEK JAWABAN ✅", use_container_width=True):
            if "Kosong" not in st.session_state.guesses:
                st.session_state.chances -= 1
                fb = hitung_feedback(st.session_state.guesses, st.session_state.target)
                st.session_state.history.append({'g': list(st.session_state.guesses), 'f': fb})
                
                if st.session_state.guesses == st.session_state.target:
                    st.balloons(); st.success("🎉 MENANG!"); st.session_state.game_over = True
                elif st.session_state.chances <= 0:
                    st.error(f"❌ KALAH! Jawabannya: {', '.join(st.session_state.target)}"); st.session_state.game_over = True
                st.rerun()
    else:
        if st.button("MAIN LAGI 🔄", use_container_width=True):
            st.session_state.game_active = False
            st.rerun()

    # Riwayat
    if st.session_state.history:
        st.write("### 📜 RIWAYAT:")
        for h in reversed(st.session_state.history):
            st.info(h['f'])
            row = "".join([f'<div style="display:inline-block; width:18px; height:18px; background-color:{WARNA_HEX[c]}; margin-right:4px; border:1px solid white; border-radius:3px;"></div>' for c in h['g']])
            st.markdown(row, unsafe_allow_html=True)
