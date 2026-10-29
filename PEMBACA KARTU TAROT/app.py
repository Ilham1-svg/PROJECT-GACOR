import pandas as pd
import streamlit as st
 
import antrean, dek, gambar, riwayat
 
st.set_page_config(page_title="Dukun Digital Nusantara", page_icon="🔮")
 
def state():
    if "antrean" not in st.session_state:
        st.session_state.antrean = antrean.buat_antrean()  
        st.session_state.dek = dek.siapkan_dek()            
        st.session_state.riwayat = []                       
        st.session_state.nomor = 0
        st.session_state.pesan = None
        st.session_state.hasil = None
 
 
def kirim_pesan(jenis, teks):
    st.session_state.pesan = (jenis, teks)
 
 
def tampilkan_pesan():
    if st.session_state.pesan:
        jenis, teks = st.session_state.pesan
        tampil = {"sukses": st.success, "gagal": st.error, "info": st.info}
        tampil[jenis](teks)
        st.session_state.pesan = None
 
 
def proses_daftar():
    nomor = st.session_state.nomor + 1
    ok, pesan = antrean.daftar_ramalan(
        st.session_state.antrean, nomor,
        st.session_state.in_nama, st.session_state.in_tanya,
    )
    if ok:
        st.session_state.nomor = nomor
        st.session_state.in_nama = ""
        st.session_state.in_tanya = ""
    kirim_pesan("sukses" if ok else "gagal", pesan)
 
 
def proses_ubah(nomor):
    baru = st.session_state[f"tanya_baru_{nomor}"]
    ok, pesan = antrean.ubah_sesi(st.session_state.antrean, nomor, baru)
    kirim_pesan("sukses" if ok else "gagal", pesan)
 
 
def proses_batal(nomor):
    if not st.session_state.get("yakin_batal", False):
        kirim_pesan("gagal", "Centang konfirmasi dulu sebelum membatalkan sesi.")
        return
    ok, pesan = antrean.batalkan_sesi(st.session_state.antrean, nomor)
    if ok:
        st.session_state.yakin_batal = False
    kirim_pesan("sukses" if ok else "gagal", pesan)
 
 
def proses_layani():
    if not st.session_state.antrean:
        kirim_pesan("info", "Antrean kosong. Daftarkan peminta ramalan dulu.")
        return
    tambahan = ""
    if len(st.session_state.dek) < len(dek.posisi):
        st.session_state.dek = dek.siapkan_dek()
        tambahan = " Kartu hampir habis, jadi dek dikocok ulang."
    sesi = antrean.layani_terdepan(st.session_state.antrean)         
    kartu = dek.tarik_kartu(st.session_state.dek, len(dek.posisi))      
    riwayat.simpan_hasil(st.session_state.riwayat, sesi, kartu)
    st.session_state.hasil = {"sesi": sesi, "kartu": kartu}
    kirim_pesan("sukses", f"Ramalan untuk {sesi['nama']} selesai." + tambahan)
 
 
def proses_kocok():
    st.session_state.dek = dek.siapkan_dek()
    kirim_pesan("sukses", "Dek dikocok ulang. Semua kartu kembali ke tumpukan.")
 
 
def tab_daftar():
    st.subheader("Daftar ramalan")
    with st.form("form_daftar"):
        st.text_input("Nama", key="in_nama", max_chars=50)
        st.text_area("Pertanyaan untuk kartu", key="in_tanya", height=100, max_chars=300)
        st.form_submit_button("Masuk antrean", on_click=proses_daftar)
 
 
def tab_antrean():
    st.subheader("Antrean")
    data = st.session_state.antrean
    if not data:
        st.info("Antrean masih kosong. Daftarkan peminta ramalan di tab Daftar ramalan.")
        return
 
    urutan = st.radio("Urutkan", list(antrean.URUTAN_TAMPILAN), horizontal=True)
    tabel = pd.DataFrame(antrean.lihat_antrean(data, urutan))
    tabel.columns = ["No", "Nama", "Pertanyaan", "Status"]
    st.dataframe(tabel, hide_index=True)
 
    daftar_no = [sesi["no"] for sesi in data]
    nama_sesi = lambda n: antrean.label_sesi(antrean.cari_sesi(data, n))
 
    st.markdown("### Ubah pertanyaan")
    pilih = st.selectbox("Pilih sesi", daftar_no, format_func=nama_sesi, key="pilih_ubah")
    st.text_area("Pertanyaan baru", value=antrean.cari_sesi(data, pilih)["pertanyaan"],
                 key=f"tanya_baru_{pilih}", max_chars=300)
    st.button("Simpan perubahan", on_click=proses_ubah, args=(pilih,))
 
    st.markdown("### Batalkan sesi")
    pilih_batal = st.selectbox("Pilih sesi", daftar_no, format_func=nama_sesi, key="pilih_batal")
    st.checkbox("Ya, batalkan sesi ini", key="yakin_batal")
    st.button("Batalkan sesi", on_click=proses_batal, args=(pilih_batal,))
 
 
def tab_ruang_ramal():
    st.subheader("Ruang ramal")
    kiri, kanan = st.columns(2)
    kiri.metric("Menunggu di antrean", len(st.session_state.antrean))
    kanan.metric("Kartu di dek", len(st.session_state.dek))
 
    if st.session_state.antrean:
        depan = st.session_state.antrean[0]
        st.text(f"Giliran berikutnya: {depan['nama']} (#{depan['no']})")
    else:
        st.write("Belum ada yang mengantre.")
 
    st.button("Layani peminta terdepan", on_click=proses_layani)
    st.button("Kocok ulang dek", on_click=proses_kocok)
 
    hasil = st.session_state.hasil
    if hasil:
        st.divider()
        st.text(f"Hasil untuk {hasil['sesi']['nama']}")
        st.text(f"Pertanyaan: {hasil['sesi']['pertanyaan']}")
        for kolom, (posisi, kartu) in zip(st.columns(len(hasil["kartu"])), hasil["kartu"]):
            with kolom:
                st.markdown(f"**{posisi}**")
                file_gambar = gambar.path_gambar(kartu)
                if file_gambar:
                    st.image(file_gambar, width=200)
                st.markdown(f"### {kartu['nama']}")
                st.write(kartu["arti"])
 
 
def tab_riwayat():
    st.subheader("Riwayat ramalan")
    data = riwayat.lihat_riwayat(st.session_state.riwayat)
    if not data:
        st.info("Belum ada ramalan. Layani peminta pertama di tab Ruang ramal.")
        return
    for catatan in data:
        with st.expander(f"#{catatan['no']} {catatan['nama']}"):
            st.text(riwayat.format_ramalan(catatan))
 
 

def main():
    state()
    st.title("Dukun Digital Nusantara")
    st.caption("Sistem Manajemen Antrean dan Pembacaan Kartu Tarot Berbasis Web. "
               "Ramalan ini hanya untuk hiburan.")
    tampilkan_pesan()
 
    t1, t2, t3, t4 = st.tabs(["Daftar ramalan", "Antrean", "Ruang ramal", "Riwayat ramalan"])
    with t1:
        tab_daftar()
    with t2:
        tab_antrean()
    with t3:
        tab_ruang_ramal()
    with t4:
        tab_riwayat()
 
 
main()
 