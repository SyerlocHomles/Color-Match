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

    /* Kotak Tebakan (Tombol Transparan di Atas Warna) */
    .stButton > button {
        border: 2px solid #555 !important;
        border-radius: 10px !important;
        height: 100px !important;
        width: 100% !important;
        transition: 0.1s;
    }
    
    /* Tombol OK Hitam/Putih */
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
        width: 15px;
        height: 15px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 10px; /* Jarak antar paku agar sejajar kartu */
        border: 1px solid #333;
    }

    /* Riwayat Horizontal */
    .history-row {
        display: flex;
        flex-direction: column; /* Ubah ke kolom agar paku di atas kartu */
        align-items: flex-start;
        gap: 5px;
        margin-bottom: 15px;
        padding: 10px;
        border-bottom: 1px solid #333;
    }
    
    .history-card {
        width: 25px;
        height: 35px;
        border: 1px solid white;
        margin-right: 2px;
    }
    </style>
""", unsafe_allow_html=True)

# --- LOGIKA GAME ---
WARNA_LIST = ["Merah", "Oren", "Kuning", "Hijau", "Biru"]
WARNA_HEX = {
    "Kosong": "#333333", "Merah": "#FF0000", "Oren": "#FFA500", 
    "Kuning": "#FFFF00", "Hijau": "#00FF00", "Biru": "#0000FF"
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

# --- PERBAIKAN LOGIKA PAKU (SINKRON KIRI-KANAN) ---
def hitung_paku(guess, target):
    # Inisialisasi semua paku sebagai Merah (Salah Total)
    paku_result = ["Merah"] * len(target)
    t_temp = list(target)
    g_temp = list(guess)
    
    # Tahap 1: Cek yang Benar Posisi & Warna (Hijau)
    for i in range(len(g_temp)):
        if g_temp[i] == t_temp[i]:
            paku_result[i] = "Hijau"
            t_temp[i] = None # Tandai agar tidak dihitung dua kali
            g_temp[i] = "DONE"
            
    # Tahap 2: Cek yang Warnanya Benar tapi Salah Posisi (Oren)
    for i in range(len(g_temp)):
        if g_temp[i] != "DONE":
            if g_temp[i] in t_temp:
                paku_result[i] = "Oren"
                # Hapus warna yang sudah 'terpakai' dari target sementara
                t_temp[t_temp.index(g_temp[i])] = None
            else:
                paku_result[i] = "Merah"
                
    return paku_result # Mengembalikan urutan asli tanpa sorted()

# --- TAMPILAN ---

st.markdown('<div class="title-text">COLOUR MATCH</div>', unsafe_allow_html=True)

col_info, col_hints = st.columns([1, 2])
with col_info:
    st.subheader(f"{st.session_state.max_k} KARTU")
with col_hints:
    # Menampilkan petunjuk warna yang ada di dalam jawaban
    hints = sorted(list(set(st.session_state.target)))
    h_cols = st.columns(5)
    for idx, h in enumerate(hints):
        h_cols[idx].markdown(f"<div style='background-color:{WARNA_HEX[h]}; height:25px; border:1px solid white;'></div>", unsafe_allow_html=True)

st.write("---")

# Kotak Tebakan Utama
cols_g = st.columns(5)
for i in range(5):
    with cols_g[i]:
        if i < st.session_state.max_k:
            color = WARNA_HEX[st.session_state.guesses[i]]
            st.button(" ", key=f"k_{i}", on_click=ganti_warna, args=(i,), use_container_width=True)
            st.markdown(f"<div style='background-color:{color}; height:12px; border-radius:5px;'></div>", unsafe_allow_html=True)

# Tombol Eksekusi
st.write("")
_, col_ok_btn = st.columns([4, 1])
with col_ok_btn:
    st.markdown('<div class="ok-button">', unsafe_allow_html=True)
    if st.button("OK"):
        if "Kosong" not in st.session_state.guesses[:st.session_state.max_k]:
            res = hitung_paku(st.session_state.guesses[:st.session_state.max_k], st.session_state.target)
            # Simpan tebakan dan hasil paku ke riwayat
            st.session_state.history.append({
                'g': list(st.session_state.guesses[:st.session_state.max_k]), 
                'p': res
            })
            
            # Cek Kemenangan
            if st.session_state.guesses[:st.session_state.max_k] == st.session_state.target:
                st.balloons()
                st.success("KEREN! Kamu Menang!")
                if st.session_state.max_k < 5: st.session_state.max_k += 1
                st.session_state.target = random.choices(WARNA_LIST, k=st.session_state.max_k)
                st.session_state.guesses = ["Kosong"] * st.session_state.max_k
                st.session_state.history = []
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- RIWAYAT DENGAN PERBAIKAN VISUAL ---
st.write("### Riwayat (Urutan Kiri ke Kanan):")
for h in reversed(st.session_state.history):
    st.markdown('<div class="history-row">', unsafe_allow_html=True)
    
    # Baris Paku (Petunjuk) - Letakkan di atas kartu agar mudah dilihat
    paku_html = '<div style="display: flex; margin-left: 5px;">'
    for p in h['p']:
        paku_html += f'<div class="paku" style="background-color:{WARNA_HEX[p]};"></div>'
    paku_html += "</div>"
    st.markdown(paku_html, unsafe_allow_html=True)
    
    # Baris Kartu (Tebakan)
    card_html = '<div style="display: flex; gap: 5px;">'
    for c in h['g']:
        card_html += f'<div class="history-card" style="background-color:{WARNA_HEX[c]};"></div>'
    card_html += "</div>"
    st.markdown(card_html, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
