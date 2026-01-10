import streamlit as st
import random

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Colour Match Master", layout="centered")

# --- 2. CSS CUSTOM (FIX MENU & JARAK RAPAT) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee+Shade&family=Space+Mono:wght@400;700&display=swap');
    #MainMenu, footer, header {visibility: hidden;}
    
    /* JARAK ANTAR KOTAK DIBUAT RAPAT (8px) AGAR TIDAK TERHALANG */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 8px !important; 
        justify-content: center !important;
    }

    [data-testid="column"] {
        flex: 1 !important;
        min-width: 0px !important;
    }

    .title-text {
        text-align: center; font-family: 'Bungee Shade', cursive; 
        font-size: 24px; color: white; margin-bottom: 20px;
    }

    /* KOTAK WARNA: Tetap Proporsional */
    .card-slot {
        aspect-ratio: 2.5 / 3; /* Lebar 2.5, Tinggi 3 */
        width: 100%;
        border-radius: 8px;
        border: 2px solid #fff;
        margin-bottom: 8px;
    }

    /* TOMBOL GANTI */
    .stButton > button {
        width: 100% !important;
        font-size: 10px !important;
        padding: 0px !important;
        height: 35px !important;
    }

    .chance-text {
        text-align: center; font-size: 18px; font-weight: bold;
        color: #FF4B4B; margin-bottom: 15px; font-family: 'Space Mono', monospace;
    }

    .pool-slot {
        height: 10px; width: 100%; border-radius: 2px; border: 1px solid white;
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
    return b_pos, b_warna

# --- 4. TAMPILAN ---
st.markdown('<div class="title-text">COLOUR MATCH</div>', unsafe_allow_html=True)

if not st.session_state.game_active:
    st.markdown('<div style="color:white; text-align:center; margin-bottom:10px;">PILIH LEVEL:</div>', unsafe_allow_html=True)
    # Tombol Level: Simbol di KIRI tulisan
    if st.button("🟢 MUDAH", use_container_width=True): start_game("Mudah"); st.rerun()
    if st.button("🟡 SEDANG", use_container_width=True): start_game("Sedang"); st.rerun()
    if st.button("🔴 SULIT", use_container_width=True): start_game("Sulit"); st.rerun()
else:
    st.markdown(f'<div class="chance-text">Sisa: {st.session_state.chances}x</div>', unsafe_allow_html=True)

    # Petunjuk Warna (Sejajar di atas)
    st.write("Warna Rahasia Terdiri Dari:")
    p_cols = st.columns(len(st.session_state.pool))
    for idx, p_color in enumerate(st.session_state.pool):
        p_cols[idx].markdown(f'<div class="pool-slot" style="background-color:{WARNA_HEX[p_color]};"></div>', unsafe_allow_html=True)

    st.write("---")

    # AREA TEBAKAN (JARAK RAPAT & HORIZONTAL)
    cols = st.columns(st.session_state.max_k)
    for i in range(st.session_state.max_k):
        with cols[i]:
            st.markdown(f'<div class="card-slot" style="background-color:{WARNA_HEX[st.session_state.guesses[i]]};"></div>', unsafe_allow_html=True)
            st.button("Ganti", key=f"btn_{i}", on_click=ganti_warna, args=(i,))

    st.write("---")
    
    if not st.session_state.game_over:
        if st.button("CEK JAWABAN (OK) ✅", use_container_width=True):
            if "Kosong" not in st.session_state.guesses:
                st.session_state.chances -= 1
                b_pos, b_warna = hitung_feedback(st.session_state.guesses, st.session_state.target)
                fb_text = f"{b_pos} Benar, {b_warna} Salah Posisi"
                st.session_state.history.append({'g': list(st.session_state.guesses), 'f': fb_text})
                
                if st.session_state.guesses == st.session_state.target:
                    st.balloons(); st.success("🎉 MENANG!"); st.session_state.game_over = True
                elif st.session_state.chances <= 0:
                    st.error("❌ KESEMPATAN HABIS!"); st.session_state.game_over = True
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
            row_html = "".join([f'<div style="display:inline-block; width:15px; height:15px; background-color:{WARNA_HEX[c]}; margin-right:4px; border:1px solid white; border-radius:2px;"></div>' for c in h['g']])
            st.markdown(row_html, unsafe_allow_html=True)
