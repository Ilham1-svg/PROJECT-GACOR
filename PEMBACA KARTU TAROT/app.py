import pandas as pd
import streamlit as st
 
import data, dek, riwayat

st.set_page_config(page_title="Dukun Digital Nusantara", page_icon="🔮")

st.markdown(
    """
    <style>
    [data-testid="stMain"] { overflow-y: scroll; }
    </style>
    """,
    unsafe_allow_html=True,
)

if "antrean" not in st.session_state:
    st.session_state.antrean = data.buat_antrean()   
    st.session_state.dek = dek.siapkan_dek()         
    st.session_state.riwayat = []                    
    st.session_state.hasil = None
    st.session_state.pesan = None
 
antrean = st.session_state.antrean
tumpukan = st.session_state.dek
catatan = st.session_state.riwayat

st.title("Dukun Digital Nusantara")
st.caption("Sistem Manajemen Antrean dan Pembacaan Kartu Tarot Berbasis Web. "
           "Ramalan ini hanya untuk hiburan.")
 
if st.session_state.pesan:
    berhasil, teks = st.session_state.pesan
    st.session_state.pesan = None
    (st.success if berhasil else st.error)(teks)
 
tab1, tab2, tab3, tab4 = st.tabs(["Daftar ramalan", "Antrean", "Ruang ramal", "Riwayat ramalan"])
 
with tab1:
    st.subheader("Daftar ramalan")
    with st.form("form_daftar", clear_on_submit=True):
        nama = st.text_input("Nama")
        pertanyaan = st.selectbox("Pertanyaan untuk kartu", data.PERTANYAAN)
        kirim = st.form_submit_button("Masuk antrean")
    if kirim:
        st.session_state.pesan = data.tambah_sesi(antrean, catatan, nama, pertanyaan)
        st.rerun()
 
with tab2:
    st.subheader("Antrean")
    if not antrean:
        st.info("Antrean masih kosong. Daftarkan peminta ramalan di tab Daftar ramalan.")
    else:
        tabel = pd.DataFrame(data.lihat_sesi(antrean))
        tabel.columns = ["No", "Nama", "Pertanyaan"]
        tabel["No"] = tabel["No"].astype(str)
        st.dataframe(
            tabel,
            hide_index=True,
            width="content",
            column_config={
                "No": st.column_config.TextColumn("No", width=50),
                "Nama": st.column_config.TextColumn("Nama", width=250),
                "Pertanyaan": st.column_config.TextColumn("Pertanyaan", width=400),
            },
        )
 
        daftar_no = [sesi["no"] for sesi in antrean]
        nama_sesi = lambda n: data.label_sesi(data.cari_sesi(antrean, n))
 
        st.markdown("Ubah pertanyaan")
        with st.form("form_ubah", clear_on_submit=True):
            pilih_ubah = st.selectbox("Pilih sesi", daftar_no, format_func=nama_sesi, key="pilih_ubah")
            pertanyaan_baru = st.selectbox("Pertanyaan baru", data.PERTANYAAN, key="tanya_baru")
            simpan = st.form_submit_button("Simpan perubahan")
        if simpan:
            st.session_state.pesan = data.ubah_sesi(antrean, pilih_ubah, pertanyaan_baru)
            st.rerun()
 
        st.markdown("Batalkan sesi")
        with st.form("form_batal", clear_on_submit=True):
            pilih_batal = st.selectbox("Pilih sesi", daftar_no, format_func=nama_sesi, key="pilih_batal")
            yakin = st.checkbox("Ya, batalkan sesi ini")
            batal = st.form_submit_button("Batalkan sesi")
        if batal:
            if yakin:
                st.session_state.pesan = data.batalkan_sesi(antrean, pilih_batal)
            else:
                st.session_state.pesan = (False, "Centang konfirmasi dulu sebelum membatalkan sesi.")
            st.rerun()
 
with tab3:
    st.subheader("Ruang ramal")
    kiri, kanan = st.columns(2)
    kiri.metric("Menunggu di antrean", len(antrean))
    kanan.metric("Kartu di dek", len(tumpukan))
 
    if antrean:
        st.write(f"Giliran berikutnya: {antrean[0]['nama']} (#{antrean[0]['no']})")
    else:
        st.write("Belum ada yang mengantre.")
 
    if st.button("Layani peminta terdepan"):
        if not antrean:
            st.session_state.pesan = (False, "Antrean kosong. Daftarkan peminta ramalan dulu.")
        else:
            acak_ulang = len(tumpukan) < len(dek.POSISI)
            sesi = data.layani_sesi(antrean)                 
            kartu = dek.tarik_kartu(tumpukan)                
            riwayat.simpan_hasil(catatan, sesi, kartu)
            st.session_state.hasil = {"sesi": sesi, "kartu": kartu}
            st.session_state.pesan = (True, f"Ramalan untuk {sesi['nama']} selesai."
                                      + (" Kartu hampir habis, jadi dek dikocok ulang." if acak_ulang else ""))
        st.rerun()
 
    if st.button("Kocok ulang dek"):
        tumpukan[:] = dek.siapkan_dek()
        st.session_state.pesan = (True, "Dek dikocok ulang. Semua kartu kembali ke tumpukan.")
        st.rerun()
 
    hasil = st.session_state.hasil
    if hasil:
        topik = data.topik[data.PERTANYAAN.index(hasil["sesi"]["pertanyaan"])]
        st.divider()
        st.write(f"Hasil untuk {hasil['sesi']['nama']}")
        st.caption(f"Pertanyaan: {hasil['sesi']['pertanyaan']}")
        for kolom, (posisi, kartu) in zip(st.columns(len(hasil["kartu"])), hasil["kartu"]):
            with kolom:
                st.markdown(f"**{posisi}**")
                file_gambar = dek.path_gambar(kartu)
                if file_gambar:
                    st.image(file_gambar, width=200)
                else:
                    st.caption(f"Gambar belum ditemukan. Taruh file .png berawalan {dek.DAFTAR_KARTU.index(kartu):02d} di folder gambar/")
                st.markdown(f"### {kartu['nama']}")
                st.write(dek.arti_kartu(kartu, topik))
 
with tab4:
    st.subheader("Riwayat ramalan")
    daftar_riwayat = riwayat.lihat_riwayat(catatan)
    if not daftar_riwayat:
        st.info("Belum ada ramalan. Layani peminta pertama di tab Ruang ramal.")
    for c in daftar_riwayat:
        with st.expander(f"#{c['no']} {c['nama']}"):
            st.write(riwayat.format_ramalan(c))
 