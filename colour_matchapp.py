import streamlit as st
import random

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Colour Match Master", layout="centered")

# --- 2. CSS CUSTOM (OPTIMASI TOMBOL & UKURAN) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee+Shade&family=Space+Mono:wght@400;700&display=swap');
    #MainMenu, footer, header {visibility: hidden;}
    
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }

    /* GRID UNTUK KOTAK JAWABAN */
    [data-testid="stHorizontalBlock"] {
        display: grid !important;
        grid-template-columns: repeat(auto-fit, minmax(0, 1fr)) !important;
        gap: 6px !important;
        width: 100% !important;
    }

    /* KOTAK WARNA LANGSING */
    .card-slot {
        aspect-ratio: 2 / 3.5;
        width: 100%;
        border-radius: 8px;
        border: 2px solid #ffffff;
        margin-bottom: 5px;
        box-shadow: 0px 4px 8px rgba(0,0,0,0.5);
    }

    /* TOMBOL GANTI: UKURAN PAS KOTAK & TEKS SATU BARIS */
    .stButton > button {
        width: 100% !important;
        font-size: 9px !important; /* Perkecil teks agar tidak enter */
        height: 32px !important;
        padding: 0px 2px !important;
        white-space: nowrap !important; /* Paksa satu baris */
        overflow: hidden !important;
        text-overflow: clip !important;
    }

    /* TOMBOL CEK JAWABAN & MAIN LAGI */
    .cek-area .stButton > button {
        width: 100% !important;
        height: 55px !important;
        font-size: 18px !important;
        font-weight: bold !important;
        background-color: #262730 !important;
        border: 2px solid #FFD700 !important;
        color: white !important;
        border-radius: 12px !important;
        margin-top: 20px;
    }

    .title-text {
        text-align: center; font-family: 'Bungee Shade', cursive; 
        font-size: 26px; color: white; margin-bottom: 20px;
    }

    .chance-text {
        text-align: center; font-size: 22px; font-weight: bold;
        color: #FF4B4B; margin-bottom: 5px;
    }

    .pool-container {
        display: flex; justify-content: center; gap: 8px; margin-bottom: 20px;
    }
    .pool-box { width: 20px; height: 20px; border-radius: 4px; border: 1px solid #fff; }
</style>
""", unsafe_allow_html=True)

# --- 3. LOGIKA GAME ---
WARNA_LIST = ["Merah", "Oren", "Kuning", "Hijau", "Biru"]
WARNA_HEX = {"Kosong": "#333333", "Merah": "#FF0000", "Oren": "#FFA500", "Kuning": "#FFFF00", "Hijau": "#00FF00", "Biru": "#0000FF"}

if 'game_active' not in st.session_state:
    st.session_state.game_active = False

def start_game(mode):
    if mode == "Mudah":
        k, ch = 3, 5
    elif mode == "Sedang":
        k, ch = 4, 8
    else: # Sulit
        k, ch = 5, 10
        
    pool = random.sample(WARNA_LIST, k)
    st.session_state.target = [random.choice(pool) for _ in range(k)]
    st.session_state.pool = pool
    st.session_state.max_k = k
    st.session_state.guesses = ["Kosong"] * k
    st.session_state.history = []
    st.session_state.chances = ch
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
    return f"{b_pos} Benar, {b_warna} Salah Posisi"

# --- 4. TAMPILAN ---
st.markdown('<div class="title-text">COLOUR MATCH</div>', unsafe_allow_html=True)

if not st.session_state.game_active:
    if st.button("🟢 MUDAH", use_container_width=True): start_game("Mudah"); st.rerun()
    if st.button("🟡 SEDANG", use_container_width=True): start_game("Sedang"); st.rerun()
    if st.button("🔴 SULIT", use_container_width=True): start_game("Sulit"); st.rerun()
else:
    st.markdown(f'<div class="chance-text">Sisa: {st.session_state.chances}x</div>', unsafe_allow_html=True)
    
    pool_html = '<div class="pool-container">'
    for p_color in st.session_state.pool:
        pool_html += f'<div class="pool-box" style="background-color:{WARNA_HEX[p_color]};"></div>'
    pool_html += '</div>'
    st.markdown(pool_html, unsafe_allow_html=True)

    cols = st.columns(st.session_state.max_k)
    for i in range(st.session_state.max_k):
        with cols[i]:
            st.markdown(f'<div class="card-slot" style="background-color:{WARNA_HEX[st.session_state.guesses[i]]};"></div>', unsafe_allow_html=True)
            st.button("Ganti", key=f"btn_{i}", on_click=ganti_warna, args=(i,))

    st.markdown('<div class="cek-area">', unsafe_allow_html=True)
    if not st.session_state.game_over:
        if st.button("Cek Jawaban", use_container_width=True):
            if "Kosong" not in st.session_state.guesses:
                st.session_state.chances -= 1
                fb = hitung_feedback(st.session_state.guesses, st.session_state.target)
                st.session_state.history.append({'g': list(st.session_state.guesses), 'f': fb})
                
                if st.session_state.guesses == st.session_state.target:
                    st.balloons()
                    st.session_state.game_over = True
                elif st.session_state.chances <= 0:
                    st.session_state.game_over = True
                st.rerun()
    else:
        # Tombol Main Lagi tanpa ikon
        if st.button("Main Lagi", use_container_width=True):
            st.session_state.game_active = False
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.history:
        st.write("---")
        st.write("### 📜 RIWAYAT TEBAKAN:")
        for h in reversed(st.session_state.history):
            st.info(h['f'])
            row_html = "".join([f'<div style="display:inline-block; width:18px; height:18px; background-color:{WARNA_HEX[c]}; margin-right:6px; border:1px solid white; border-radius:3px;"></div>' for c in h['g']])
            st.markdown(row_html, unsafe_allow_html=True)
