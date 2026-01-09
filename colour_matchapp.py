import streamlit as st
import random

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Colour Match Master", layout="centered")

# --- 2. CSS CUSTOM (STYLING HP OPTIMIZED) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee+Shade&family=Space+Mono:wght@400;700&display=swap');

    #MainMenu, footer, header {visibility: hidden;}
    
    .title-text {
        text-align: center; 
        font-family: 'Bungee Shade', cursive; 
        font-size: 28px; 
        color: white; 
        margin-bottom: 10px;
    }

    .desc-text {
        font-family: 'Space Mono', monospace;
        color: white;
        background-color: rgba(255, 255, 255, 0.1);
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #555;
        margin-bottom: 20px;
        font-size: 12px;
        line-height: 1.6;
    }

    .card-slot {
        height: 50px;
        width: 100%;
        border-radius: 8px;
        border: 2px solid #555;
        margin-bottom: 8px;
    }

    /* Jarak antara baris tombol ganti dengan tombol OK */
    .action-gap {
        margin-bottom: 30px;
    }

    .stButton > button {
        font-size: 11px !important;
        border-radius: 6px !important;
        height: 35px !important;
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
    posisi_benar, warna_benar_salah_posisi = 0, 0
    
    # 1. Cek Warna Benar & Posisi Benar
    for i in range(len(t_temp)):
        if g_temp[i] == t_temp[i]:
            posisi_benar += 1
            t_temp[i], g_temp[i] = "DONE_T", "DONE_G"
            
    # 2. Cek Warna Benar tapi Salah Posisi
    for i in range(len(g_temp)):
        if g_temp[i] != "DONE_G" and g_temp[i] in t_temp:
            warna_benar_salah_posisi += 1
            t_temp[t_temp.index(g_temp[i])] = "DONE_T"
            
    warna_salah = len(target) - (posisi_benar + warna_benar_salah_posisi)
    
    return f"{posisi_benar} warna benar & posisi benar, {warna_benar_salah_posisi} warna benar tapi salah posisi, {warna_salah} warna salah"

# --- 4. TAMPILAN ---
st.markdown('<div class="title-text">COLOUR MATCH</div>', unsafe_allow_html=True)

if not st.session_state.game_active:
    st.markdown("""
    <div class="desc-text">
        <strong>🎯 CARA BERMAIN:</strong><br>
        1. Pilih tingkat kesulitan di bawah.<br>
        2. Gunakan tombol 'Ganti' untuk mengubah warna kartu.<br>
        3. Tebak urutan warna rahasia yang dipilih komputer.<br>
        4. Tekan tombol OK untuk melihat hasil feedback.<br>
        5. Warna & Posisi Benar = Tepat sasaran.<br>
        6. Warna Benar Salah Posisi = Ada warnanya tapi salah letak.
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

    st.write(f"**Pilihan Warna:**")
    h_cols = st.columns(len(st.session_state.pool))
    for idx, h in enumerate(st.session_state.pool):
        h_cols[idx].markdown(f"<div style='background-color:{WARNA_HEX[h]}; height:10px; border:1px solid white;'></div>", unsafe_allow_html=True)

    st.write("---")

    # BARIS KARTU
    cols_cards = st.columns(st.session_state.max_k)
    for i in range(st.session_state.max_k):
        with cols_cards[i]:
            current_color = WARNA_HEX[st.session_state.guesses[i]]
            st.markdown(f'<div class="card-slot" style="background-color:{current_color};"></div>', unsafe_allow_html=True)

    # BARIS TOMBOL GANTI (Horizontal di bawah kartu)
    cols_btns = st.columns(st.session_state.max_k)
    for i in range(st.session_state.max_k):
        with cols_btns[i]:
            st.button("Ganti", key=f"btn_{i}", on_click=ganti_warna, args=(i,))

    st.markdown('<div class="action-gap"></div>', unsafe_allow_html=True)

    # TOMBOL OK
    if st.button("CEK JAWABAN (OK) ✅", key="ok_main", use_container_width=True):
        if "Kosong" not in st.session_state.guesses:
            teks = hitung_feedback(st.session_state.guesses, st.session_state.target)
            st.session_state.history.append({'g': list(st.session_state.guesses), 'f': teks})
            if st.session_state.guesses == st.session_state.target:
                st.balloons()
                st.success("🎉 JACKPOT! KAMU MENANG!")

    if st.session_state.history:
        st.write("---")
        st.write("### 📜 RIWAYAT:")
        for h in reversed(st.session_state.history):
            st.info(h['f'])
            card_row = "".join([f'<div style="display:inline-block; width:15px; height:15px; background-color:{WARNA_HEX[c]}; margin-right:5px; border:1px solid white;"></div>' for c in h['g']])
            st.markdown(card_row, unsafe_allow_html=True)
