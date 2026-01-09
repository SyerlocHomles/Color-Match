import streamlit as st
import random

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Colour Match Master", layout="centered")

# --- 2. CSS CUSTOM (STABIL & PRESISI) ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .title-text {
        text-align: center;
        font-size: 32px;
        font-weight: bold;
        color: white;
    }

    .level-text {
        text-align: center;
        font-size: 18px;
        font-weight: bold;
        color: #FFA500;
        margin-bottom: 20px;
    }

    /* Area Riwayat agar Bulatan di Tengah Atas Kartu */
    .history-row {
        display: flex;
        flex-direction: row;
        gap: 15px;
        padding: 10px 0;
        border-bottom: 1px solid #333;
        justify-content: flex-start;
    }

    .column-pair {
        display: flex;
        flex-direction: column;
        align-items: center; /* KUNCI: Paku jadi tengah atas kartu */
        width: 40px;
    }

    .paku-circle {
        width: 14px;
        height: 14px;
        border-radius: 50%;
        margin-bottom: 6px;
        border: 1px solid #000;
    }

    .card-rect {
        width: 32px;
        height: 45px;
        border: 1px solid white;
        border-radius: 4px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. LOGIKA GAME & LEVELING ---
WARNA_LIST = ["Merah", "Oren", "Kuning", "Hijau", "Biru"]
WARNA_HEX = {
    "Kosong": "#333333", "Merah": "#FF0000", "Oren": "#FFA500", 
    "Kuning": "#FFFF00", "Hijau": "#00FF00", "Biru": "#0000FF"
}

if 'level' not in st.session_state:
    st.session_state.level = 1
    st.session_state.max_k = 3
    st.session_state.target = random.choices(WARNA_LIST, k=3)
    st.session_state.guesses = ["Kosong"] * 3
    st.session_state.history = []

def tentukan_jumlah_kartu(lvl):
    if lvl <= 5: return 3
    if 6 <= lvl <= 10: return 4
    return 5

def ganti_warna(i):
    current = st.session_state.guesses[i]
    if current == "Kosong":
        st.session_state.guesses[i] = WARNA_LIST[0]
    else:
        idx = (WARNA_LIST.index(current) + 1) % len(WARNA_LIST)
        st.session_state.guesses[i] = WARNA_LIST[idx]

def hitung_paku(guess, target):
    paku_res = ["Merah"] * len(target)
    t_temp = list(target)
    g_temp = list(guess)
    
    # Hijau: Pas warna & posisi
    for i in range(len(g_temp)):
        if g_temp[i] == t_temp[i]:
            paku_res[i] = "Hijau"
            t_temp[i] = None
            g_temp[i] = "DONE"
    # Oren: Warna ada tapi posisi salah
    for i in range(len(g_temp)):
        if g_temp[i] != "DONE":
            if g_temp[i] in t_temp:
                paku_res[i] = "Oren"
                t_temp[t_temp.index(g_temp[i])] = None
    return paku_res

# --- 4. TAMPILAN ANTARMUKA ---
st.markdown('<div class="title-text">COLOUR MATCH</div>', unsafe_allow_html=True)
st.markdown(f'<div class="level-text">LEVEL {st.session_state.level} ({st.session_state.max_k} KARTU)</div>', unsafe_allow_html=True)

# Hint warna target
hints = sorted(list(set(st.session_state.target)))
h_cols = st.columns(len(hints))
for idx, h in enumerate(hints):
    h_cols[idx].markdown(f"<div style='background-color:{WARNA_HEX[h]}; height:20px; border:1px solid white;'></div>", unsafe_allow_html=True)

st.write("---")

# Area tombol kartu
cols_g = st.columns(st.session_state.max_k)
for i in range(st.session_state.max_k):
    with cols_g[i]:
        c_code = WARNA_HEX[st.session_state.guesses[i]]
        st.button(" ", key=f"btn_{i}", on_click=ganti_warna, args=(i,), use_container_width=True)
        st.markdown(f"<div style='background-color:{c_code}; height:12px; border-radius:5px;'></div>", unsafe_allow_html=True)

st.write("")
_, col_ok = st.columns([4, 1])
with col_ok:
    if st.button("OK", use_container_width=True):
        if "Kosong" not in st.session_state.guesses:
            res_paku = hitung_paku(st.session_state.guesses, st.session_state.target)
            st.session_state.history.append({'g': list(st.session_state.guesses), 'p': res_paku})
            
            # Cek Menang
            if st.session_state.guesses == st.session_state.target:
                st.balloons()
                st.session_state.level += 1
                st.session_state.max_k = tentukan_jumlah_kartu(st.session_state.level)
                st.session_state.target = random.choices(WARNA_LIST, k=st.session_state.max_k)
                st.session_state.guesses = ["Kosong"] * st.session_state.max_k
                st.session_state.history = []
                st.rerun()

# --- 5. RIWAYAT (SOLUSI ANTI-BOCOR & CENTER) ---
st.write("### Riwayat:")
for h in reversed(st.session_state.history):
    # Menggunakan container tunggal untuk satu baris riwayat
    with st.container():
        # Membangun HTML untuk baris tersebut
        html_string = '<div class="history-row">'
        for i in range(len(h['g'])):
            p_color = WARNA_HEX[h['p'][i]]
            c_color = WARNA_HEX[h['g'][i]]
            html_string += f'''
                <div class="column-pair">
                    <div class="paku-circle" style="background-color: {p_color};"></div>
                    <div class="card-rect" style="background-color: {c_color};"></div>
                </div>
            '''
        html_string += '</div>'
        st.markdown(html_string, unsafe_allow_html=True)
