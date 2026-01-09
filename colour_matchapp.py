import streamlit as st
import random

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Colour Match Pro", layout="centered")

# --- CSS CUSTOM (PERBAIKAN VISUAL & PENYELARASAN PAKU) ---
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
        margin-bottom: 10px;
    }

    .level-text {
        text-align: center;
        font-size: 18px;
        color: #FFA500;
        margin-bottom: 20px;
    }

    .stButton > button {
        border: 2px solid #555 !important;
        border-radius: 10px !important;
        height: 80px !important;
        width: 100% !important;
    }
    
    .ok-button > div > button {
        background-color: white !important;
        color: black !important;
        border: 2px solid black !important;
        font-weight: bold !important;
        width: 100% !important;
    }

    /* Container untuk menyelaraskan paku tepat di atas kartu */
    .history-item-container {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        margin-bottom: 20px;
        padding-bottom: 10px;
        border-bottom: 1px solid #333;
    }

    .row-visual {
        display: flex;
        gap: 10px; /* Jarak antar kolom (paku + kartu) */
    }

    .column-pair {
        display: flex;
        flex-direction: column;
        align-items: center; /* MEMBUAT PAKU DI TENGAH ATAS KARTU */
        width: 30px; /* Lebar tetap agar paku dan kartu sinkron vertikal */
    }

    .paku-circle {
        width: 14px;
        height: 14px;
        border-radius: 50%;
        margin-bottom: 5px;
        border: 1px solid #111;
    }

    .card-rect {
        width: 25px;
        height: 35px;
        border: 1px solid white;
    }
    </style>
""", unsafe_allow_html=True)

# --- LOGIKA GAME & LEVELING ---
WARNA_LIST = ["Merah", "Oren", "Kuning", "Hijau", "Biru"]
WARNA_HEX = {
    "Kosong": "#333333", "Merah": "#FF0000", "Oren": "#FFA500", 
    "Kuning": "#FFFF00", "Hijau": "#00FF00", "Biru": "#0000FF"
}

# Inisialisasi State
if 'level' not in st.session_state:
    st.session_state.level = 1
    st.session_state.max_k = 3
    st.session_state.target = random.choices(WARNA_LIST, k=st.session_state.max_k)
    st.session_state.guesses = ["Kosong"] * st.session_state.max_k
    st.session_state.history = []

def update_level_logic():
    """Mengatur jumlah kartu berdasarkan level saat ini"""
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
    
    # Hijau: Posisi & Warna Benar
    for i in range(len(g_temp)):
        if g_temp[i] == t_temp[i]:
            paku_result[i] = "Hijau"
            t_temp[i] = None
            g_temp[i] = "DONE"
            
    # Oren: Warna Benar, Posisi Salah
    for i in range(len(g_temp)):
        if g_temp[i] != "DONE":
            if g_temp[i] in t_temp:
                paku_result[i] = "Oren"
                t_temp[t_temp.index(g_temp[i])] = None
                
    return paku_result

# --- TAMPILAN UTAMA ---

st.markdown('<div class="title-text">COLOUR MATCH</div>', unsafe_allow_html=True)
st.markdown(f'<div class="level-text">LEVEL {st.session_state.level} ({st.session_state.max_k} KARTU)</div>', unsafe_allow_html=True)

# Hint Warna
hints = sorted(list(set(st.session_state.target)))
h_cols = st.columns(len(hints) if len(hints) > 0 else 1)
for idx, h in enumerate(hints):
    h_cols[idx].markdown(f"<div style='background-color:{WARNA_HEX[h]}; height:20px; border:1px solid white; border-radius:3px;'></div>", unsafe_allow_html=True)

st.write("---")

# Area Tebakan (Dibuat Dinamis)
cols_g = st.columns(st.session_state.max_k)
for i in range(st.session_state.max_k):
    with cols_g[i]:
        color = WARNA_HEX[st.session_state.guesses[i]]
        st.button(" ", key=f"btn_{i}", on_click=ganti_warna, args=(i,), use_container_width=True)
        st.markdown(f"<div style='background-color:{color}; height:10px; border-radius:5px;'></div>", unsafe_allow_html=True)

# Tombol OK
st.write("")
_, col_ok = st.columns([3, 1])
with col_ok:
    st.markdown('<div class="ok-button">', unsafe_allow_html=True)
    if st.button("OK"):
        if "Kosong" not in st.session_state.guesses:
            res = hitung_paku(st.session_state.guesses, st.session_state.target)
            st.session_state.history.append({'g': list(st.session_state.guesses), 'p': res})
            
            # Cek Menang
            if st.session_state.guesses == st.session_state.target:
                st.balloons()
                st.session_state.level += 1
                update_level_logic()
                st.session_state.target = random.choices(WARNA_LIST, k=st.session_state.max_k)
                st.session_state.guesses = ["Kosong"] * st.session_state.max_k
                st.session_state.history = []
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- RIWAYAT (PERBAIKAN BUG POSISI PAKU) ---
st.write("### Riwayat:")
for h in reversed(st.session_state.history):
    # Menggunakan HTML/CSS untuk memastikan paku tepat di atas kartu secara center
    item_html = '<div class="history-item-container"><div class="row-visual">'
    
    # Looping per kolom (Paku + Kartu di bawahnya)
    for i in range(len(h['g'])):
        warna_paku = WARNA_HEX[h['p'][i]]
        warna_kartu = WARNA_HEX[h['g'][i]]
        
        item_html += f'''
            <div class="column-pair">
                <div class="paku-circle" style="background-color: {warna_paku};"></div>
                <div class="card-rect" style="background-color: {warna_kartu};"></div>
            </div>
        '''
    
    item_html += '</div></div>'
    st.markdown(item_html, unsafe_allow_html=True)
