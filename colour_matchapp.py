import streamlit as st
import random

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Colour Match Master", layout="centered")

# --- 2. CSS CUSTOM (HARD FIX UNTUK JARAK SANGAT RAPAT) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee+Shade&family=Space+Mono:wght@400;700&display=swap');
    #MainMenu, footer, header {visibility: hidden;}
    
    /* MEMAKSA JARAK ANTAR KOLOM JADI MINIMAL */
    [data-testid="stHorizontalBlock"] {
        gap: 2px !important; 
        justify-content: center !important;
        flex-wrap: nowrap !important; /* Mencegah kotak turun ke bawah */
    }

    /* MENGHAPUS PADDING BAWAAN STREAMLIT PADA KOLOM */
    [data-testid="column"] {
        padding: 0px !important;
        margin: 0px -2px !important; /* Teknik negative margin untuk merapatkan */
        min-width: 0px !important;
        flex: 0 0 auto !important;
        width: 60px !important;
    }

    .title-text {
        text-align: center; font-family: 'Bungee Shade', cursive; 
        font-size: 24px; color: white; margin-bottom: 10px;
    }

    /* KOTAK WARNA: LANGSING SESUAI GAMBAR */
    .card-slot {
        width: 58px !important;
        height: 90px !important;
        border-radius: 6px;
        border: 1.5px solid #ffffff;
        margin: 0 auto 5px auto;
    }

    /* TOMBOL GANTI: PRESISI DI BAWAH KOTAK */
    .stButton > button {
        width: 58px !important;
        height: 30px !important;
        font-size: 10px !important;
        padding: 0px !important;
        border-radius: 4px !important;
        margin: 0 auto !important;
    }

    /* KOTAK KECIL WARNA RAHASIA (TENGAH) */
    .pool-container {
        display: flex;
        justify-content: center;
        gap: 5px;
        margin-bottom: 15px;
    }
    .pool-box {
        width: 18px;
        height: 18px;
        border-radius: 3px;
        border: 1px solid white;
    }

    /* TOMBOL CEK JAWABAN: MEMANJANG HORIZONTAL */
    .cek-wrapper .stButton > button {
        width: 100% !important;
        height: 50px !important;
        font-size: 18px !important;
        font-weight: bold !important;
        background-color: #262730 !important;
        border: 2px solid #FFD700 !important;
        color: white !important;
        margin-top: 20px;
        border-radius: 10px !important;
    }

    .chance-text {
        text-align: center; font-size: 22px; font-weight: bold;
        color: #FF4B4B; margin-bottom: 5px; font-family: 'Space Mono', monospace;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. LOGIKA GAME ---
if 'game_active' not in st.session_state:
    st.session_state.game_active = False

WARNA_LIST = ["Merah", "Oren", "Kuning", "Hijau", "Biru"]
WARNA_HEX = {"Kosong": "#333333", "Merah": "#FF0000", "Oren": "#FFA500", "Kuning": "#FFFF00", "Hijau": "#00FF00", "Biru": "#0000FF"}

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
    
    # 1. WARNA RAHASIA (KOTAK KECIL TENGAH)
    st.markdown('<div style="color:white; text-align:center; font-size:12px; margin-bottom:5px;">Warna Rahasia Terdiri Dari:</div>', unsafe_allow_html=True)
    pool_html = '<div class="pool-container">'
    for p_color in st.session_state.pool:
        pool_html += f'<div class="pool-box" style="background-color:{WARNA_HEX[p_color]};"></div>'
    pool_html += '</div>'
    st.markdown(pool_html, unsafe_allow_html=True)

    st.write("---")

    # 2. AREA TEBAKAN (RAPAT & SEMPIT)
    cols = st.columns(st.session_state.max_k)
    for i in range(st.session_state.max_k):
        with cols[i]:
            st.markdown(f'<div class="card-slot" style="background-color:{WARNA_HEX[st.session_state.guesses[i]]};"></div>', unsafe_allow_html=True)
            st.button("Ganti", key=f"btn_{i}", on_click=ganti_warna, args=(i,))

    # 3. TOMBOL CEK JAWABAN (MEMANJANG)
    st.markdown('<div class="cek-wrapper">', unsafe_allow_html=True)
    if not st.session_state.game_over:
        if st.button("Cek Jawaban", use_container_width=True):
            if "Kosong" not in st.session_state.guesses:
                st.session_state.chances -= 1
                b_pos = sum(1 for g, t in zip(st.session_state.guesses, st.session_state.target) if g == t)
                st.session_state.history.append({'g': list(st.session_state.guesses), 'f': f"{b_pos} Benar"})
                if st.session_state.guesses == st.session_state.target:
                    st.balloons(); st.session_state.game_over = True
                elif st.session_state.chances <= 0:
                    st.session_state.game_over = True
                st.rerun()
    else:
        if st.button("MAIN LAGI 🔄", use_container_width=True):
            st.session_state.game_active = False
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
