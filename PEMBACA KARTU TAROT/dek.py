import os
import random
 
# Folder gambar: tarot_web/gambar (naik dua tingkat dari modul/dek.py)
FOLDER_GAMBAR = os.path.join(os.path.dirname(__file__), "gambar")
EKSTENSI = (".png",)
 
# lambda: "The Sun", "the-sun", "THE SUN" -> "the_sun"
nama_file = lambda nama: nama.strip().lower().replace(" ", "_").replace("-", "_")
 
# Posisi kartu pada satu sesi ramalan (tuple = data tetap).
POSISI = ("Masa lalu", "Masa kini", "Masa depan")
 
# 22 kartu Major Arcana. Tuple berisi dict supaya data tetap tidak berubah urutannya.
DAFTAR_KARTU = (
    {"nama": "The Fool", "arti": "Awal baru dan keberanian mencoba. Lompat dulu, rapikan rencana belakangan."},
    {"nama": "The Magician", "arti": "Kamu punya semua alat yang dibutuhkan. Tinggal mulai memakainya."},
    {"nama": "The High Priestess", "arti": "Dengarkan intuisi. Jawabannya sudah ada, hanya belum kamu akui."},
    {"nama": "The Empress", "arti": "Masa subur untuk kreativitas dan perhatian pada orang terdekat."},
    {"nama": "The Emperor", "arti": "Butuh disiplin dan aturan main yang jelas agar urusan tidak berantakan."},
    {"nama": "The Hierophant", "arti": "Ikuti cara yang sudah terbukti. Minta saran dari orang yang lebih paham."},
    {"nama": "The Lovers", "arti": "Pilihan penting soal hubungan atau nilai hidup. Pilih yang jujur."},
    {"nama": "The Chariot", "arti": "Tekad kuat membawamu maju. Kendalikan arah, jangan ikut arus."},
    {"nama": "Strength", "arti": "Kekuatan datang dari sabar dan lembut, bukan dari memaksa."},
    {"nama": "The Hermit", "arti": "Waktunya menyendiri sebentar untuk berpikir jernih."},
    {"nama": "Wheel of Fortune", "arti": "Keadaan berputar. Yang di bawah akan naik, yang di atas jangan lengah."},
    {"nama": "Justice", "arti": "Semua ada konsekuensinya. Timbang dengan adil sebelum memutuskan."},
    {"nama": "The Hanged Man", "arti": "Berhenti sejenak dan lihat masalah dari sudut pandang lain."},
    {"nama": "Death", "arti": "Satu fase berakhir supaya fase baru bisa mulai. Bukan berarti seram."},
    {"nama": "Temperance", "arti": "Cari keseimbangan. Jangan ekstrem ke satu sisi."},
    {"nama": "The Devil", "arti": "Waspada kebiasaan atau godaan yang mengikatmu tanpa sadar."},
    {"nama": "The Tower", "arti": "Perubahan mendadak. Menyakitkan, tetapi membersihkan yang memang rapuh."},
    {"nama": "The Star", "arti": "Harapan dan pemulihan. Pelan-pelan, keadaan membaik."},
    {"nama": "The Moon", "arti": "Situasi belum jelas. Tunda keputusan besar sampai informasinya lengkap."},
    {"nama": "The Sun", "arti": "Kabar baik, energi positif, dan hasil yang terang."},
    {"nama": "Judgement", "arti": "Saatnya evaluasi diri dan memutuskan bangkit."},
    {"nama": "The World", "arti": "Satu siklus selesai dengan utuh. Rayakan pencapaianmu."},
)
 
 
def buat_dek():
    """Membuat dek baru berisi semua kartu (salinan, urutan belum dikocok)."""
    return [dict(kartu) for kartu in DAFTAR_KARTU]
 
 
def kocok_dek(dek):
    """Mengocok dek di tempat, lalu mengembalikannya."""
    random.shuffle(dek)
    return dek
 
 
def siapkan_dek():
    """Dek baru yang langsung dikocok."""
    return kocok_dek(buat_dek())
 
 
def tarik_kartu(dek, jumlah=3):
    """Menarik kartu dari PUNCAK tumpukan (pop = LIFO).
 
    Mengembalikan list tuple (posisi, kartu).
    Jika kartu di dek tidak cukup, dek diisi ulang dan dikocok dulu (di tempat).
    """
    jumlah = min(jumlah, len(POSISI))
    if len(dek) < jumlah:
        dek[:] = siapkan_dek()
    return [(POSISI[i], dek.pop()) for i in range(jumlah)]
 
 
# lambda: hanya huruf kecil, tanpa angka/spasi/tanda baca. "00-TheFool" -> "thefool"
huruf = lambda teks: "".join(c for c in teks.lower() if c.isalpha())


def _tanpa_ekstensi(berkas):
    """Nama file tanpa ekstensi (termasuk ekstensi ganda seperti the_sun.jpg.jpg)."""
    dasar, ekstensi = os.path.splitext(berkas)
    while ekstensi.lower() in EKSTENSI:
        berkas = dasar
        dasar, ekstensi = os.path.splitext(berkas)
    return berkas


def path_gambar(kartu):
    """Alamat file gambar sebuah kartu. None jika filenya belum ada.

    Yang dibandingkan hanya huruf-hurufnya (angka, spasi, garis, huruf besar/kecil diabaikan).
    File cocok jika namanya berakhir dengan nama kartu tanpa "The", contohnya kartu The Fool:
    the_fool.jpg, 00-TheFool.png, RWS_Tarot_00_Fool.jpg
    """
    if not os.path.isdir(FOLDER_GAMBAR):
        return None
    lengkap = huruf(kartu["nama"])                                   # "thefool"
    pendek = lengkap[3:] if lengkap.startswith("the") else lengkap   # "fool"
    for berkas in sorted(os.listdir(FOLDER_GAMBAR)):
        if os.path.splitext(berkas)[1].lower() not in EKSTENSI:
            continue
        if huruf(_tanpa_ekstensi(berkas)).endswith(pendek):
            return os.path.join(FOLDER_GAMBAR, berkas)
    return None