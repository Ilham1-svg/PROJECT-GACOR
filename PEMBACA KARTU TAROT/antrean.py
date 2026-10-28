from collections import deque
 
STATUS = ("Menunggu", "Sedang diramal")
 
# lambda: mengurutkan data untuk tampilan
URUTAN_TAMPILAN = {
    "Urutan antrean": lambda data: list(data),
    "Nama A-Z": lambda data: sorted(data, key=lambda s: s["nama"].lower()),
}
# lambda: label singkat sebuah sesi untuk pilihan di form
label_sesi = lambda s: f"#{s['no']} {s['nama']}"
 
def buat_antrean():
    """Antrean kosong (deque)."""
    return deque()
 
 
def validasi_input(nama, pertanyaan):
    """Mengecek isian. Mengembalikan (valid, pesan)."""
    if not nama.strip():
        return False, "Nama belum diisi. Tulis nama peminta ramalan."
    if len(pertanyaan.strip()) < 5:
        return False, "Pertanyaan terlalu pendek. Tulis minimal 5 karakter."
    return True, ""
 
 
# ---------- CREATE ----------
def daftar_ramalan(antrean, nomor, nama, pertanyaan):
    """Menambah sesi ke BELAKANG antrean."""
    valid, pesan = validasi_input(nama, pertanyaan)
    if not valid:
        return False, pesan
    sesi = {
        "no": nomor,
        "nama": nama.strip(),
        "pertanyaan": pertanyaan.strip(),
        "status": STATUS[0],
    }
    antrean.append(sesi)
    return True, f"{sesi['nama']} masuk antrean dengan nomor #{nomor}."
 
 
# ---------- READ ----------
def lihat_antrean(antrean, urutan="Urutan antrean"):
    """Daftar sesi untuk ditampilkan. Antrean asli tidak berubah."""
    return URUTAN_TAMPILAN[urutan](antrean)
 
 
def cari_sesi(antrean, nomor):
    """Mencari sesi berdasarkan nomor. None jika tidak ada."""
    for sesi in antrean:
        if sesi["no"] == nomor:
            return sesi
    return None
 
 
# ---------- UPDATE ----------
def ubah_sesi(antrean, nomor, pertanyaan_baru):
    """Mengganti pertanyaan sesi. Posisi di antrean tidak berubah."""
    sesi = cari_sesi(antrean, nomor)
    if sesi is None:
        return False, "Sesi tidak ditemukan. Pilih sesi dari daftar antrean."
    valid, pesan = validasi_input(sesi["nama"], pertanyaan_baru)
    if not valid:
        return False, pesan
    sesi["pertanyaan"] = pertanyaan_baru.strip()
    return True, f"Pertanyaan {sesi['nama']} diperbarui."
 
 
# ---------- DELETE ----------
def batalkan_sesi(antrean, nomor):
    """Mengeluarkan sesi dari antrean."""
    sesi = cari_sesi(antrean, nomor)
    if sesi is None:
        return False, "Sesi tidak ditemukan. Pilih sesi dari daftar antrean."
    antrean.remove(sesi)
    return True, f"Sesi {sesi['nama']} dibatalkan."
 
 
# ---------- QUEUE (FIFO) ----------
def layani_terdepan(antrean):
    """Mengambil sesi paling DEPAN (popleft = FIFO). None jika antrean kosong."""
    if not antrean:
        return None
    sesi = antrean.popleft()
    sesi["status"] = STATUS[1]
    return sesi