import os
import sys
import json
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from github_upload import upload_pdf_github
from pdf_service import generate_pdf
from whatsapp_service import kirim_whatsapp
from laporan import export_excel

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.align import Align
from rich.columns import Columns
from rich.progress import Progress
from rich import box

from pyfiglet import Figlet

import questionary

from datetime import datetime

try:
    from dotenv import load_dotenv
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False

    def load_dotenv():
        pass

try:
    import winsound
except:
    winsound = None


# =========================================================
# CONSOLE
# =========================================================

console = Console()


# =========================================================
# DATABASE FILE
# =========================================================

DB_FILE = os.path.join(BASE_DIR, "transaksi.json")


# =========================================================
# DATA
# =========================================================

queue = []

# SLOT JADI 2
slots = [
    {"id": 1, "status": "Kosong", "mobil": None},
    {"id": 2, "status": "Kosong", "mobil": None},
]

transaksi = []

next_invoice = 1
next_queue = 1


# =========================================================
# DATABASE
# =========================================================

def simpan_transaksi():

    try:

        with open(DB_FILE, "w", encoding="utf-8") as file:

            json.dump(
                transaksi,
                file,
                indent=4,
                ensure_ascii=False
            )

    except Exception as e:

        error(f"Gagal menyimpan transaksi: {e}")


def load_transaksi():

    global transaksi
    global next_invoice

    if not os.path.exists(DB_FILE):

        transaksi = []

        return

    try:

        with open(DB_FILE, "r", encoding="utf-8") as file:

            transaksi = json.load(file)

        if transaksi:

            invoice_terakhir = transaksi[-1]["invoice"]

            nomor = int(
                invoice_terakhir.split("-")[1]
            )

            next_invoice = nomor + 1

    except Exception as e:

        transaksi = []

        error(f"Gagal load transaksi: {e}")


# =========================================================
# ADMIN
# =========================================================

load_dotenv()

USERNAME = os.getenv("ADMIN_USERNAME", "admin")
PASSWORD = os.getenv("ADMIN_PASSWORD", "123")


# =========================================================
# STYLE
# =========================================================

custom_style = questionary.Style([
    ('qmark', 'fg:#00ffff bold'),
    ('question', 'bold fg:#00ffff'),
    ('answer', 'fg:#ffffff bold'),
    ('pointer', 'fg:#00ffff bold'),
    ('highlighted', 'fg:#00ffff bold'),
])


# =========================================================
# CLEAR
# =========================================================

def clear():

    os.system("cls" if os.name == "nt" else "clear")


# =========================================================
# SOUND
# =========================================================

def beep():

    try:

        if winsound:

            winsound.Beep(1200, 120)

        else:

            print("\a")

    except:

        pass


# =========================================================
# SUCCESS
# =========================================================

def success(msg):

    beep()

    console.print(
        Align.center(
            Panel(
                f"[bold bright_cyan]{msg}[/bold bright_cyan]",
                border_style="bright_cyan",
                width=70
            )
        )
    )


# =========================================================
# ERROR
# =========================================================

def error(msg):

    console.print(
        Align.center(
            Panel(
                f"[bold red]{msg}[/bold red]",
                border_style="red",
                width=70
            )
        )
    )


# =========================================================
# PAUSE
# =========================================================

def pause():

    console.print(
        "\n[cyan]Tekan Enter untuk lanjut...[/cyan]"
    )

    input()


# =========================================================
# LOADING
# =========================================================

def loading():

    clear()

    console.print("\n")

    console.print(
        Align.center(
            "[bold bright_cyan]INITIALIZING SYSTEM[/bold bright_cyan]"
        )
    )

    with Progress() as progress:

        task = progress.add_task(
            "[cyan]Loading...",
            total=100
        )

        while not progress.finished:

            progress.update(task, advance=2)

            time.sleep(0.03)

    beep()


# =========================================================
# HEADER
# =========================================================

def header():

    fig = Figlet(font="slant")

    title = fig.renderText("MSJ CARWASH")

    panel = Panel(
        Align.center(
            f"[bold bright_cyan]{title}[/bold bright_cyan]\n"
            "[cyan]Professional Carwash Management[/cyan]"
        ),
        border_style="bright_cyan",
        box=box.DOUBLE,
        width=90
    )

    console.print(Align.center(panel))


# =========================================================
# DASHBOARD
# =========================================================

def dashboard():

    jumlah_antrian = len(queue)

    jumlah_transaksi = len(transaksi)

    total_pendapatan = sum(
        item["harga"]
        for item in transaksi
    )

    panel1 = Panel(
        Align.center(
            f"[bold bright_cyan]{jumlah_antrian}[/bold bright_cyan]\n"
            "Antrian"
        ),
        border_style="cyan",
        width=25
    )

    panel2 = Panel(
        Align.center(
            f"[bold bright_cyan]{jumlah_transaksi}[/bold bright_cyan]\n"
            "Transaksi"
        ),
        border_style="cyan",
        width=25
    )

    panel3 = Panel(
        Align.center(
            f"[bold bright_cyan]Rp {total_pendapatan:,}[/bold bright_cyan]\n"
            "Pendapatan"
        ),
        border_style="cyan",
        width=25
    )

    console.print(
        Align.center(
            Columns([panel1, panel2, panel3])
        )
    )


# =========================================================
# MENU
# =========================================================

def menu():

    table = Table(
        title="[bold bright_cyan]MAIN MENU[/bold bright_cyan]",
        border_style="cyan",
        box=box.ROUNDED,
        width=60
    )

    table.add_column("NO", justify="center")
    table.add_column("FITUR")

    table.add_row("1", "Tambah Mobil")
    table.add_row("2", "Tampilkan Antrian")
    table.add_row("3", "Masukkan ke slot antrean")
    table.add_row("4", "Tampilkan Slot")
    table.add_row("5", "Selesaikan Cuci")
    table.add_row("6", "Riwayat Transaksi")
    table.add_row("7", "Export Excel")
    table.add_row("0", "Keluar")

    console.print(Align.center(table))


# =========================================================
# LOGIN
# =========================================================

def login():

    while True:

        clear()

        console.print("\n")

        console.print(
            Align.center(
                Panel(
                    "[bold bright_cyan]ADMIN LOGIN[/bold bright_cyan]",
                    border_style="bright_cyan",
                    box=box.DOUBLE,
                    width=60
                )
            )
        )

        username = questionary.text(
            "Username:",
            style=custom_style
        ).ask()

        password = questionary.password(
            "Password:",
            style=custom_style
        ).ask()

        if username is None or password is None:
            error("ACCESS DENIED")
            time.sleep(1.5)
            continue

        if username == USERNAME and password == PASSWORD:

            success("ACCESS GRANTED")

            time.sleep(1)

            return

        else:

            error("ACCESS DENIED")

            time.sleep(1.5)


# =========================================================
# TAMBAH MOBIL
# =========================================================

def tambah_mobil():

    global next_queue

    clear()

    header()

    nama = questionary.text(
        "Nama pelanggan:",
        style=custom_style
    ).ask()

    no_hp = questionary.text(
        "Nomor WhatsApp:",
        style=custom_style
    ).ask()

    plat = questionary.text(
        "Plat nomor:",
        style=custom_style
    ).ask()

    layanan = questionary.select(
        "Jenis layanan:",
        choices=[
            "Cuci Biasa",
            "Premium Wash",
        ],
        style=custom_style
    ).ask()

    if layanan is None:
        error("Layanan harus dipilih")
        pause()
        return

    # HARGA OTOMATIS
    if layanan == "Cuci Biasa":

        harga = 50000

    elif layanan == "Premium Wash":

        harga = 85000

    kode_antrian = f"A-{next_queue:03d}"

    data = {
        "queue_id": kode_antrian,
        "nama": nama,
        "no_hp": no_hp,
        "plat": plat,
        "layanan": layanan,
        "harga": harga,
        "waktu": datetime.now().strftime("%d-%m-%Y %H:%M")
    }

    queue.append(data)

    next_queue += 1

    success(
        f"Mobil berhasil masuk antrian!\nQueue ID: {kode_antrian}"
    )

    pause()


# =========================================================
# TAMPILKAN ANTRIAN
# =========================================================

def tampilkan_antrian():

    clear()

    header()

    if not queue:

        error("Antrian kosong!")

        pause()

        return

    table = Table(
        title="[bold bright_cyan]DAFTAR ANTRIAN[/bold bright_cyan]",
        border_style="cyan",
        box=box.DOUBLE_EDGE,
        width=120,
        show_lines=True
    )

    table.add_column("QUEUE")
    table.add_column("NAMA")
    table.add_column("PLAT")
    table.add_column("LAYANAN")
    table.add_column("HARGA")

    for item in queue:

        table.add_row(
            item["queue_id"],
            item["nama"],
            item["plat"],
            item["layanan"],
            f"Rp {item['harga']:,}"
        )

    console.print(Align.center(table))

    pause()


# =========================================================
# TAMPILKAN SLOT
# =========================================================

def tampilkan_slot():

    clear()

    header()

    table = Table(
        title="[bold bright_cyan]CARWASH SLOT[/bold bright_cyan]",
        border_style="bright_cyan",
        box=box.DOUBLE_EDGE,
        width=100,
        show_lines=True
    )

    table.add_column("SLOT")
    table.add_column("QUEUE")
    table.add_column("NAMA")
    table.add_column("PLAT")

    for slot in slots:

        if slot["mobil"]:

            table.add_row(
                str(slot["id"]),
                slot["mobil"]["queue_id"],
                slot["mobil"]["nama"],
                slot["mobil"]["plat"]
            )

        else:

            table.add_row(
                str(slot["id"]),
                "-",
                "-",
                "-"
            )

    console.print(Align.center(table))

    pause()


# =========================================================
# ASSIGN SLOT
# =========================================================

def assign_slot():

    clear()

    header()

    if not queue:

        error("Antrian kosong!")

        pause()

        return

    slot_kosong = None

    for slot in slots:

        if slot["status"] == "Kosong":

            slot_kosong = slot

            break

    if not slot_kosong:

        error("Semua slot penuh!")

        pause()

        return

    mobil = queue.pop(0)

    slot_kosong["status"] = "Terisi"

    slot_kosong["mobil"] = mobil

    success(
        f"{mobil['queue_id']} masuk Slot {slot_kosong['id']}"
    )

    pause()


# =========================================================
# SELESAI CUCI
# =========================================================

def selesai_cuci():

    global next_invoice

    clear()

    header()

    for slot in slots:

        if slot["mobil"]:

            console.print(
                f"[cyan]Slot {slot['id']}[/cyan] : "
                f"{slot['mobil']['queue_id']} - "
                f"{slot['mobil']['nama']}"
            )

        else:

            console.print(
                f"[cyan]Slot {slot['id']}[/cyan] : Kosong"
            )

    try:

        slot_input = questionary.text(
            "Masukkan ID Slot:",
            style=custom_style
        ).ask()

        if slot_input is None:
            error("Input slot tidak boleh kosong")
            pause()
            return

        id_slot = int(slot_input)

    except:

        error("Input harus angka!")

        pause()

        return

    target = None

    for slot in slots:

        if slot["id"] == id_slot:

            target = slot

            break

    if not target:

        error("Slot tidak ditemukan!")

        pause()

        return

    if target["status"] == "Kosong":

        error("Slot masih kosong!")

        pause()

        return

    mobil = target["mobil"]

    invoice = f"INV-{next_invoice:04d}"

    data_transaksi = {
        "queue_id": mobil["queue_id"],
        "invoice": invoice,
        "nama": mobil["nama"],
        "no_hp": mobil["no_hp"],
        "plat": mobil["plat"],
        "layanan": mobil["layanan"],
        "harga": mobil["harga"],
        "tanggal": datetime.now().strftime("%d-%m-%Y %H:%M")
    }

    transaksi.append(data_transaksi)

    simpan_transaksi()

    try:

        pdf_file = generate_pdf(data_transaksi)

        pdf_url = upload_pdf_github(pdf_file)

    except Exception as e:

        error(f"Gagal generate PDF: {e}")

        pdf_url = None

    try:

        kirim_whatsapp(
            mobil["no_hp"],
            f"""
Halo {mobil['nama']}

Terima kasih telah menggunakan layanan MSJ Carwash.

Invoice:
{invoice}

Total:
Rp {mobil['harga']:,}

Download PDF:
{pdf_url if pdf_url else 'PDF tidak tersedia'}
""",
            pdf_url if pdf_url else ""
        )

    except Exception as e:

        error(f"Gagal kirim WhatsApp : {e}")

    target["status"] = "Kosong"
    target["mobil"] = None

    # AUTO ASSIGN
    if queue:

        mobil_baru = queue.pop(0)

        target["status"] = "Terisi"

        target["mobil"] = mobil_baru

        success(
            f"{mobil_baru['queue_id']} otomatis masuk Slot {target['id']}"
        )

    next_invoice += 1

    success("Pencucian selesai!")

    pause()


# =========================================================
# RIWAYAT TRANSAKSI
# =========================================================

def tampilkan_transaksi():

    clear()

    header()

    if not transaksi:

        error("Belum ada transaksi!")

        pause()

        return

    table = Table(
        title="[bold bright_cyan]TRANSAKSI[/bold bright_cyan]",
        border_style="cyan",
        box=box.DOUBLE_EDGE,
        width=140,
        show_lines=True
    )

    table.add_column("QUEUE")
    table.add_column("INVOICE")
    table.add_column("NAMA")
    table.add_column("PLAT")
    table.add_column("LAYANAN")
    table.add_column("TOTAL")
    table.add_column("TANGGAL")

    for item in transaksi:

        table.add_row(
            item["queue_id"],
            item["invoice"],
            item["nama"],
            item["plat"],
            item["layanan"],
            f"Rp {item['harga']:,}",
            item["tanggal"]
        )

    console.print(Align.center(table))

    pause()


# =========================================================
# FILTER TRANSAKSI
# =========================================================

def filter_transaksi(mode):

    sekarang = datetime.now()

    hasil = []

    for item in transaksi:

        tanggal = datetime.strptime(
            item["tanggal"],
            "%d-%m-%Y %H:%M"
        )

        if mode == "harian":

            if tanggal.date() == sekarang.date():

                hasil.append(item)

        elif mode == "bulanan":

            if (
                tanggal.month == sekarang.month
                and
                tanggal.year == sekarang.year
            ):

                hasil.append(item)

    return hasil


# =========================================================
# EXPORT EXCEL
# =========================================================

def export_excel_menu():

    pilihan = questionary.select(
        "Export laporan:",
        choices=[
            "Harian",
            "Bulanan"
        ],
        style=custom_style
    ).ask()

    if pilihan is None:
        pause()
        return

    mode = "harian" if pilihan == "Harian" else "bulanan"

    data_filter = filter_transaksi(mode)

    if not data_filter:

        error("Tidak ada transaksi!")

        pause()

        return

    filename = export_excel(type(
        "obj",
        (object,),
        {"daftar_transaksi": data_filter}
    ))

    success(
        f"Laporan {pilihan} berhasil dibuat:\n{filename}"
    )

    pause()

# =========================================================
# MAIN
# =========================================================

def main():

    loading()

    load_transaksi()

    login()

    while True:

        clear()

        header()

        dashboard()

        menu()

        pilihan = questionary.select(
            "Pilih menu:",
            choices=[
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "0"
            ],
            style=custom_style
        ).ask()

        if pilihan is None:
            continue

        if pilihan == "1":

            tambah_mobil()

        elif pilihan == "2":

            tampilkan_antrian()

        elif pilihan == "3":

            assign_slot()

        elif pilihan == "4":

            tampilkan_slot()

        elif pilihan == "5":

            selesai_cuci()

        elif pilihan == "6":

            tampilkan_transaksi()

        elif pilihan == "7":

            export_excel_menu()

        elif pilihan == "0":

            clear()

            console.print("\n")

            console.print(
                Align.center(
                    Panel(
                        "[bold bright_cyan]THANK YOU[/bold bright_cyan]\n"
                        "[cyan]MSJ CARWASH SYSTEM[/cyan]",
                        border_style="bright_cyan",
                        box=box.DOUBLE,
                        width=60
                    )
                )
            )

            break


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":

    main()