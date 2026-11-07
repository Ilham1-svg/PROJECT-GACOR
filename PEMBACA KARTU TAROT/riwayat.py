
def simpan_riwayat(riwayat, hasil):
    catatan = {
        "nama": hasil["nama"],
        "pertanyaan": hasil["pertanyaan"],
        "kartu": [kartu.copy() for kartu in hasil["kartu"]],
        "arti": hasil["arti"].copy()
    }
    riwayat.append(catatan)
    return catatan
