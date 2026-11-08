import random
import os

FOLDER_GAMBAR = os.path.join(os.path.dirname(__file__), "gambar")

DEK = [
    {"nama": "The Fool", "gambar": "00.png"},
    {"nama": "The Magician", "gambar": "01.png"},
    {"nama": "The High Priestess", "gambar": "02.png"},
    {"nama": "The Empress", "gambar": "03.png"},
    {"nama": "The Emperor", "gambar": "04.png"},
    {"nama": "The Hierophant", "gambar": "05.png"},
    {"nama": "The Lovers", "gambar": "06.png"},
    {"nama": "The Chariot", "gambar": "07.png"},
    {"nama": "Strength", "gambar": "08.png"},
    {"nama": "The Hermit", "gambar": "09.png"},
    {"nama": "Wheel of Fortune", "gambar": "10.png"},
    {"nama": "Justice", "gambar": "11.png"},
    {"nama": "The Hanged Man", "gambar": "12.png"},
    {"nama": "Death", "gambar": "13.png"},
    {"nama": "Temperance", "gambar": "14.png"},
    {"nama": "The Devil", "gambar": "15.png"},
    {"nama": "The Tower", "gambar": "16.png"},
    {"nama": "The Star", "gambar": "17.png"},
    {"nama": "The Moon", "gambar": "18.png"},
    {"nama": "The Sun", "gambar": "19.png"},
    {"nama": "Judgement", "gambar": "20.png"},
    {"nama": "The World", "gambar": "21.png"}
]

def kocok_dek():
    return random.sample(DEK, len(DEK))

def tarik_kartu(dek, jumlah=3):
    if jumlah < 1 or len(dek) < jumlah:
        raise ValueError("Jumlah kartu tidak mencukupi.")
    return [dek.pop() for _ in range(jumlah)]

def path_gambar(nama):
    path = os.path.join(FOLDER_GAMBAR, nama)
    return path if os.path.exists(path) else None