import streamlit as st
import random

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Colour Match", layout="centered")

# --- CSS CUSTOM UNTUK MEMPERBAIKI TAMPILAN (FIX BUG & LAYOUT) ---
st.markdown("""
    <style>
    /* Menghilangkan elemen default Streamlit yang mengganggu */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Judul Tengah Atas */
    .title-text {
        text-align: center;
        font-size: 32px;
        font-weight: bold;
        color: white;
        margin-bottom: 20px;
    }

    /* Container Kartu & Info */
    .info-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
    }

    /* Kotak Tebakan (Tombol Transparan di Atas Warna) */
    .stButton > button {
        border: 2px solid #555 !important;
        border-radius: 10px !important;
        height: 100px !important;
        width: 100% !important;
        transition: 0.1s;
    }
    
    /* Tombol OK Hitam */
    .ok-button > div > button {
        background-color: white !important;
        color: black !important;
        border: 2px solid black !important;
        height: 40px !important;
        width: 80px !important;
        font-weight: bold !important;
    }

    /* Style untuk Paku Bulat */
    .paku {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 4px;
        border: 1px solid #333;
    }

    /* Riwayat Horizontal */
    .history-row {
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 10px;
        padding: 5px;
        border-bottom: 1px solid #333;
    }
    
    .history-card {
        width: 20px;
        height: 30px;
        border: 1px solid white;
    }
    </style>
""", unsafe_allow_html=True)

# --- LOGIKA GAME ---
WARNA_LIST = ["Merah", "Oren", "Kuning", "Hijau", "Biru"]
WARNA_HEX = {
    "Kosong": "#333333", "Merah": "#FF0000", "Oren": "#FFA500", 
    "Kuning": "#FFFF00", "Hijau": "#00FF00", "Biru": "#0000FF", "Abu-abu": "#808080"
}

if 'target' not in st.session_state:
    st.session_state.max_k = 3
    st.session_state.target = random.choices(WARNA_LIST, k=st.session_state.max_k)
    st.session_state.guesses = ["Kosong"] * st.session_state.max_k
    st.session_state.history = []

def ganti_warna(i):
    current = st.session_state.guesses[i]
    if current == "Kosong":
        st.session_state.guesses[i] = WARNA_LIST[0]
    else:
        idx = (WARNA_LIST.index(current) + 1) % len(WARNA_LIST)
        st.session_state.guesses[i] = WARNA_LIST[idx]

def hitung_paku(guess, target):
    paku = []
    t_temp = list(target)
    g_temp = list(guess)
    
    # 1. Hijau (Benar Posisi & Warna)
    idx_done = []
    for i in range(len(g_temp)):
        if g_temp[i] == t_temp[i]:
            paku.append("Hijau")
            t_temp[i] = None
            g_temp[i] = "DONE"
            idx_done.append(i)
            
    # 2. Oren & Abu-abu
    for i in range(len(g_temp)):
        if g_temp[i] != "DONE":
            if g_temp[i] in t_temp:
                paku.append("Oren")
                t_temp[t_temp.index(g_temp[i])] = None
            else:
                paku.append("Merah")
    
    # Sisa paku abu-abu jika warna benar tapi posisi sudah terpakai semua (Mastermind Logic)
    # Untuk menyederhanakan sesuai permintaanmu, merah jika salah total.
    return sorted(paku, reverse=True) # Hijau dulu, lalu Oren, lalu Merah

# --- TAMPILAN SESUAI INSTRUKSI ---

# 1. Judul Tengah Atas
st.markdown('<div class="title-text">COLOUR MATCH</div>', unsafe_allow_html=True)

# 3 & 4. Info Kartu & Hint Warna
col_info, col_hints = st.columns([1, 2])
with col_info:
    st.subheader(f"{st.session_state.max_k} KARTU")
with col_hints:
    hints = sorted(list(set(st.session_state.target)))
    h_cols = st.columns(len(hints))
    for idx, h in enumerate(hints):
        h_cols[idx].markdown(f"<div style='background-color:{WARNA_HEX[h]}; height:25px; border:1px solid white;'></div>", unsafe_allow_html=True)

st.write("---")

# 5. 5 Kotak Tebakan (Klik langsung pada kotak)
cols_g = st.columns(5)
for i in range(5):
    with cols_g[i]:
        if i < st.session_state.max_k:
            # Tombol yang berubah warna saat diklik (Kecepatan diperbaiki)
            color = WARNA_HEX[st.session_state.guesses[i]]
            st.button(" ", key=f"k_{i}", on_click=ganti_warna, args=(i,), 
                      help="Klik untuk ganti warna", use_container_width=True)
            # Menampilkan warna di bawah tombol karena CSS Streamlit membatasi warna tombol secara native
            st.markdown(f"<div style='background-color:{color}; height:10px; border-radius:5px;'></div>", unsafe_allow_html=True)
        else:
            st.write("")

# 6. Tombol OK Hitam
st.write("")
col_ok_space, col_ok_btn = st.columns([4, 1])
with col_ok_btn:
    st.markdown('<div class="ok-button">', unsafe_allow_html=True)
    if st.button("OK"):
        if "Kosong" not in st.session_state.guesses[:st.session_state.max_k]:
            res = hitung_paku(st.session_state.guesses[:st.session_state.max_k], st.session_state.target)
            st.session_state.history.append({'g': list(st.session_state.guesses[:st.session_state.max_k]), 'p': res})
            
            if st.session_state.guesses[:st.session_state.max_k] == st.session_state.target:
                st.balloons()
                if st.session_state.max_k < 5: st.session_state.max_k += 1
                st.session_state.target = random.choices(WARNA_LIST, k=st.session_state.max_k)
                st.session_state.guesses = ["Kosong"] * st.session_state.max_k
                st.session_state.history = []
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# 6 (Perbaikan). Riwayat Horizontal
st.write("### Riwayat:")
for h in reversed(st.session_state.history):
    st.markdown('<div class="history-row">', unsafe_allow_html=True)
    
    # Paku
    paku_html = "<div>"
    for p in h['p']:
        paku_html += f'<div class="paku" style="background-color:{WARNA_HEX[p]};"></div>'
    paku_html += "</div>"
    st.markdown(paku_html, unsafe_allow_html=True)
    
    # Kartu (Horizontal)
    card_html = '<div style="display: flex; gap: 5px;">'
    for c in h['g']:
        card_html += f'<div class="history-card" style="background-color:{WARNA_HEX[c]};"></div>'
    card_html += "</div>"
    st.markdown(card_html, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
