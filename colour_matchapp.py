import streamlit as st
import random

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Colour Match Master", layout="centered")

# --- 2. CSS CUSTOM (FONT UNIK & DESKRIPSI) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee+Shade&family=Space+Mono:ital,wght@0,400;0,700;1,400;1,700&display=swap');

    #MainMenu, footer, header {visibility: hidden;}
    
    .title-text {
        text-align: center; 
        font-family: 'Bungee Shade', cursive; 
        font-size: 45px; 
        color: white; 
        margin-bottom: 10px;
    }

    .desc-text {
        font-family: 'Space Mono', monospace;
        color: white;
        background-color: rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #555;
        margin-bottom: 30px;
        line-height: 1.6;
    }

    .card-slot {
        position: relative;
        height: 120px;
        width: 100%;
        border-radius: 12px;
        border: 2px solid #555;
        margin-bottom: 10px;
    }

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
    # DESKRIPSI CARA BERMAIN
    st.markdown("""
    <div class="desc-text">
        <strong>🎯 CARA BERMAIN:</strong><br>
        1. Pilih tingkat kesulitan untuk menentukan jumlah kartu.<br>
        2. Klik pada kotak kartu untuk mengganti warnanya.<br>
        3. Gunakan petunjuk warna di bagian atas untuk mengetahui warna apa saja yang mungkin muncul.<br>
        4. Tekan tombol <strong>OK</strong> untuk mengecek tebakanmu.<br>
        5. Perhatikan kalimat riwayat untuk membantumu memecahkan kode warna!
    </div>
    """, unsafe_allow_html=True)

    st.write("### 🕹️ PILIH TINGKAT KESULITAN:")
    c1, c2, c3 = st.columns(3)
    # Gunakan on_click agar state langsung berubah
    c1.button("MUDAH (3)", on_click=start_game, args=("Mudah",), key="m_btn")
    c2.button("SEDANG (4)", on_click=start_game, args=("Sedang",), key="s_btn")
    c3.button("SULIT (5)", on_click=start_game, args=("Sulit",), key="sl_btn")
else:
    # Sidebar untuk reset
    st.sidebar.button("🔙 GANTI LEVEL", on_click=lambda: st.session_state.update({"game_active": False}))

    st.write(f"**Warna yang mungkin muncul ({st.session_state.max_k} kartu):**")
    h_cols = st.columns(len(st.session_state.pool))
    for idx, h in enumerate(st.session_state.pool):
        h_cols[idx].markdown(f"<div style='background-color:{WARNA_HEX[h]}; height:20px; border:1px solid white;'></div>", unsafe_allow_html=True)

    st.write("---")

    # KARTU INTERAKTIF
    cols = st.columns(st.session_state.max_k)
    for i in range(st.session_state.max_k):
        with cols[i]:
            current_color = WARNA_HEX[st.session_state.guesses[i]]
            st.markdown(f'<div class="card-slot" style="background-color:{current_color};"></div>', unsafe_allow_html=True)
            st.button("", key=f"slot_btn_{i}", on_click=ganti_warna, args=(i,))

    st.write("")
    if st.button("CEK JAWABAN (OK) ✅", key="final_ok_btn", use_container_width=True):
        if "Kosong" not in st.session_state.guesses:
            teks = hitung_feedback(st.session_state.guesses, st.session_state.target)
            st.session_state.history.append({'g': list(st.session_state.guesses), 'f': teks})
            if st.session_state.guesses == st.session_state.target:
                st.balloons()
                st.success("🎉 JACKPOT! KAMU MENANG!")

    # RIWAYAT
    if st.session_state.history:
        st.write("### 📜 RIWAYAT:")
        for h in reversed(st.session_state.history):
            st.info(h['f'])
            card_row = "".join([f'<div style="display:inline-block; width:20px; height:30px; background-color:{WARNA_HEX[c]}; margin-right:5px; border:1px solid white;"></div>' for c in h['g']])
            st.markdown(card_row, unsafe_allow_html=True)
