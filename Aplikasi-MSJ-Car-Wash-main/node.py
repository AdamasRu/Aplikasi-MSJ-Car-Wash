from datetime import datetime

class NodeMobil:

    def __init__(
        self,
        id_antrian,
        nama_pelanggan,
        no_hp,
        plat_nomor,
        jenis_layanan,
        harga,
        waktu_masuk=None
    ):

        self.id_antrian = id_antrian

        self.nama_pelanggan = nama_pelanggan

        self.no_hp = no_hp

        self.plat_nomor = plat_nomor

        self.jenis_layanan = jenis_layanan

        self.harga = harga

        self.waktu_masuk = (
            waktu_masuk
            if waktu_masuk
            else datetime.now()
        )

        self.status = "MENUNGGU"

        self.next = None


    def __str__(self):

        return (
            f"[{self.id_antrian}] "
            f"{self.nama_pelanggan} - "
            f"{self.plat_nomor}"
        )