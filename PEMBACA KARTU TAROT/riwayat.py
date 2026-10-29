format_ramalan = lambda c: (
    f"#{c['no']} {c['nama']} bertanya \"{c['pertanyaan']}\" -> "
    + ", ".join(f"{posisi}: {kartu['nama']}" for posisi, kartu in c["kartu"])
)
 
 
def simpan_hasil(riwayat, sesi, kartu_terpilih):
    """Menaruh hasil ramalan di puncak tumpukan riwayat."""
    riwayat.append({
        "no": sesi["no"],
        "nama": sesi["nama"],
        "pertanyaan": sesi["pertanyaan"],
        "kartu": kartu_terpilih,
    })
 
 
def lihat_riwayat(riwayat):
    """Daftar riwayat dari yang TERBARU (puncak) ke yang terlama."""
    return list(reversed(riwayat))
 