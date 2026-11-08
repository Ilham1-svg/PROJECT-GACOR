import streamlit as st
from data import PERTANYAAN, tambah_peminta, ubah_peminta, hapus_peminta
from dek import kocok_dek, tarik_kartu, path_gambar
from riwayat import simpan_riwayat
from arti import makna_statis

POSISI = ("Masa lalu", "Masa kini", "Masa depan")

st.set_page_config(page_title="GORANGO",layout="centered")
st.title("🔮 Dukun Online")
st.caption("Sistem Pembaca Kartu Tarot Berbasis Streamlit")

if "antrean" not in st.session_state: st.session_state.antrean = []
if "dek" not in st.session_state: st.session_state.dek = kocok_dek()
if "riwayat" not in st.session_state: st.session_state.riwayat = []
if "hasil" not in st.session_state: st.session_state.hasil = None
if "flash" not in st.session_state: st.session_state.flash = None

if st.session_state.flash:
    tipe, pesan = st.session_state.flash
    getattr(st, tipe)(pesan)
    st.session_state.flash = None

tab1, tab2, tab3, tab4 = st.tabs(["Daftar Ramalan", "Antrean", "Ruang Ramal", "Riwayat Ramalan"])

with tab1:
    st.subheader("Daftar Ramalan")
    with st.form("form_daftar", clear_on_submit=True):
        nama = st.text_input("Nama peminta")
        pertanyaan = st.selectbox("Pilih pertanyaan", PERTANYAAN)
        kirim = st.form_submit_button("Ambil Nomor Antrean")
    if kirim:
        pesan = tambah_peminta(st.session_state.antrean, nama, pertanyaan)
        if pesan == "ok": st.success(f"{nama} Berhasil masuk antrean.")
        else: st.warning(pesan)

with tab2:
    st.subheader("Antrean Peminta")
    antrean = st.session_state.antrean
    if not antrean:
        st.info("Antrean masih kosong.")
    else:
        for i, peminta in enumerate(antrean, start=1):
            st.write(f"**{i}. {peminta['nama']}** — {peminta['pertanyaan']}")

        nomor = st.selectbox("Pilih nomor antrean", range(1, len(antrean) + 1))
        aksi = st.radio("Aksi", ["Ubah pertanyaan", "Batalkan antrean"], horizontal=True)

        if aksi == "Ubah pertanyaan":
            pertanyaan_baru = st.selectbox("Pertanyaan baru", PERTANYAAN, key="ubah")
            if st.button("Simpan perubahan"):
                if ubah_peminta(antrean, int(nomor) - 1, pertanyaan_baru):
                    st.session_state.pesan_antrean = ("success", "Pertanyaan berhasil diubah.")
                st.rerun()
        else:
            konfirmasi = st.checkbox("Saya yakin ingin membatalkan antrean ini.")
            if st.button("Batalkan"):
                if not konfirmasi:
                    st.warning("Silakan centang konfirmasi terlebih dahulu!")
                else:
                    if hapus_peminta(antrean, int(nomor) - 1):
                        st.session_state.pesan_antrean = ("success", "Antrean berhasil dibatalkan.")
                    st.rerun()
    if st.session_state.get("pesan_antrean"):
        tipe, teks = st.session_state.pop("pesan_antrean")
        getattr(st, tipe)(teks)

with tab3:
    st.subheader("Ruang Ramal")
    antrean = st.session_state.antrean
    st.metric("Jumlah Kartu Tersisa", len(st.session_state.dek)," / 22")

    if st.button("Kocok Ulang Kartu"):
        st.session_state.dek = kocok_dek()
        st.session_state.pesan_ruang = ("success", "Dek kartu berhasil dikocok ulang.")
        st.rerun()  

    st.write(f"Jumlah peminta dalam antrean: **{len(antrean)}**")
    if not antrean:
        st.info("Belum ada peminta. Daftarkan peminta terlebih dahulu.")
    elif st.button("Layani Peminta Berikutnya", type="primary"):
        peminta = antrean[0]
        if len(st.session_state.dek) < 3: st.session_state.dek = kocok_dek()
        try:
            kartu = tarik_kartu(st.session_state.dek, 3)
            arti = [makna_statis(k["nama"], peminta["pertanyaan"], w) for k, w in zip(kartu, POSISI)]
            hasil = {"nama": peminta["nama"], "pertanyaan": peminta["pertanyaan"], "kartu": kartu, "arti": arti}
            simpan_riwayat(st.session_state.riwayat, hasil)
            antrean.pop(0)
            st.session_state.hasil = hasil
            st.session_state.pesan_ruang = ("success", "Ramalan berhasil dibuat.")
            st.rerun()
        except (RuntimeError, ValueError) as error:
            st.session_state.dek = kocok_dek()
            st.error(f"Ramalan gagal diproses: {error}")
    if st.session_state.get("pesan_ruang"):
        tipe, teks = st.session_state.pop("pesan_ruang")
        getattr(st, tipe)(teks)

    if st.session_state.hasil:
        hasil = st.session_state.hasil
        st.divider()
        st.write(f"**Peminta:** {hasil['nama']}")
        st.write(f"**Pertanyaan:** {hasil['pertanyaan']}")
        st.caption("Urutan kartu: Masa lalu → Masa kini → Masa depan")
        for posisi, kartu, arti in zip(POSISI, hasil["kartu"], hasil["arti"]):
            with st.container(border=True):
                st.markdown(f"**{posisi}: {kartu['nama']}**")
                kolom_gambar, kolom_arti = st.columns([1, 2])
                gambar = path_gambar(kartu["gambar"])
                with kolom_gambar:
                    if gambar:
                        st.image(gambar, width=180)
                    else:
                        st.info("Gambar kartu belum tersedia.")
                with kolom_arti:
                    st.write(arti)
        st.caption("Anggap ini bahan refleksi, bukan kepastian. Keputusan tetap ada di tanganmu.")

with tab4:
    st.subheader("Riwayat Ramalan")
    if not st.session_state.riwayat:
        st.info("Belum ada riwayat ramalan.")
    else:
        for i, catatan in enumerate(reversed(st.session_state.riwayat), start=1):
            with st.expander(f"{i}. {catatan['nama']}"):
                st.write(f"Pertanyaan: {catatan['pertanyaan']}")
                for posisi, kartu, arti in zip(("Masa lalu", "Masa kini", "Masa depan"), catatan["kartu"], catatan["arti"]):
                    st.write(f"**{posisi}: {kartu['nama']}**")
                    st.write(arti)