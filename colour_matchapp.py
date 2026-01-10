import streamlit as st
import random

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Colour Match Master", layout="centered")

# --- 2. CSS CUSTOM (FIX LAYOUT & FONT) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee+Shade&family=Space+Mono:wght@400;700&display=swap');
    #MainMenu, footer, header {visibility: hidden;}
    
    /* Memaksa kolom tetap horizontal di HP untuk kartu dan tombol */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 5px !important;
    }

    .title-text {
        text-align: center; font-family: 'Bungee Shade', cursive; 
        font-size: 26px; color: white; margin-bottom: 10px;
    }

    .desc-text {
        font-family: 'Space Mono', monospace; color: white;
        background-color: rgba(255, 255, 255, 0.1); padding: 15px;
        border-radius: 12px; border: 1px solid #555;
        margin-bottom: 20px; font-size: 12px; line-height: 1.6;
    }

    .card-slot {
        height: 40px; width: 100%; border-radius: 5px;
        border: 1px solid #fff; margin-bottom: 5px;
    }

    .stButton > button {
        font-size: 9px !important; padding: 0px !important;
        height: 30px !important; border-radius: 4px !important;
        white-space: normal !important;
    }

    .chance-text {
        text-align: center; font-size: 18px; font-weight: bold;
        color: #FF4B4B; margin-bottom: 10px;
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
    st.session_state.chances = 5 # Set kesempatan 5x
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
    return f"{b_pos} warna benar & posisi benar, {b_warna} warna benar tapi salah posisi, {salah} warna salah"

# --- 4. TAMPILAN ---
st.markdown('<div class="title-text">COLOUR MATCH</div>', unsafe_allow_html=True)

if not st.session_state.game_active:
    st.markdown("""
    <div class="desc-text">
        <strong>🎯 CARA BERMAIN:</strong><br>
        1. Pilih tingkat kesulitan di bawah.<br>
        2. Gunakan tombol 'Ganti Warna' di bawah kotak.<br>
        3. Kamu hanya punya 5 kesempatan menebak!<br>
        4. Tekan tombol CEK JAWABAN untuk melihat hasil.<br>
        5. <b>Posisi Benar</b>: Warna & letak tepat.<br>
        6. <b>Salah Posisi</b>: Warna ada, tapi letak salah.
    </div>
    """, unsafe_allow_html=True)
    if st.button("🟢 MUDAH (3 KARTU)", use_container_width=True): start_game("Mudah"); st.rerun()
    if st.button("🟡 SEDANG (4 KARTU)", use_container_width=True): start_game("Sedang"); st.rerun()
    if st.button("🔴 SULIT (5 KARTU)", use_container_width=True): start_game("Sulit"); st.rerun()
else:
    if st.sidebar.button("🔙 MENU UTAMA"):
        st.session_state.game_active = False
        st.rerun()

    # Menampilkan Sisa Kesempatan
    st.markdown(f'<div class="chance-text">Sisa Kesempatan: {st.session_state.chances}x</div>', unsafe_allow_html=True)

    # Area Bermain (Kartu dan Tombol)
    cols = st.columns(st.session_state.max_k)
    for i in range(st.session_state.max_k):
        with cols[i]:
            st.markdown(f'<div class="card-slot" style="background-color:{WARNA_HEX[st.session_state.guesses[i]]};"></div>', unsafe_allow_html=True)
            st.button("Ganti Warna", key=f"g_{i}", on_click=ganti_warna, args=(i,))

    st.write("")
    
    # Tombol Cek Jawaban
    if not st.session_state.game_over:
        if st.button("CEK JAWABAN ✅", use_container_width=True):
            if "Kosong" not in st.session_state.guesses:
                st.session_state.chances -= 1
                fb = hitung_feedback(st.session_state.guesses, st.session_state.target)
                st.session_state.history.append({'g': list(st.session_state.guesses), 'f': fb})
                
                if st.session_state.guesses == st.session_state.target:
                    st.balloons()
                    st.success("🎉 JACKPOT! KAMU MENANG!")
                    st.session_state.game_over = True
                elif st.session_state.chances <= 0:
                    st.error(f"❌ GAME OVER! Jawaban benar: {', '.join(st.session_state.target)}")
                    st.session_state.game_over = True
                st.rerun()

    # Riwayat
    if st.session_state.history:
        st.write("---")
        st.write("### 📜 RIWAYAT:")
        for h in reversed(st.session_state.history):
            st.info(h['f'])
            row = "".join([f'<div style="display:inline-block; width:15px; height:15px; background-color:{WARNA_HEX[c]}; margin-right:5px; border:1px solid white; border-radius:3px;"></div>' for c in h['g']])
            st.markdown(row, unsafe_allow_html=True)
