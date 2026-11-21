import json
import os

FILE_TAROT = os.path.join(os.path.dirname(__file__), "tarot.json")
with open(FILE_TAROT, encoding="utf-8") as f:
    DATA_TAROT = json.load(f)

PERTANYAAN = tuple(DATA_TAROT["pertanyaan"])

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