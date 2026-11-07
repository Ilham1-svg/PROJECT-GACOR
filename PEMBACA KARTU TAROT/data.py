PERTANYAAN = (
    "Bagaimana perkembangan hubungan sosial dan percintaanku?",
    "Bagaimana perkembangan pendidikan, karier, dan potensi diriku?",
    "Bagaimana kondisi kesejahteraan hidupku?",
    "Apakah keputusan dan langkah yang sedang kuambil sudah benar?",
)

rapikan_nama = lambda nama: " ".join(nama.strip().split()).title()

def tambah_peminta(antrean, nama, pertanyaan):
    nama = rapikan_nama(nama)
    if not nama:
        return "Nama tidak boleh kosong."
    if pertanyaan not in PERTANYAAN:
        return "Pertanyaan tidak valid."
    antrean.append({"nama": nama, "pertanyaan": pertanyaan})
    return "ok"

def ubah_peminta(antrean, indeks, pertanyaan_baru):
    if 0 <= indeks < len(antrean) and pertanyaan_baru in PERTANYAAN:
        antrean[indeks]["pertanyaan"] = pertanyaan_baru
        return True
    return False

def hapus_peminta(antrean, indeks):
    if 0 <= indeks < len(antrean):
        return antrean.pop(indeks)
    return None