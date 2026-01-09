def hitung_feedback(guess, target):
    # Pastikan kita membandingkan list dengan panjang yang sama
    t_temp = list(target)
    g_temp = list(guess)
    
    benar_posisi = 0
    salah_posisi = 0
    
    # LANGKAH 1: Cek Benar Posisi (Warna & Letak Sama)
    for i in range(len(t_temp)):
        if g_temp[i] == t_temp[i]:
            benar_posisi += 1
            t_temp[i] = "DONE_T" # Tandai agar tidak dihitung lagi
            g_temp[i] = "DONE_G"
            
    # LANGKAH 2: Cek Salah Posisi (Warna Ada di Target tapi beda letak)
    for i in range(len(g_temp)):
        if g_temp[i] != "DONE_G": # Hanya cek yang belum dapat poin Benar Posisi
            if g_temp[i] in t_temp:
                salah_posisi += 1
                # Hapus satu warna yang cocok dari target temp agar tidak double hitung
                t_temp[t_temp.index(g_temp[i])] = "DONE_T"
                
    # LANGKAH 3: Sisa kartu adalah Salah Warna
    salah_warna = len(target) - (benar_posisi + salah_posisi)
    
    return f"{benar_posisi} warna benar, {salah_posisi} warna salah posisi, {salah_warna} warna salah"

# --- BAGIAN TOMBOL OK (Update Logika Rerun) ---
if st.button("OK", use_container_width=True):
    if "Kosong" not in st.session_state.guesses:
        # PENTING: Gunakan slice [:] agar tidak merusak data asli saat pengecekan
        hasil_teks = hitung_feedback(st.session_state.guesses[:st.session_state.max_k], st.session_state.target)
        
        st.session_state.history.append({
            'g': list(st.session_state.guesses[:st.session_state.max_k]), 
            'f': hasil_teks
        })
        
        # Cek Kemenangan
        if st.session_state.guesses[:st.session_state.max_k] == st.session_state.target:
            st.balloons()
            st.success("JACKPOT! Semua Benar!")
