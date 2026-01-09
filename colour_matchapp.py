import streamlit as st
import random

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Colour Match Master", layout="centered")

# --- 2. CSS CUSTOM ---
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
    # Komputer memilih urutan rahasia
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
    # Buat salinan agar tidak merusak data asli
    t_temp = list(target)
    g_temp = list(guess)
    pos_benar = 0
    warna_salah_pos = 0

    # 1. Hitung Posisi Benar
    for i in range(len(t_temp)):
        if g_temp[i] == t_temp[i]:
            pos_benar += 1
            t_temp[i] = "MATCHED"
            g_temp[i] = "USED"

    # 2. Hitung Benar Warna tapi Salah Posisi
    for i in range(len(g_temp)):
        if g_temp[i] != "USED":
            if g_temp[i] in t_temp:
                warna_salah_pos += 1
                t_temp[t_temp.index(g_temp[i])] = "MATCHED"
                g_temp[i] = "USED"
    
    # 3. Hitung Warna yang Memang Salah (Tidak ada di target)
    warna_salah = len(target) - (pos_benar + warna_salah_pos)
    
    return f"{pos_benar} warna benar & posisi benar, {warna_salah_pos} warna benar tapi salah posisi, {warna_salah} warna salah"

# --- 4. TAMPILAN ---
st.markdown('<div class="title-text">COLOUR MATCH</div>', unsafe_allow_html=True)

if not st.session_state.game_active:
    st.markdown("""
    <div class="desc-text">
        <strong>🎯 CARA BERMAIN:</strong><br>
        1. Pilih tingkat kesulitan di bawah.<br>
        2. Gunakan tombol 'Ganti' di bawah setiap kotak untuk mengubah warna.<br>
        3. Tebak urutan warna rahasia yang disembunyikan komputer.<br>
        4. Tekan tombol OK untuk melihat hasil feedback tebakanmu.<br>
        5. <strong>Posisi Benar</strong> = Warna dan letaknya sudah tepat.<br>
        6. <strong>Salah Posisi</strong> = Warna ada di rahasia, tapi letaknya keliru.
    </div>
    """, unsafe_allow_html=True)

    st.write("### 🕹️ PILIH TINGKAT KESULITAN:")
    if st.button("🟢 MUDAH (3 KARTU)", use_container_width=True): start_game("Mudah"); st.rerun()
    if st.button("🟡 SEDANG (4 KARTU)", use_container_width=True): start_game("Sedang"); st.rerun()
    if st.button("🔴 SULIT (5 KARTU)", use_container_width=True): start_game("Sulit"); st.rerun()

else:
    if st.sidebar.button("🔙 KEMBALI KE MENU"):
        st.session_state.game_active = False
        st.rerun()

    st.write(f"**Warna yang mungkin muncul:**")
    h_cols = st.columns(len(st.session_state.pool))
    for idx, h in enumerate(st.session_state.pool):
        h_cols[idx].markdown(f"<div style='background-color:{WARNA_HEX[h]}; height:10px; border:1px solid white; border-radius:3px;'></div>", unsafe_allow_html=True)

    st.write("---")

    # SLOT KARTU
    cols_cards = st.columns(st.session_state.max_k)
    for i in range(st.session_state.max_k):
        with cols_cards[i]:
            current_color = WARNA_HEX[st.session_state.guesses[i]]
            st.markdown(f'<div class="card-slot" style="background-color:{current_color};"></div>', unsafe_allow_html=True)

    # TOMBOL GANTI (HORIZONTAL)
    cols_btns = st.columns(st.session_state.max_k)
    for i in range(st.session_state.max_k):
        with cols_btns[i]:
            st.button("Ganti", key=f"btn_{i}", on_click=ganti_warna, args=(i,))

    st.markdown('<div class="action-gap"></div>', unsafe_allow_html=True)

    if st.button("CEK JAWABAN (OK) ✅", key="ok_main", use_container_width=True):
        if "Kosong" not in st.session_state.guesses:
            teks = hitung_feedback(st.session_state.guesses, st.session_state.target)
            st.session_state.history.append({'g': list(st.session_state.guesses), 'f': teks})
            if st.session_state.guesses == st.session_state.target:
                st.balloons()
                st.success("🎉 MANTAP! KAMU BERHASIL MENEBAK SEMUANYA!")

    if st.session_state.history:
        st.write("---")
        st.write("### 📜 RIWAYAT TEBAKAN:")
        for h in reversed(st.session_state.history):
            st.info(h['f'])
            card_row = "".join([f'<div style="display:inline-block; width:20px; height:20px; background-color:{WARNA_HEX[c]}; margin-right:8px; border:1px solid white; border-radius:4px;"></div>' for c in h['g']])
            st.markdown(card_row, unsafe_allow_html=True)
            st.write("")
