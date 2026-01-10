import streamlit as st
import random

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Colour Match Master", layout="centered")

# --- 2. CSS CUSTOM (KUNCI UKURAN & JARAK SEMPIT) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee+Shade&family=Space+Mono:wght@400;700&display=swap');
    #MainMenu, footer, header {visibility: hidden;}
    
    /* AREA CONTAINER UTAMA */
    .stApp { background-color: #0E1117; }

    /* JARAK ANTAR KOTAK SANGAT SEMPIT (5px) */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 5px !important; 
        justify-content: center !important;
        align-items: flex-start !important;
    }

    /* KUNCI LEBAR KOLOM AGAR KOTAK TETAP KECIL */
    [data-testid="column"] {
        width: 70px !important; 
        flex: none !important;
    }

    .title-text {
        text-align: center; font-family: 'Bungee Shade', cursive; 
        font-size: 24px; color: white; margin-bottom: 10px;
    }

    /* KOTAK WARNA: UKURAN TETAP (± 2cm x 2.5cm) */
    .card-slot {
        width: 65px !important;
        height: 85px !important;
        border-radius: 6px;
        border: 2px solid #fff;
        margin-bottom: 5px;
    }

    /* TOMBOL GANTI KECIL */
    .stButton > button {
        width: 65px !important;
        height: 30px !important;
        font-size: 10px !important;
        padding: 0px !important;
    }

    /* KOTAK KECIL WARNA RAHASIA (HORIZONTAL) */
    .pool-container {
        display: flex;
        justify-content: center;
        gap: 8px;
        margin-bottom: 15px;
    }
    .pool-box {
        width: 20px;
        height: 20px;
        border-radius: 3px;
        border: 1px solid white;
    }

    .chance-text {
        text-align: center; font-size: 18px; font-weight: bold;
        color: #FF4B4B; margin-bottom: 10px; font-family: 'Space Mono', monospace;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. LOGIKA GAME ---
WARNA_LIST = ["Merah", "Oren", "Kuning", "Hijau", "Biru"]
WARNA_HEX = {"Kosong": "#333333", "Merah": "#FF0000", "Oren": "#FFA500", "Kuning": "#FFFF00", "Hijau": "#00FF00", "Biru": "#0000FF"}

if 'game_active' not in st.session_state:
    st.session_state.game_active = False

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

# --- 4. TAMPILAN ---
st.markdown('<div class="title-text">COLOUR MATCH</div>', unsafe_allow_html=True)

if not st.session_state.game_active:
    st.markdown('<div style="color:white; text-align:center; margin-bottom:15px;">PILIH LEVEL:</div>', unsafe_allow_html=True)
    if st.button("🟢 MUDAH", use_container_width=True): start_game("Mudah"); st.rerun()
    if st.button("🟡 SEDANG", use_container_width=True): start_game("Sedang"); st.rerun()
    if st.button("🔴 SULIT", use_container_width=True): start_game("Sulit"); st.rerun()
else:
    st.markdown(f'<div class="chance-text">Sisa: {st.session_state.chances}x</div>', unsafe_allow_html=True)
    
    # ASUMSI WARNA RAHASIA (KOTAK KECIL HORIZONTAL)
    st.markdown('<div style="color:white; text-align:center; font-size:14px; margin-bottom:5px;">Warna Rahasia Terdiri Dari:</div>', unsafe_allow_html=True)
    pool_html = '<div class="pool-container">'
    for p_color in st.session_state.pool:
        pool_html += f'<div class="pool-box" style="background-color:{WARNA_HEX[p_color]};"></div>'
    pool_html += '</div>'
    st.markdown(pool_html, unsafe_allow_html=True)

    # AREA TEBAKAN (JARAK SEMPIT & UKURAN TETAP)
    cols = st.columns(st.session_state.max_k)
    for i in range(st.session_state.max_k):
        with cols[i]:
            st.markdown(f'<div class="card-slot" style="background-color:{WARNA_HEX[st.session_state.guesses[i]]};"></div>', unsafe_allow_html=True)
            st.button("Ganti", key=f"btn_{i}", on_click=ganti_warna, args=(i,))

    st.write("")
    if not st.session_state.game_over:
        if st.button("CEK JAWABAN ✅", use_container_width=True):
            if "Kosong" not in st.session_state.guesses:
                st.session_state.chances -= 1
                b_pos = sum(1 for g, t in zip(st.session_state.guesses, st.session_state.target) if g == t)
                st.session_state.history.append({'g': list(st.session_state.guesses), 'f': f"{b_pos} Benar Posisi"})
                if st.session_state.guesses == st.session_state.target:
                    st.balloons(); st.session_state.game_over = True
                elif st.session_state.chances <= 0:
                    st.session_state.game_over = True
                st.rerun()
    else:
        st.button("MAIN LAGI 🔄", use_container_width=True, on_click=lambda: setattr(st.session_state, 'game_active', False))
