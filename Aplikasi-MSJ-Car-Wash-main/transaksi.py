# transaksi.py

import json
import os
from datetime import datetime


# CLASS TRANSAKSI
class Transaksi:

    def __init__(
        self,
        id_transaksi: int,
        mobil,
        waktu_mulai,
        metode_pembayaran: str,
        waktu_selesai=None
    ):

        self.id_transaksi = id_transaksi

        self.nama_pelanggan = mobil.nama_pelanggan
        self.plat_nomor = mobil.plat_nomor
        self.jenis_layanan = mobil.jenis_layanan
        self.harga = mobil.harga

        self.waktu_masuk = mobil.waktu_masuk
        self.waktu_mulai = waktu_mulai

        if waktu_selesai:
            self.waktu_selesai = waktu_selesai
        else:
            self.waktu_selesai = datetime.now()

        self.metode_pembayaran = metode_pembayaran


    # UBAH KE DICTIONARY
    def to_dict(self):

        return {

            "id_transaksi": self.id_transaksi,

            "nama_pelanggan": self.nama_pelanggan,

            "plat_nomor": self.plat_nomor,

            "jenis_layanan": self.jenis_layanan,

            "harga": self.harga,

            "waktu_masuk": str(self.waktu_masuk),

            "waktu_mulai": str(self.waktu_mulai),

            "waktu_selesai": str(self.waktu_selesai),

            "metode_pembayaran": self.metode_pembayaran
        }


    def __str__(self):

        return (
            f"[Transaksi {self.id_transaksi}] "
            f"{self.plat_nomor} | "
            f"{self.jenis_layanan} | "
            f"Rp {self.harga}"
        )


# CLASS TRANSAKSI MANAGER
class TransaksiManager:

    def __init__(self):

        self.file_path = os.path.join(os.path.dirname(__file__), "data", "transaksi.json")

        self.daftar_transaksi = []

        self.next_id = 1

        self.load_transaksi()


    # LOAD DARI JSON
    def load_transaksi(self):

        if not os.path.exists(self.file_path):

            with open(self.file_path, "w") as file:
                json.dump([], file)

        with open(self.file_path, "r") as file:

            try:

                data = json.load(file)

                self.daftar_transaksi = data

                if data:

                    last_id = data[-1]["id_transaksi"]

                    self.next_id = last_id + 1

                else:

                    self.next_id = 1

            except json.JSONDecodeError:

                self.daftar_transaksi = []

                self.next_id = 1


    # SAVE KE JSON
    def save_transaksi(self):

        with open(self.file_path, "w") as file:

            json.dump(
                self.daftar_transaksi,
                file,
                indent=4
            )


    # CREATE TRANSAKSI
    def buat_transaksi(
        self,
        mobil,
        waktu_mulai,
        metode_pembayaran
    ):

        transaksi = Transaksi(
            id_transaksi=self.next_id,
            mobil=mobil,
            waktu_mulai=waktu_mulai,
            metode_pembayaran=metode_pembayaran
        )

        self.daftar_transaksi.append(
            transaksi.to_dict()
        )

        self.next_id += 1

        self.save_transaksi()

        print(
            f"Transaksi untuk "
            f"{transaksi.plat_nomor} berhasil dibuat."
        )

        return transaksi


    # READ TRANSAKSI
    def display_transaksi(self):

        if not self.daftar_transaksi:

            print("Belum ada transaksi.")

            return

        print("\n=== DAFTAR TRANSAKSI ===")

        for data in self.daftar_transaksi:

            print(
                f"[{data['id_transaksi']}] "
                f"{data['plat_nomor']} | "
                f"{data['jenis_layanan']} | "
                f"Rp {data['harga']}"
            )


    # TOTAL PENDAPATAN
    def hitung_total_pendapatan(self):

        total = 0

        for data in self.daftar_transaksi:

            total += data["harga"]

        return total