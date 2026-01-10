import streamlit as st
import random

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Colour Match Master", layout="centered")

# --- 2. CSS CUSTOM (KUNCI UKURAN KOTAK & JARAK) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee+Shade&family=Space+Mono:wght@400;700&display=swap');
    #MainMenu, footer, header {visibility: hidden;}
    
    /* AREA CONTAINER KOTAK */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 18px !important; /* Jarak antar kotak ± 0.5cm */
        justify-content: center !important;
        align-items: flex-start !important;
    }

    /* KUNCI LEBAR KOLOM AGAR KOTAK TIDAK MELEBAR */
    [data-testid="column"] {
        width: 95px !important; /* Kunci lebar 2.5cm */
        flex: none !important;
    }

    .title-text {
        text-align: center; font-family: 'Bungee Shade', cursive; 
        font-size: 24px; color: white; margin-bottom: 20px;
    }

    /* KOTAK WARNA: FIX 2.5CM X 3CM */
    .card-slot {
        width: 95px !important;  /* ± 2.5cm */
        height: 115px !important; /* ± 3cm */
        border-radius: 10px;
        border: 2px solid #fff;
        margin-bottom: 10px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
    }

    /* TOMBOL GANTI JADI LEBIH PAS */
    .stButton > button {
        width: 95px !important;
        height: 35px !important;
        font-size: 12px !important;
        padding: 0px !important;
    }

    .chance-text {
        text-align: center; font-size: 18px; font-weight: bold;
        color: #FF4B4B; margin-bottom: 15px; font-family: 'Space Mono', monospace;
    }
    
    /* PANEL WARNA RAHASIA DI ATAS */
    .pool-slot {
        height: 12px; width: 100%; border-radius: 2px; border: 1px solid white;
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

# --- 4. TAMPILAN ---
st.markdown('<div class="title-text">COLOUR MATCH</div>', unsafe_allow_html=True)

if not st.session_state.game_active:
    st.markdown('<div style="color:white; text-align:center; margin-bottom:15px;">PILIH LEVEL:</div>', unsafe_allow_html=True)
    if st.button("🟢 MUDAH", use_container_width=True): start_game("Mudah"); st.rerun()
    if st.button("🟡 SEDANG", use_container_width=True): start_game("Sedang"); st.rerun()
    if st.button("🔴 SULIT", use_container_width=True): start_game("Sulit"); st.rerun()
else:
    st.markdown(f'<div class="chance-text">Sisa: {st.session_state.chances}x</div>', unsafe_allow_html=True)
    st.write("Warna Rahasia Terdiri Dari:")
    
    # Pool Warna
    p_cols = st.columns(len(st.session_state.pool))
    for idx, p_color in enumerate(st.session_state.pool):
        p_cols[idx].markdown(f'<div class="pool-slot" style="background-color:{WARNA_HEX[p_color]};"></div>', unsafe_allow_html=True)

    st.write("---")

    # AREA TEBAKAN (UKURAN TETAP & JARAK PAS)
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
                # (Logika hitung feedback singkat)
                b_pos = sum(1 for g, t in zip(st.session_state.guesses, st.session_state.target) if g == t)
                fb_text = f"{b_pos} Benar Posisi"
                st.session_state.history.append({'g': list(st.session_state.guesses), 'f': fb_text})
                
                if st.session_state.guesses == st.session_state.target:
                    st.balloons(); st.success("🎉 MENANG!"); st.session_state.game_over = True
                elif st.session_state.chances <= 0:
                    st.error("❌ KALAH!"); st.session_state.game_over = True
                st.rerun()
    else:
        if st.button("MAIN LAGI 🔄", use_container_width=True):
            st.session_state.game_active = False
            st.rerun()
