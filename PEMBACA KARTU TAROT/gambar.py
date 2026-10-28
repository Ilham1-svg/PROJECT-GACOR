"""gambar.py
Mengurus gambar kartu tarot: mencari file gambar dari folder gambar/.
"""
import os

# folder gambar/ berada sejajar dengan file ini (satu folder dengan app.py)
folder_gambar = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gambar")

# lambda: "The Sun" -> "thesun", "Wheel of Fortune" -> "wheeloffortune"
kunci_kartu = lambda nama: nama.replace(" ", "").lower()


def path_gambar(kartu):
    """Alamat file gambar sebuah kartu. None jika filenya belum ada.

    File di folder bernama seperti "19-TheSun.png": nomor di depan diabaikan,
    lalu dicocokkan dengan nama kartu tanpa spasi dan tanpa membedakan huruf besar/kecil.
    """
    if not os.path.isdir(folder_gambar):
        return None
    kunci = kunci_kartu(kartu["nama"])
    for nama_berkas in os.listdir(folder_gambar):
        dasar, ekstensi = os.path.splitext(nama_berkas)
        if ekstensi.lower() == ".png" and dasar.split("-", 1)[-1].lower() == kunci:
            return os.path.join(folder_gambar, nama_berkas)
    return None
