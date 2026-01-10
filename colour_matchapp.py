import streamlit as st
import random

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Colour Match Master", layout="centered")

# --- 2. CSS CUSTOM ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee+Shade&family=Bungee&family=Space+Mono:wght@400;700&display=swap');
    #MainMenu, footer, header {visibility: hidden;}
    .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }

    @keyframes pulse {
        0% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.05); opacity: 0.9; }
        100% { transform: scale(1); opacity: 1; }
    }

    .win-text {
        text-align: center; font-family: 'Bungee', cursive;
        font-size: 36px; color: #FFD700;
        text-shadow: 0 0 15px rgba(255, 215, 0, 0.7);
        animation: pulse 1s infinite; margin-top: 10px;
    }

    [data-testid="stHorizontalBlock"] {
        display: grid !important;
        grid-template-columns: repeat(auto-fit, minmax(0, 1fr)) !important;
        gap: 6px !important; width: 100% !important;
    }

    .card-slot {
        aspect-ratio: 2 / 3.2; width: 100%;
        border-radius: 8px; border: 2px solid #ffffff;
        margin-bottom: 5px;
    }

    .stButton > button {
        width: 100% !important; font-size: 9px !important;
        height: 32px !important; white-space: nowrap !important;
    }

    .cek-area .stButton > button {
        width: 100% !important; height: 50px !important;
        font-size: 16px !important; font-weight: bold !important;
        background-color: #262730 !important; border: 2px solid #FFD700 !important;
        color: white !important; border-radius: 10px !important; margin-top: 15px;
    }

    .title-text {
        text-align: center; font-family: 'Bungee Shade', cursive; 
        font-size: 24px; color: white; margin-bottom: 10px;
    }

    .pool-container { display: flex; justify-content: center; gap: 8px; margin-bottom: 15px; }
    .pool-box { width: 18px; height: 18px; border-radius: 4px; border: 1px solid #fff; }
</style>
""", unsafe_allow_html=True)

# --- 3. LOGIKA GAME ---
WARNA_LIST = ["Merah", "Oren", "Kuning", "Hijau", "Biru"]
WARNA_HEX = {"Kosong": "#333333", "Merah": "#FF0000", "Oren": "#FFA500", "Kuning": "#FFFF00", "Hijau": "#00FF00", "Biru": "#0000FF"}

if 'game_active' not in st.session_state:
    st.session_state.game_active = False

def start_game(mode):
    k, ch = (3, 5) if mode == "Mudah" else (4, 8) if mode == "Sedang" else (5, 10)
    full_pool = random.sample(WARNA_LIST, k) 
    target = [random.choice(full_pool) for _ in range(k)]
    st.session_state.display_pool = sorted(list(set(target)))
    st.session_state.selection_pool = full_pool 
    st.session_state.target = target
    st.session_state.max_k = k
    st.session_state.guesses = ["Kosong"] * k
    st.session_state.history = []
    st.session_state.chances = ch
    st.session_state.game_active = True
    st.session_state.game_over = False
    st.session_state.won = False

def ganti_warna(i):
    if not st.session_state.game_over:
        pool = st.session_state.selection_pool
        cur = st.session_state.guesses[i]
        next_idx = (pool.index(cur) + 1) % len(pool) if cur in pool else 0
        st.session_state.guesses[i] = pool[next_idx]

# --- 4. TAMPILAN ---
st.markdown('<div class="title-text">COLOUR MATCH</div>', unsafe_allow_html=True)

# FITUR BARU: INSTRUKSI TETAP ADA DI DALAM EXPANDER
with st.expander("📖 Cara Bermain (Klik untuk Baca)"):
    st.write("""
    1. Tebak urutan warna rahasia di atas.
    2. Klik tombol **Ganti** di bawah setiap kotak untuk memilih warna.
    3. Warna rahasia **HANYA** terdiri dari warna yang muncul di kotak kecil.
    4. **X Benar** = Jumlah warna yang sudah tepat di posisi yang benar.
    """)

if not st.session_state.game_active:
    st.markdown('<div style="text-align:center; color:white; margin-bottom:10px;">PILIH LEVEL:</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: 
        if st.button("🟢 MUDAH"): start_game("Mudah"); st.rerun()
    with c2: 
        if st.button("🟡 SEDANG"): start_game("Sedang"); st.rerun()
    with c3: 
        if st.button("🔴 SULIT"): start_game("Sulit"); st.rerun()
else:
    # Header Status Game
    if st.session_state.won:
        st.balloons()
        st.markdown('<div class="win-text">✨ YOU WIN! ✨</div>', unsafe_allow_html=True)
    elif st.session_state.game_over:
        st.error(f"❌ Jawabannya: {', '.join(st.session_state.target)}")

    st.markdown(f'<div style="text-align:center; color:#FF4B4B; font-weight:bold; font-size:18px;">Sisa: {st.session_state.chances}x</div>', unsafe_allow_html=True)
    
    # Petunjuk Warna Rahasia
    if 'display_pool' in st.session_state:
        pool_html = '<div class="pool-container">'
        for p_color in st.session_state.display_pool:
            pool_html += f'<div class="pool-box" style="background-color:{WARNA_HEX[p_color]};"></div>'
        pool_html += '</div>'
        st.markdown(pool_html, unsafe_allow_html=True)

    # Area Game
    cols = st.columns(st.session_state.max_k)
    for i in range(st.session_state.max_k):
        with cols[i]:
            st.markdown(f'<div class="card-slot" style="background-color:{WARNA_HEX.get(st.session_state.guesses[i], "#333333")};"></div>', unsafe_allow_html=True)
            st.button("Ganti", key=f"btn_{i}", on_click=ganti_warna, args=(i,))

    # Tombol Cek / Reset
    st.markdown('<div class="cek-area">', unsafe_allow_html=True)
    if not st.session_state.game_over:
        if st.button("Cek Jawaban", use_container_width=True):
            if "Kosong" not in st.session_state.guesses:
                st.session_state.chances -= 1
                b_pos = sum(1 for g, t in zip(st.session_state.guesses, st.session_state.target) if g == t)
                st.session_state.history.append({'g': list(st.session_state.guesses), 'f': f"{b_pos} Benar"})
                if st.session_state.guesses == st.session_state.target:
                    st.session_state.won = True; st.session_state.game_over = True
                elif st.session_state.chances <= 0:
                    st.session_state.game_over = True
                st.rerun()
    else:
        if st.button("Main Lagi", use_container_width=True):
            st.session_state.game_active = False; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Riwayat
    if st.session_state.history:
        st.markdown("---")
        for h in reversed(st.session_state.history):
            st.info(h['f'])
            row_html = "".join([f'<div style="display:inline-block; width:18px; height:18px; background-color:{WARNA_HEX[c]}; margin-right:6px; border:1px solid white; border-radius:3px;"></div>' for c in h['g']])
            st.markdown(row_html, unsafe_allow_html=True)
