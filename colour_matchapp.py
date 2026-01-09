import streamlit as st
import random

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Guess Color Master", layout="centered")

# --- CSS UNTUK PRESISI POSISI (SESUAI SKETSA) ---
st.markdown("""
    <style>
    /* Container utama agar seperti papan game */
    .game-container {
        position: relative;
        width: 350px;
        height: 600px;
        margin: auto;
        border: 3px solid #000;
        border-radius: 20px;
        padding: 20px;
        background-color: white;
    }
    
    /* Angka sisa nyawa (Kiri Atas) */
    .score-text {
        position: absolute;
        top: 20px; left: 30px;
        font-size: 40px; font-weight: bold;
    }

    /* Warna petunjuk (Kanan Atas) */
    .hint-container {
        position: absolute;
        top: 30px; right: 30px;
        display: flex; gap: 10px;
    }
    .hint-box {
        width: 30px; height: 35px; border: 2px solid #000;
    }

    /* 5 Kotak Utama (Tengah) */
    .main-cards {
        position: absolute;
        top: 130px; left: 25px;
        display: flex; gap: 8px;
    }
    .card {
        width: 55px; height: 90px;
        border: 2px solid #000; border-radius: 12px;
    }

    /* Area Paku dan Tombol OK (Bawah Kartu) */
    .action-row {
        position: absolute;
        top: 240px; left: 20px;
        width: 310px;
        display: flex; align-items: center; justify-content: space-between;
    }
    .paku-box {
        display: flex; gap: 4px;
    }
    .paku {
        width: 12px; height: 12px; border-radius: 50%; border: 1px solid #000;
    }
    .ok-circle {
        width: 40px; height: 40px; border: 2px solid #000;
        border-radius: 50%; text-align: center; line-height: 36px;
        font-weight: bold; cursor: pointer;
    }

    /* Menghilangkan header default streamlit agar rapi */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- LOGIKA GAME ---
WARNA_LIST = ["Merah", "Oren", "Kuning", "Hijau", "Biru"]
WARNA_HEX = {
    "Putih": "#FFFFFF", "Merah": "#FF0000", "Oren": "#FFA500", 
    "Kuning": "#FFFF00", "Hijau": "#00FF00", "Biru": "#0000FF", "Abu": "#808080"
}

if 'target' not in st.session_state:
    st.session_state.target = random.choices(WARNA_LIST, k=5)
    st.session_state.guesses = ["Putih"] * 5
    st.session_state.attempts = []

def ganti_warna(i):
    current = st.session_state.guesses[i]
    if current == "Putih": next_c = WARNA_LIST[0]
    else: next_c = WARNA_LIST[(WARNA_LIST.index(current) + 1) % len(WARNA_LIST)]
    st.session_state.guesses[i] = next_c

def setor_jawaban():
    if "Putih" in st.session_state.guesses: return
    
    res = []
    temp_target = st.session_state.target[:]
    temp_guess = st.session_state.guesses[:]

    # 1. Hijau (Benar Posisi)
    for i in range(5):
        if temp_guess[i] == temp_target[i]:
            res.append("Hijau")
            temp_target[i] = None
            temp_guess[i] = None
    
    # 2. Oren (Benar Warna, Salah Posisi)
    for i in range(5):
        if temp_guess[i] and temp_guess[i] in temp_target:
            res.append("Oren")
            temp_target[temp_target.index(temp_guess[i])] = None
            temp_guess[i] = None
    
    # 3. Merah (Salah)
    while len(res) < 5:
        res.append("Merah")
        
    st.session_state.attempts.append({'c': list(st.session_state.guesses), 'p': res})
    if st.session_state.guesses == st.session_state.target:
        st.success("LEVEL UP!")
        st.session_state.target = random.choices(WARNA_LIST, k=random.randint(3,5))
        st.session_state.attempts = []

# --- RENDER TAMPILAN SESUAI SKETSA ---
# Container Utama
st.markdown('<div class="game-container">', unsafe_allow_html=True)

# 1. Sisa Nyawa (Angka 50 di sketsamu)
nyawa = 10 - len(st.session_state.attempts)
st.markdown(f'<div class="score-text">{nyawa}</div>', unsafe_allow_html=True)

# 2. Petunjuk Warna (Kanan Atas)
hints = sorted(list(set(st.session_state.target)))
h_html = "".join([f'<div class="hint-box" style="background-color:{WARNA_HEX[h]}"></div>' for h in hints])
st.markdown(f'<div class="hint-container">{h_html}</div>', unsafe_allow_html=True)

# 3. 5 Kotak Tengah (Kartu)
st.markdown('<div class="main-cards">', unsafe_allow_html=True)
cols = st.columns(5)
for i in range(5):
    with cols[i]:
        st.markdown(f'<div class="card" style="background-color:{WARNA_HEX[st.session_state.guesses[i]]}"></div>', unsafe_allow_html=True)
        st.button("🔄", key=f"btn_{i}", on_click=ganti_warna, args=(i,))
st.markdown('</div>', unsafe_allow_html=True)

# 4. Paku & Tombol OK (Baris Bawah Kartu)
st.markdown('<div class="action-row">', unsafe_allow_html=True)
# Menampilkan paku dari tebakan terakhir
paku_html = ""
if st.session_state.attempts:
    last_paku = st.session_state.attempts[-1]['p']
    paku_html = "".join([f'<div class="paku" style="background-color:{WARNA_HEX[p]}"></div>' for p in last_paku])

st.markdown(f'<div class="paku-box">{paku_html}</div>', unsafe_allow_html=True)
st.button("OK", on_click=setor_jawaban)
st.markdown('</div>', unsafe_allow_html=True)

# 5. Riwayat (Scroll kebawah)
st.write("<br><br><br><br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
st.write("--- **RIWAYAT TEBAKAN** ---")
for a in reversed(st.session_state.attempts):
    st.write(f"Paku: {' '.join(a['p'])}")

st.markdown('</div>', unsafe_allow_html=True)
