import streamlit as st
import random

# --- STYLE CSS AGAR MIRIP SKETSA ---
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; }
    .card-slot {
        border: 2px solid #000;
        border-radius: 15px;
        height: 120px;
        width: 80px;
        margin: auto;
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: #f9f9f9;
    }
    .paku-container {
        display: flex;
        gap: 5px;
        align-items: center;
    }
    .paku-dot {
        width: 15px;
        height: 15px;
        border-radius: 50%;
        border: 1px solid #000;
    }
    /* Tombol transparan di atas kotak kartu */
    .stButton>button {
        height: 120px;
        background-color: transparent !important;
        border: none !important;
        color: transparent !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- LOGIKA GAME ---
WARNA_MAP = {
    "Putih": "#FFFFFF", "Merah": "#FF0000", "Oren": "#FFA500", 
    "Kuning": "#FFFF00", "Hijau": "#00FF00", "Biru": "#0000FF"
}
LIST_WARNA = ["Merah", "Oren", "Kuning", "Hijau", "Biru"]

if 'game' not in st.session_state:
    st.session_state.game = {
        'target': random.choices(LIST_WARNA, k=5),
        'attempts': [],
        'current_guess': ["Putih"] * 5,
        'over': False
    }

def handle_click(i):
    if not st.session_state.game['over']:
        curr = st.session_state.game['current_guess'][i]
        next_idx = (LIST_WARNA.index(curr) + 1) % len(LIST_WARNA) if curr in LIST_WARNA else 0
        st.session_state.game['current_guess'][i] = LIST_WARNA[next_idx]

# --- TAMPILAN ATAS (INFO) ---
col_score, col_hints = st.columns([1, 2])
with col_score:
    st.markdown(f"### {10 - len(st.session_state.game['attempts'])}") # Angka 50 di sketsamu (Sisa Nyawa)
with col_hints:
    hints = sorted(list(set(st.session_state.game['target'])))
    h_cols = st.columns(len(hints))
    for idx, h in enumerate(hints):
        h_cols[idx].markdown(f"<div style='background-color:{WARNA_MAP[h]}; height:30px; border:2px solid #000;'></div>", unsafe_allow_html=True)

st.write("")

# --- TAMPILAN TENGAH (5 KARTU) ---
cols = st.columns(5)
for i in range(5):
    with cols[i]:
        # Kotak warna
        color = WARNA_MAP[st.session_state.game['current_guess'][i]]
        st.markdown(f"<div class='card-slot' style='background-color:{color};'></div>", unsafe_allow_html=True)
        # Tombol transparan untuk klik
        st.button(" ", key=f"btn_{i}", on_click=handle_click, args=(i,))

# --- TOMBOL OK ---
col_space, col_ok = st.columns([4, 1])
with col_ok:
    if st.button("OK", key="ok_btn"):
        # Logika Pengecekan Paku
        guess = st.session_state.game['current_guess']
        target = st.session_state.game['target']
        
        # Simulasi hasil paku sederhana
        paku_result = []
        for g, t in zip(guess, target):
            if g == t: paku_result.append("#00FF00") # Hijau (Benar semua)
            elif g in target: paku_result.append("#FFA500") # Oren (Benar warna)
            else: paku_result.append("#FF0000") # Merah (Salah)
        
        st.session_state.game['attempts'].append({'guess': list(guess), 'paku': paku_result})
        if guess == target:
            st.success("Level Up!")
            st.session_state.game['over'] = True

st.write("---")

# --- RIWAYAT (PAKU DI KIRI) ---
for att in reversed(st.session_state.game['attempts']):
    c_paku, c_cards = st.columns([1, 3])
    with c_paku:
        paku_html = "<div class='paku-container'>"
        for p_color in att['paku']:
            paku_html += f"<div class='paku-dot' style='background-color:{p_color};'></div>"
        paku_html += "</div>"
        st.markdown(paku_html, unsafe_allow_html=True)
    with c_cards:
        card_html = "<div style='display:flex; gap:5px;'>"
        for c_color in att['guess']:
            card_html += f"<div style='width:20px; height:30px; background-color:{WARNA_MAP[c_color]}; border:1px solid #000;'></div>"
        card_html += "</div>"
        st.markdown(card_html, unsafe_allow_html=True)
