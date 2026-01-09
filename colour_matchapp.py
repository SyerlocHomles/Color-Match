import streamlit as st
import random

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Colour Match Pro", layout="centered")

# --- CSS CUSTOM (VERSI STABIL) ---
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
        margin-bottom: 5px;
    }

    .level-text {
        text-align: center;
        font-size: 18px;
        font-weight: bold;
        color: #FFA500;
        margin-bottom: 20px;
    }

    /* Tombol Tebakan */
    .stButton > button {
        border: 2px solid #555 !important;
        border-radius: 10px !important;
        height: 80px !important;
        width: 100% !important;
    }
    
    /* Tombol OK */
    .ok-button-container {
        display: flex;
        justify-content: flex-end;
        margin-top: 20px;
    }

    /* CSS untuk Riwayat agar Bulatan di Tengah Atas Kartu */
    .history-container {
        display: flex;
        flex-direction: column;
        gap: 15px;
        margin-top: 20px;
    }

    .history-row {
        display: flex;
        flex-direction: row;
        gap: 12px;
        padding: 10px;
        border-bottom: 1px solid #333;
    }

    .column-pair {
        display: flex;
        flex-direction: column;
        align-items: center; /* Paku jadi tengah atas */
        width: 35px;
    }

    .paku-circle {
        width: 14px;
        height: 14px;
        border-radius: 50%;
        margin-bottom: 6px;
        border: 1px solid #000;
    }

    .card-rect {
        width: 30px;
        height: 40px;
        border: 1px solid white;
        border-radius: 4px;
    }
    </style>
""", unsafe_allow_html=True)

# --- LOGIKA GAME & LEVEL ---
WARNA_LIST = ["Merah", "Oren", "Kuning", "Hijau", "Biru"]
WARNA_HEX = {
    "Kosong": "#333333", "Merah": "#FF0000", "Oren": "#FFA500", 
    "Kuning": "#FFFF00", "Hijau": "#00FF00", "Biru": "#0000FF"
}

if 'level' not in st.session_state:
    st.session_state.level = 1
    st.session_state.max_k = 3
    st.session_state.target = random.choices(WARNA_LIST, k=st.session_state.max_k)
    st.session_state.guesses = ["Kosong"] * st.session_state.max_k
    st.session_state.history = []

def update_game_difficulty():
    """Update jumlah kartu berdasarkan level tebakan user"""
    if st.session_state.level <= 5:
        st.session_state.max_k = 3
    elif 6 <= st.session_state.level <= 10:
        st.session_state.max_k = 4
    else:
        st.session_state.max_k = 5

def ganti_warna(i):
    current = st.session_state.guesses[i]
    if current == "Kosong":
        st.session_state.guesses[i] = WARNA_LIST[0]
    else:
        idx = (WARNA_LIST.index(current) + 1) % len(WARNA_LIST)
        st.session_state.guesses[i] = WARNA_LIST[idx]

def hitung_paku(guess, target):
    paku_result = ["Merah"] * len(target)
    t_temp = list(target)
    g_temp = list(guess)
    
    # 1. Hijau (Posisi & Warna Benar)
    for i in range(len(g_temp)):
        if g_temp[i] == t_temp[i]:
            paku_result[i] = "Hijau"
            t_temp[i] = None
            g_temp[i] = "DONE"
            
    # 2. Oren (Warna Benar, Posisi Salah)
    for i in range(len(g_temp)):
        if g_temp[i] != "DONE":
            if g_temp[i] in t_temp:
                paku_result[i] = "Oren"
                t_temp[t_temp.index(g_temp[i])] = None
                
    return paku_result

# --- TAMPILAN ---
st.markdown('<div class="title-text">COLOUR MATCH</div>', unsafe_allow_html=True)
st.markdown(f'<div class="level-text">LEVEL {st.session_state.level} ({st.session_state.max_k} KARTU)</div>', unsafe_allow_html=True)

# Hint Warna yang Ada (Target)
hints = sorted(list(set(st.session_state.target)))
h_cols = st.columns(len(hints) if len(hints) > 0 else 1)
for idx, h in enumerate(hints):
    h_cols[idx].markdown(f"<div style='background-color:{WARNA_HEX[h]}; height:20px; border:1px solid white; border-radius:3px;'></div>", unsafe_allow_html=True)

st.write("---")

# Area Klik Kartu
cols_g = st.columns(st.session_state.max_k)
for i in range(st.session_state.max_k):
    with cols_g[i]:
        color_code = WARNA_HEX[st.session_state.guesses[i]]
        st.button(" ", key=f"btn_{i}", on_click=ganti_warna, args=(i,), use_container_width=True)
        st.markdown(f"<div style='background-color:{color_code}; height:12px; border-radius:5px;'></div>", unsafe_allow_html=True)

# Tombol OK
st.write("")
col_space, col_btn = st.columns([4, 1])
with col_btn:
    if st.button("OK", use_container_width=True):
        if "Kosong" not in st.session_state.guesses[:st.session_state.max_k]:
            res = hitung_paku(st.session_state.guesses[:st.session_state.max_k], st.session_state.target)
            st.session_state.history.append({
                'g': list(st.session_state.guesses[:st.session_state.max_k]), 
                'p': res
            })
            
            # Cek Kemenangan
            if st.session_state.guesses[:st.session_state.max_k] == st.session_state.target:
                st.balloons()
                st.session_state.level += 1
                update_game_difficulty()
                st.session_state.target = random.choices(WARNA_LIST, k=st.session_state.max_k)
                st.session_state.guesses = ["Kosong"] * st.session_state.max_k
                st.session_state.history = [] # Reset riwayat tiap naik level
                st.rerun()

# --- BAGIAN RIWAYAT (FIX VISUAL) ---
st.write("### Riwayat:")

# Bungkus seluruh riwayat dalam satu blok HTML agar tidak pecah jadi teks
history_html = '<div class="history-container">'

for h in reversed(st.session_state.history):
    history_html += '<div class="history-row">'
    
    for i in range(len(h['g'])):
        p_color = WARNA_HEX[h['p'][i]]
        c_color = WARNA_HEX[h['g'][i]]
        
        history_html += f'''
            <div class="column-pair">
                <div class="paku-circle" style="background-color: {p_color};"></div>
                <div class="card-rect" style="background-color: {c_color};"></div>
            </div>
        '''
    history_html += '</div>'

history_html += '</div>'
st.markdown(history_html, unsafe_allow_html=True)
