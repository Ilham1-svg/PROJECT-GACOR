format_ramalan = lambda c: (
    f"#{c['no']} {c['nama']} bertanya \"{c['pertanyaan']}\" -> "
    + ", ".join(f"{posisi}: {kartu['nama']}" for posisi, kartu in c["kartu"])
)
 
def simpan_hasil(riwayat, sesi, kartu_terpilih):
    riwayat.append({
        "no": sesi["no"],
        "nama": sesi["nama"],
        "pertanyaan": sesi["pertanyaan"],
        "kartu": kartu_terpilih,
    })
 
def lihat_riwayat(riwayat):
    return list(reversed(riwayat))
 