import random
import os
from data import PERTANYAAN, DATA_TAROT

FOLDER_GAMBAR = os.path.join(os.path.dirname(__file__), "gambar")
DEK = DATA_TAROT["dek"]
MAKNA = DATA_TAROT["arti"]

def kocok_kartu (): 
    return random.sample(DEK, len(DEK))

def tarik_kartu(dek, jumlah=3):
    if jumlah < 1 or len(dek) < jumlah: raise ValueError("Jumlah kartu tidak mencukupi.")
    return [dek.pop() for _ in range(jumlah)]

def path_gambar(nama):
    path = os.path.join(FOLDER_GAMBAR, nama)
    return path if os.path.exists(path) else None

def makna_statis(nama_kartu, topik, waktu=None):
    if nama_kartu not in MAKNA: raise ValueError(f"Makna kartu '{nama_kartu}' belum tersedia.")
    if topik not in PERTANYAAN: raise ValueError("Pertanyaan tidak valid.")
    inti = MAKNA[nama_kartu]["inti"]
    makna_topik = MAKNA[nama_kartu]["topik"]
    indeks = PERTANYAAN.index(topik)
    if indeks < len(makna_topik) and makna_topik[indeks]:
        isi = makna_topik[indeks]
        if waktu: isi = f"Di {waktu.lower()}, {isi[0].lower() + isi[1:]}"
        return f"Kartu ini melambangkan {inti}.\n\n{isi}"
    return f"Arti umum kartu ini adalah {inti}."