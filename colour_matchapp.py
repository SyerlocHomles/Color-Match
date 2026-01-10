import streamlit as st
import random

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Colour Match Master", layout="centered")

# --- 2. CSS CUSTOM (FIX UKURAN KOTAK & HORIZONTAL SCROLL) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee+Shade&family=Space+Mono:wght@400;700&display=swap');
    #MainMenu, footer, header {visibility: hidden;}
    
    /* Container untuk scroll jika layar HP sempit */
    .game-container {
        display: flex !important;
        flex-direction: row !important;
        overflow-x: auto !important; /* Memungkinkan scroll ke samping */
        padding: 10px 0 !important;
        gap: 15px !important;
        justify-content: flex-start !important;
        -webkit-overflow-scrolling: touch;
    }

    /* Memaksa kolom Streamlit mengikuti aturan scroll */
    [data-testid="stHorizontalBlock"] {
        flex-wrap: nowrap !important;
        overflow-x: auto !important;
    }

    .title-text {
        text-align: center; font-family: 'Bungee Shade', cursive; 
        font-size: 24px; color: white; margin-bottom: 10px;
    }

    /* KOTAK WARNA: Lebar 2.5cm (~95px) & Tinggi 3cm (~115px) */
    .card-slot {
        width: 95px !important;
        height: 115px !important;
        border-radius: 8px;
        border: 2px solid #fff;
        margin-bottom: 10px;
        flex-shrink: 0 !important; /* Mencegah kotak jadi gepeng */
    }

    .stButton > button {
        width: 95px !important; /* Lebar tombol sama dengan kotak */
        font-size: 11px !important;
        height: 40px !important;
        border-radius: 6px !important;
    }

    .chance-text {
        text-align: center; font-size: 18px; font-weight: bold;
        color: #FF4B4B; margin-bottom: 15px; font-family: 'Space Mono', monospace;
    }

    /* Baris petunjuk warna di atas dibuat kecil saja */
    .pool-slot {
        height: 12px; width: 40px; border-radius: 2px; border: 1px solid white;
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
    return f"{b_pos} benar posisi, {b_warna} benar warna (salah posisi), {salah} salah"

# --- 4. TAMPILAN ---
st.markdown('<div class="title-text">COLOUR MATCH</div>', unsafe_allow_html=True)

if not st.session_state.game_active:
    # Tampilan Menu Awal
    st.markdown('<div style="color:white; text-align:center;">PILIH LEVEL:</div>', unsafe_allow_html=True)
    if st.button("🟢 MUDAH", use_container_width=True): start_game("Mudah"); st.rerun()
    if st.button("🟡 SEDANG", use_container_width=True): start_game("Sedang"); st.rerun()
    if st.button("🔴 SULIT", use_container_width=True): start_game("Sulit"); st.rerun()
else:
    # Game Aktif
    st.markdown(f'<div class="chance-text">Kesempatan: {st.session_state.chances}x</div>', unsafe_allow_html=True)

    # Petunjuk Warna (Kecil)
    st.write("Warna Rahasia Terdiri Dari:")
    p_cols = st.columns(len(st.session_state.pool))
    for idx, p_color in enumerate(st.session_state.pool):
        p_cols[idx].markdown(f'<div class="pool-slot" style="background-color:{WARNA_HEX[p_color]};"></div>', unsafe_allow_html=True)

    st.write("---")

    # AREA TEBAKAN (HORIZONTALLY SCROLLABLE)
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
                    st.error("❌ KALAH!"); st.session_state.game_over = True
                st.rerun()
    else:
        if st.button("MAIN LAGI 🔄", use_container_width=True):
            st.session_state.game_active = False
            st.rerun()

    # Riwayat Tebakan
    if st.session_state.history:
        st.write("### 📜 RIWAYAT:")
        for h in reversed(st.session_state.history):
            st.info(h['f'])
            row = "".join([f'<div style="display:inline-block; width:20px; height:20px; background-color:{WARNA_HEX[c]}; margin-right:5px; border:1px solid white; border-radius:3px;"></div>' for c in h['g']])
            st.markdown(row, unsafe_allow_html=True)
