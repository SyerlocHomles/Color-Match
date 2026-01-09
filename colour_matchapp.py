import streamlit as st
import random

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Colour Match Master", layout="centered")

# --- 2. CSS CUSTOM (STABIL & CENTER) ---
st.markdown("""
<style>
    #MainMenu, footer, header {visibility: hidden;}
    .title-text {text-align: center; font-size: 30px; font-weight: bold; color: white; margin-bottom: 5px;}
    .level-text {text-align: center; font-size: 16px; font-weight: bold; color: #FFA500; margin-bottom: 20px;}
    
    /* Tombol Utama */
    .stButton > button {border: 2px solid #555 !important; border-radius: 10px !important; height: 75px !important; width: 100% !important;}
    
    /* Layout Riwayat */
    .history-row {display: flex; flex-direction: row; gap: 12px; padding: 10px 0; border-bottom: 1px solid #333;}
    .column-pair {display: flex; flex-direction: column; align-items: center; width: 35px;}
    .paku-circle {width: 14px; height: 14px; border-radius: 50%; margin-bottom: 6px; border: 1px solid #000;}
    .card-rect {width: 30px; height: 42px; border: 1px solid white; border-radius: 4px;}
</style>
""", unsafe_allow_html=True)

# --- 3. LOGIKA GAME ---
WARNA_LIST = ["Merah", "Oren", "Kuning", "Hijau", "Biru"]
WARNA_HEX = {"Kosong": "#333333", "Merah": "#FF0000", "Oren": "#FFA500", "Kuning": "#FFFF00", "Hijau": "#00FF00", "Biru": "#0000FF"}

if 'level' not in st.session_state:
    st.session_state.level, st.session_state.max_k = 1, 3
    st.session_state.target = random.choices(WARNA_LIST, k=3)
    st.session_state.guesses = ["Kosong"] * 3
    st.session_state.history = []

def tentukan_k(lvl):
    if lvl <= 5: return 3
    if 6 <= lvl <= 10: return 4
    return 5

def ganti_warna(i):
    cur = st.session_state.guesses[i]
    idx = (WARNA_LIST.index(cur) + 1) % len(WARNA_LIST) if cur != "Kosong" else 0
    st.session_state.guesses[i] = WARNA_LIST[idx]

def hitung_paku(guess, target):
    paku = ["Merah"] * len(target)
    t_temp, g_temp = list(target), list(guess)
    for i in range(len(g_temp)):
        if g_temp[i] == t_temp[i]:
            paku[i], t_temp[i], g_temp[i] = "Hijau", None, "DONE"
    for i in range(len(g_temp)):
        if g_temp[i] != "DONE" and g_temp[i] in t_temp:
            paku[i], t_temp[t_temp.index(g_temp[i])] = "Oren", None
    return paku

# --- 4. TAMPILAN ---
st.markdown(f'<div class="title-text">COLOUR MATCH</div>', unsafe_allow_html=True)
st.markdown(f'<div class="level-text">LEVEL {st.session_state.level} ({st.session_state.max_k} KARTU)</div>', unsafe_allow_html=True)

# Hints
hints = sorted(list(set(st.session_state.target)))
h_cols = st.columns(len(hints))
for idx, h in enumerate(hints):
    h_cols[idx].markdown(f"<div style='background-color:{WARNA_HEX[h]}; height:18px; border:1px solid white;'></div>", unsafe_allow_html=True)

st.write("---")

# Buttons
cols = st.columns(st.session_state.max_k)
for i in range(st.session_state.max_k):
    with cols[i]:
        st.button(" ", key=f"b{i}", on_click=ganti_warna, args=(i,), use_container_width=True)
        st.markdown(f"<div style='background-color:{WARNA_HEX[st.session_state.guesses[i]]}; height:10px; border-radius:5px;'></div>", unsafe_allow_html=True)

st.write("")
if st.button("OK", use_container_width=True):
    if "Kosong" not in st.session_state.guesses:
        res = hitung_paku(st.session_state.guesses, st.session_state.target)
        st.session_state.history.append({'g': list(st.session_state.guesses), 'p': res})
        if st.session_state.guesses == st.session_state.target:
            st.balloons()
            st.session_state.level += 1
            st.session_state.max_k = tentukan_k(st.session_state.level)
            st.session_state.target = random.choices(WARNA_LIST, k=st.session_state.max_k)
            st.session_state.guesses, st.session_state.history = ["Kosong"] * st.session_state.max_k, []
            st.rerun()

# --- 5. RIWAYAT (CLEAN HTML) ---
st.write("### Riwayat:")
for h in reversed(st.session_state.history):
    html = '<div class="history-row">'
    for i in range(len(h['g'])):
        html += f'<div class="column-pair"><div class="paku-circle" style="background-color:{WARNA_HEX[h["p"][i]]};"></div><div class="card-rect" style="background-color:{WARNA_HEX[h["g"][i]]};"></div></div>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)
