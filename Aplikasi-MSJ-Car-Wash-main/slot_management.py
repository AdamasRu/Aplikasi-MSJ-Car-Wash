slots = [
    {"id": 1, "mobil": None},
    {"id": 2, "mobil": None},
    {"id": 3, "mobil": None},
]

def tampilkan_slot(console):

    console.print("\n[bold cyan]STATUS SLOT[/bold cyan]\n")

    for slot in slots:

        if slot["mobil"]:

            mobil = slot["mobil"]

            console.print(
                f"Slot {slot['id']} : "
                f"{mobil.plat_nomor}"
            )

        else:

            console.print(
                f"Slot {slot['id']} : KOSONG"
            )


def assign_slot(queue):

    if queue.is_empty():
        return None

    for slot in slots:

        if slot["mobil"] is None:

            mobil = queue.dequeue()

            slot["mobil"] = mobil

            mobil.status = "DICUCI"

            return slot

    return None


def selesai_cuci(slot_id):

    for slot in slots:

        if slot["id"] == slot_id:

            mobil = slot["mobil"]

            slot["mobil"] = None

            return mobil

    return None