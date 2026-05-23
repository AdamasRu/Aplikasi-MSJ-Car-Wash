from rich.table import Table
from rich.console import Console
from rich import box
from rich.align import Align

console = Console()

class QueueLL:

    def __init__(self):

        self.front = None
        self.rear = None


    def enqueue(self, node):

        if self.rear is None:

            self.front = self.rear = node

            return

        self.rear.next = node

        self.rear = node


    def dequeue(self):

        if self.front is None:
            return None

        temp = self.front

        self.front = self.front.next

        if self.front is None:
            self.rear = None

        return temp


    def is_empty(self):

        return self.front is None


    def display_queue(self):

        if self.front is None:

            console.print(
                "\n[bold red]Antrian kosong[/bold red]"
            )

            return

        table = Table(
            title="DAFTAR ANTRIAN",
            border_style="cyan",
            box=box.ROUNDED
        )

        table.add_column("NO")
        table.add_column("Nama")
        table.add_column("No HP")
        table.add_column("Plat")
        table.add_column("Layanan")
        table.add_column("Harga")

        current = self.front

        nomor = 1

        while current:

            table.add_row(
                str(nomor),
                current.nama_pelanggan,
                current.no_hp,
                current.plat_nomor,
                current.jenis_layanan,
                f"Rp {current.harga:,}"
            )

            current = current.next

            nomor += 1

        console.print(
            Align.center(table)
        )