import streamlit as st
import random

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Guess The Colour - Master", layout="centered")

# --- STYLE CSS UNTUK TAMPILAN HP ---
st.markdown("""
    <style>
    .color-box {
        width: 50px; height: 70px; border-radius: 10px; border: 2px solid #333;
        display: inline-block; margin: 5px; cursor: pointer; text-align: center; line-height: 70px;
    }
    .paku {
        width: 15px; height: 15px; border-radius: 50%; display: inline-block; margin-right: 5px;
    }
    .stButton>button { width: 100%; border-radius: 20px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- INITIAL STATE ---
WARNA_DAFTAR = {
    "Putih": "#FFFFFF", "Merah": "#FF4B4B", "Oren": "#FFA500", 
    "Kuning": "#FFFF00", "Hijau": "#00FF00", "Biru": "#0000FF"
}
LIST_WARNA = list(WARNA_DAFTAR.keys())[1:] # Kecuali Putih

if 'level' not in st.session_state:
    st.session_state.level = 1
    st.session_state.max_kartu = 3 # Mulai dari 3 kartu
    st.session_state.jawaban_rahasia = random.choices(LIST_WARNA, k=st.session_state.max_kartu)
    st.session_state.tebakan_saat_ini = ["Putih"] * st.session_state.max_kartu
    st.session_state.riwayat = []
    st.session_state.game_over = False

def reset_game(next_level=False):
    if next_level:
        st.session_state.level += 1
        st.session_state.max_kartu = min(5, st.session_state.max_kartu + 1)
    else:
        st.session_state.level = 1
        st.session_state.max_kartu = 3
    
    st.session_state.jawaban_rahasia = random.choices(LIST_WARNA, k=st.session_state.max_kartu)
    st.session_state.tebakan_saat_ini = ["Putih"] * st.session_state.max_kartu
    st.session_state.riwayat = []
    st.session_state.game_over = False

# --- LOGIKA PENGECEKAN (PAKU) ---
def cek_jawaban(tebakan, rahasia):
    hasil_paku = []
    temp_rahasia = rahasia[:]
    temp_tebakan = tebakan[:]
    
    # 1. Cek Hijau (Benar posisi & warna)
    for i in range(len(temp_tebakan)):
        if temp_tebakan[i] == temp_rahasia[i]:
            hasil_paku.append("🟢") # Hijau
            temp_rahasia[i] = None
            temp_tebakan[i] = "DONE"
            
    # 2. Cek Oranye & Abu-abu
    for i in range(len(temp_tebakan)):
        if temp_tebakan[i] != "DONE":
            if temp_tebakan[i] in temp_rahasia:
                hasil_paku.append("🟠") # Oranye
                temp_rahasia[temp_rahasia.index(temp_tebakan[i])] = None
            else:
                hasil_paku.append("🔴") # Merah (Salah Total)
                
    random.shuffle(hasil_paku) # Paku diacak agar tidak memberitahu posisi mana yang benar
    return "".join(hasil_paku)

# --- UI TAMPILAN ---
st.title("🎨 Guess The Colour")
st.subheader(f"Level {st.session_state.level} - Tebak {st.session_state.max_kartu} Kartu")

# Header Informasi (Sesuai sketsa: Poin & Warna yang tersedia)
c1, c2 = st.columns([1, 2])
with c1:
    st.metric("Sisa Nyawa", 10 - len(st.session_state.riwayat))
with c2:
    warna_unik = sorted(list(set(st.session_state.jawaban_rahasia)))
    st.write("Warna di dalam kartu:")
    cols = st.columns(len(warna_unik))
    for i, w in enumerate(warna_unik):
        cols[i].markdown(f"<div style='background-color:{WARNA_DAFTAR[w]}; height:20px; border:1px solid grey;'></div>", unsafe_allow_html=True)

st.write("---")

# Area Kartu Tebakan (Bisa diklik)
cols_kartu = st.columns(st.session_state.max_kartu)
for i in range(st.session_state.max_kartu):
    with cols_kartu[i]:
        if st.button(f"K{i+1}", key=f"btn_{i}"):
            if not st.session_state.game_over:
                idx_sekarang = LIST_WARNA.index(st.session_state.tebakan_saat_ini[i]) if st.session_state.tebakan_saat_ini[i] in LIST_WARNA else -1
                st.session_state.tebakan_saat_ini[i] = LIST_WARNA[(idx_sekarang + 1) % len(LIST_WARNA)]
        
        warna_hex = WARNA_DAFTAR[st.session_state.tebakan_saat_ini[i]]
        st.markdown(f"<div class='color-box' style='background-color:{warna_hex};'></div>", unsafe_allow_html=True)

# Tombol OK
if st.button("✅ SETOR JAWABAN (OK)"):
    if "Putih" in st.session_state.tebakan_saat_ini:
        st.warning("Pilih semua warna dulu!")
    else:
        hasil = cek_jawaban(st.session_state.tebakan_saat_ini, st.session_state.jawaban_rahasia)
        st.session_state.riwayat.append({"tebakan": list(st.session_state.tebakan_saat_ini), "paku": hasil})
        
        if st.session_state.tebakan_saat_ini == st.session_state.jawaban_rahasia:
            st.success("LUAR BIASA! Kamu Benar!")
            st.balloons()
            st.button("Lanjut ke Level Berikutnya", on_click=reset_game, args=(True,))
            st.session_state.game_over = True
        elif len(st.session_state.riwayat) >= 10:
            st.error(f"GAME OVER! Jawabannya adalah: {', '.join(st.session_state.jawaban_rahasia)}")
            st.button("Coba Lagi", on_click=reset_game)
            st.session_state.game_over = True

# Riwayat Tebakan (Paku di sebelah kiri sesuai sketsa)
st.write("### Riwayat Tebakan")
for r in reversed(st.session_state.riwayat):
    col_p, col_t = st.columns([1, 2])
    with col_p:
        st.write(f"Paku: {r['paku']}")
    with col_t:
        warna_html = "".join([f"<div class='paku' style='background-color:{WARNA_DAFTAR[w]};'></div>" for w in r['tebakan']])
        st.markdown(warna_html, unsafe_allow_html=True)

if st.sidebar.button("Reset Total"):
    reset_game()
