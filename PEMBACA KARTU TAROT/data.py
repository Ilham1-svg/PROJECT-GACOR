from collections import deque
 
PERTANYAAN = (
    "Bagaimana peruntungan percintaanku?",
    "Bagaimana perkembangan kuliah dan tugas-tugasku?",
    "Bagaimana prospek karier atau magangku?",
    "Bagaimana kondisi keuanganku ke depan?",
    "Bagaimana hubunganku dengan teman dan keluarga?",
    "Bagaimana kondisi semangat dan kesehatanku?",
    "Apa yang sebaiknya berhenti kupikirkan?",
    "Apakah aku sedang berada di jalur yang tepat?",
)
# Urutannya HARUS sama dengan PERTANYAAN di atas
topik = ("cinta", "kuliah", "karier", "uang", "sosial", "kesehatan", "lepas", "jalur")
assert len(PERTANYAAN) == len(topik), "PERTANYAAN dan TOPIK harus sama panjang"

# lambda: cara menampilkan daftar sesi
URUTAN_TAMPILAN = {
    "Urutan antrean": lambda sesi: list(sesi),
    "Nama A-Z": lambda sesi: sorted(sesi, key=lambda s: s["nama"].lower()),
}
# lambda: label singkat satu sesi untuk pilihan di form
label_sesi = lambda s: f"#{s['no']} {s['nama']}"

def buat_antrean():
    return deque()
 
def nomor_berikutnya(antrean, riwayat):
    semua = [s["no"] for s in antrean] + [c["no"] for c in riwayat]
    return max(semua, default=0) + 1
 
def validasi_input(nama, pertanyaan):
    if not nama.strip():
        return False, "Nama belum diisi. Tulis nama peminta ramalan."
    if pertanyaan not in PERTANYAAN:
        return False, "Pertanyaan tidak dikenal. Pilih dari daftar."
    return True, ""
#CREATE 
def tambah_sesi(antrean, riwayat, nama, pertanyaan):
    valid, pesan = validasi_input(nama, pertanyaan)
    if not valid:
        return False, pesan
    sesi = {
        "no": nomor_berikutnya(antrean, riwayat),
        "nama": nama.strip(),
        "pertanyaan": pertanyaan,
    }
    antrean.append(sesi)
    return True, f"{sesi['nama']} masuk antrean dengan nomor #{sesi['no']}."
#READ
def lihat_sesi(antrean, urutan="Urutan antrean"):
    return URUTAN_TAMPILAN[urutan](antrean)
 
def cari_sesi(antrean, nomor):
    for sesi in antrean:
        if sesi["no"] == nomor:
            return sesi
    return None
#UPDATE
def ubah_sesi(antrean, nomor, pertanyaan_baru):
    sesi = cari_sesi(antrean, nomor)
    if sesi is None:
        return False, "Sesi tidak ditemukan. Pilih sesi dari daftar antrean."
    valid, pesan = validasi_input(sesi["nama"], pertanyaan_baru)
    if not valid:
        return False, pesan
    sesi["pertanyaan"] = pertanyaan_baru
    return True, f"Pertanyaan {sesi['nama']} diperbarui."
#DELETE
def batalkan_sesi(antrean, nomor):
    sesi = cari_sesi(antrean, nomor)
    if sesi is None:
        return False, "Sesi tidak ditemukan. Pilih sesi dari daftar antrean."
    antrean.remove(sesi)
    return True, f"Sesi {sesi['nama']} dibatalkan."
 
def layani_sesi(antrean):
    if not antrean:
        return None
    return antrean.popleft()