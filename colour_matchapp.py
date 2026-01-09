import streamlit as st
import random

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Colour Match", layout="centered")

# --- CSS UNTUK TAMPILAN SESUAI SKETSA ---
st.markdown("""
    <style>
    .main { background-color: #FFFFFF; }
    .title { text-align: center; font-family: 'Courier New', Courier, monospace; font-weight: bold; font-size: 30px; margin-bottom: 20px; }
    .game-board { border: 3px solid #000; border-radius: 20px; padding: 20px; max-width: 400px; margin: auto; position: relative; }
    .card-slot { width: 55px; height: 85px; border: 2px solid #000; border-radius: 10px; display: inline-block; margin: 5px; }
    .history-card { width: 20px; height: 30px; border: 1px solid #000; display: inline-block; margin: 2px; }
    .paku { width: 12px; height: 12px; border-radius: 50%; border: 1px solid #000; display: inline-block; margin: 2px; }
    .stButton>button { width: 100%; border-radius: 20px; border: 2px solid #000; font-weight: bold; background-color: white; }
    </style>
""", unsafe_allow_html=True)

# --- SISTEM LOGIKA GAME ---
WARNA_MAP = {
    "Kosong": "#F0F0F0", "Merah": "#FF0000", "Oren": "#FFA500", 
    "Kuning": "#FFFF00", "Hijau": "#00FF00", "Biru": "#0000FF", "Abu-abu": "#808080"
}
LIST_WARNA = ["Merah", "Oren", "Kuning", "Hijau", "Biru"]

if 'target' not in st.session_state:
    st.session_state.max_k = 3 # Mulai dari level 3 kartu
    st.session_state.target = random.choices(LIST_WARNA, k=st.session_state.max_k)
    st.session_state.guesses = ["Kosong"] * st.session_state.max_k
    st.session_state.history = []

def hitung_paku(guess, target):
    paku = []
    t_count = {w: target.count(w) for w in LIST_WARNA}
    g_count = {w: 0 for w in LIST_WARNA}
    
    # 1. Hijau (Posisi & Warna Benar)
    matched_idx = []
    for i in range(len(guess)):
        if guess[i] == target[i]:
            paku.append("Hijau")
            g_count[guess[i]] += 1
            matched_idx.append(i)
            
    # 2. Oren & Abu-abu
    for i in range(len(guess)):
        if i not in matched_idx:
            if guess[i] in target:
                if g_count[guess[i]] < t_count[guess[i]]:
                    paku.append("Oren")
                    g_count[guess[i]] += 1
                else:
                    paku.append("Abu-abu") # Benar warna, tapi kuota habis
            else:
                paku.append("Merah")
    
    while len(paku) < len(target): paku.append("Merah")
    return sorted(paku) # Agar posisi paku tidak membocorkan posisi kartu

# --- TAMPILAN ---
st.markdown("<div class='title'>COLOUR MATCH</div>", unsafe_allow_html=True)

with st.container():
    st.markdown("<div class='game-board'>", unsafe_allow_html=True)
    
    # Header: Info Kartu & Hint Warna (Sesuai Sketsa)
    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown(f"### {len(st.session_state.target)} KARTU")
    with c2:
        hints = sorted(list(set(st.session_state.target)))
        cols = st.columns(len(hints))
        for i, h in enumerate(hints):
            cols[i].markdown(f"<div style='background-color:{WARNA_MAP[h]}; height:25px; border:2px solid #000;'></div>", unsafe_allow_html=True)

    st.write("---")

    # Slot Tebakan (5 Kotak Kosong/Klik untuk ganti warna)
    cols_g = st.columns(st.session_state.max_k)
    for i in range(st.session_state.max_k):
        with cols_g[i]:
            if st.button("🔄", key=f"btn_{i}"):
                cur = st.session_state.guesses[i]
                next_w = LIST_WARNA[0] if cur == "Kosong" else LIST_WARNA[(LIST_WARNA.index(cur)+1)%5]
                st.session_state.guesses[i] = next_w
            st.markdown(f"<div class='card-slot' style='background-color:{WARNA_MAP[st.session_state.guesses[i]]};'></div>", unsafe_allow_html=True)

    # Tombol OK
    if st.button("OK"):
        if "Kosong" not in st.session_state.guesses:
            paku_res = hitung_paku(st.session_state.guesses, st.session_state.target)
            st.session_state.history.append({'g': list(st.session_state.guesses), 'p': paku_res})
            
            if st.session_state.guesses == st.session_state.target:
                st.success("BERHASIL!")
                if st.session_state.max_k < 5: st.session_state.max_k += 1
                st.session_state.target = random.choices(LIST_WARNA, k=st.session_state.max_k)
                st.session_state.guesses = ["Kosong"] * st.session_state.max_k
                st.session_state.history = []
                st.rerun()

    # Riwayat Tebakan
    st.markdown("<strong>Riwayat:</strong>", unsafe_allow_html=True)
    for h in reversed(st.session_state.history):
        col_p, col_c = st.columns([1, 2])
        with col_p:
            for p in h['p']:
                st.markdown(f"<div class='paku' style='background-color:{WARNA_MAP[p]};'></div>", unsafe_allow_html=True)
        with col_c:
            for w in h['g']:
                st.markdown(f"<div class='history-card' style='background-color:{WARNA_MAP[w]};'></div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

if st.sidebar.button("Reset Game"):
    st.session_state.clear()
    st.rerun()
