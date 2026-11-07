import random
import requests
from functools import lru_cache
import os

OPENAI_URL = "https://api.openai.com/v1/chat/completions"
API_KEY = os.getenv("OPENAI_API_KEY")
FOLDER_GAMBAR = os.path.join(os.path.dirname(__file__), "gambar")

DEK = [
    {"nama": "The Fool", "kode_api": "ar00", "gambar": "00.png"},
    {"nama": "The Magician", "kode_api": "ar01", "gambar": "01.png"},
    {"nama": "The High Priestess", "kode_api": "ar02", "gambar": "02.png"},
    {"nama": "The Empress", "kode_api": "ar03", "gambar": "03.png"},
    {"nama": "The Emperor", "kode_api": "ar04", "gambar": "04.png"},
    {"nama": "The Hierophant", "kode_api": "ar05", "gambar": "05.png"},
    {"nama": "The Lovers", "kode_api": "ar06", "gambar": "06.png"},
    {"nama": "The Chariot", "kode_api": "ar07", "gambar": "07.png"},
    {"nama": "Strength", "kode_api": "ar08", "gambar": "08.png"},
    {"nama": "The Hermit", "kode_api": "ar09", "gambar": "09.png"},
    {"nama": "Wheel of Fortune", "kode_api": "ar10", "gambar": "10.png"},
    {"nama": "Justice", "kode_api": "ar11", "gambar": "11.png"},
    {"nama": "The Hanged Man", "kode_api": "ar12", "gambar": "12.png"},
    {"nama": "Death", "kode_api": "ar13", "gambar": "13.png"},
    {"nama": "Temperance", "kode_api": "ar14", "gambar": "14.png"},
    {"nama": "The Devil", "kode_api": "ar15", "gambar": "15.png"},
    {"nama": "The Tower", "kode_api": "ar16", "gambar": "16.png"},
    {"nama": "The Star", "kode_api": "ar17", "gambar": "17.png"},
    {"nama": "The Moon", "kode_api": "ar18", "gambar": "18.png"},
    {"nama": "The Sun", "kode_api": "ar19", "gambar": "19.png"},
    {"nama": "Judgement", "kode_api": "ar20", "gambar": "20.png"},
    {"nama": "The World", "kode_api": "ar21", "gambar": "21.png"},
]


def kocok_dek():
    return random.sample(DEK, len(DEK))


def tarik_kartu(dek, jumlah=3):
    if jumlah < 1 or len(dek) < jumlah:
        raise ValueError("Jumlah kartu tidak mencukupi.")
    return [dek.pop() for _ in range(jumlah)]


@lru_cache(maxsize=66)
def _interpretasi_ai(nama, topik, posisi):
    if not API_KEY:
        raise RuntimeError("OPENAI_API_KEY belum tersedia.")
    prompt = f"""
    Buat interpretasi kartu Tarot {nama}.
    Pertanyaan pengguna: {topik}
    Posisi kartu: {posisi}.

    Gunakan Bahasa Indonesia yang sederhana.
    Jelaskan secara rinci dalam 2 paragraf.
    Hubungkan arti kartu dengan pertanyaan pengguna.
    Berikan saran yang realistis dan bersifat refleksi.
    Jangan menyatakan ramalan sebagai kepastian.
    """
    try:
        response = requests.post(
            OPENAI_URL,
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={
                "model": "gpt-4.1-mini",
                "messages": [{"role": "user", "content": prompt}],
                "max_completion_tokens": 400
            },
            timeout=30
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
    except (requests.RequestException, ValueError, KeyError, IndexError) as error:
        raise RuntimeError("Gagal mendapatkan interpretasi AI.") from error

def arti_kartu(kartu, topik=None, posisi="upright"):
    if posisi not in ("upright", "reversed"):
        raise ValueError("Posisi kartu tidak valid.")
    return _interpretasi_ai(kartu["nama"], topik or "Umum", posisi)

def path_gambar(nama):
    path = os.path.join(FOLDER_GAMBAR, nama)
    return path if os.path.exists(path) else None

def bersihkan_cache_api():
    _interpretasi_ai.cache_clear()
