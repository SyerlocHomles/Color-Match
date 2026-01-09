import streamlit as st
import random

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Colour Match Master", layout="centered")

# --- 2. CSS CUSTOM (KARTU LEBIH KECIL & RAPI) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee+Shade&family=Space+Mono:wght@400;700&display=swap');

    #MainMenu, footer, header {visibility: hidden;}
    
    .title-text {
        text-align: center; 
        font-family: 'Bungee Shade', cursive; 
        font-size: 30px; 
        color: white; 
        margin-bottom: 15px;
    }

    .desc-text {
        font-family: 'Space Mono', monospace;
        color: white;
        background-color: rgba(255, 255, 255, 0.1);
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #555;
        margin-bottom: 20px;
        font-size: 13px;
    }

    /* Ukuran kartu yang lebih kecil untuk HP */
    .card-slot {
        height: 60px;
        width: 100%;
        border-radius: 8px;
        border: 2px solid #555;
        margin-bottom: 8px; /* Jarak antara kartu dan tombol di bawahnya */
    }

    /* Styling tombol ganti warna agar kecil dan pas di tengah */
    .stButton > button {
        width: 100% !important;
        border-radius: 5px !important;
        padding: 2px !important;
        font-size: 12px !important;
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
    return f"{b} Benar, {s} Salah Posisi"

# --- 4. TAMPILAN ---
st.markdown('<div class="title-text">COLOUR MATCH</div>', unsafe_allow_html=True)

if not st.session_state.game_active:
    st.markdown("""
    <div class="desc-text">
        <strong>🎯 CARA BERMAIN:</strong><br>
        1. Pilih level untuk mulai.<br>
        2. Klik tombol 🔄 di bawah kotak untuk ganti warna.<br>
        3. Tekan OK untuk cek hasil.
    </div>
    """, unsafe_allow_html=True)

    st.write("### 🕹️ PILIH LEVEL:")
    if st.button("🟢 MUDAH", use_container_width=True): start_game("Mudah"); st.rerun()
    if st.button("🟡 SEDANG", use_container_width=True): start_game("Sedang"); st.rerun()
    if st.button("🔴 SULIT", use_container_width=True): start_game("Sulit"); st.rerun()

else:
    if st.sidebar.button("🔙 MENU UTAMA"):
        st.session_state.game_active = False
        st.rerun()

    # Petunjuk Warna
    st.write(f"**Pilihan Warna:**")
    h_cols = st.columns(len(st.session_state.pool))
    for idx, h in enumerate(st.session_state.pool):
        h_cols[idx].markdown(f"<div style='background-color:{WARNA_HEX[h]}; height:10px; border:1px solid white;'></div>", unsafe_allow_html=True)

    st.write("---")

    # SLOT KARTU & TOMBOL HORIZONTAL
    cols = st.columns(st.session_state.max_k)
    for i in range(st.session_state.max_k):
        with cols[i]:
            # Visual Warna
            current_color = WARNA_HEX[st.session_state.guesses[i]]
            st.markdown(f'<div class="card-slot" style="background-color:{current_color};"></div>', unsafe_allow_html=True)
            # Tombol Ganti Warna di bawah masing-masing kartu
            st.button("🔄", key=f"btn_{i}", on_click=ganti_warna, args=(i,))

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
