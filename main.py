import csv
from datetime import datetime
from collections import deque

FILE_CSV = "laundry.csv"

antrian = deque()

PAKET = {
    "Reguler": {"harga": 10000, "denda": 1000},
    "Express": {"harga": 15000, "denda": 2000}
}

def init_csv():
    try:
        with open(FILE_CSV, "x", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([
                "id","nama","berat","paket",
                "tanggal_masuk","status"
            ])
    except FileExistsError:
        pass

def load_data():
    data = []
    try:
        with open(FILE_CSV, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
    except FileNotFoundError:
        pass
    return data

def save_data(data):
    with open(FILE_CSV, "w", newline="", encoding="utf-8") as file:
        fieldnames = [
            "id","nama","berat","paket",
            "tanggal_masuk","status"
        ]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def hitung_harga(order):
    paket = order["paket"]
    berat = float(order["berat"])

    harga_awal = berat * PAKET[paket]["harga"]

    tanggal_masuk = datetime.strptime(
        order["tanggal_masuk"],
        "%Y-%m-%d"
    )

    hari = (datetime.now() - tanggal_masuk).days
    if hari < 0:
        hari = 0

    tambahan = hari * PAKET[paket]["denda"]
    return harga_awal + tambahan

def tambah_laundry():
    data = load_data()

    id_order = input("ID Order : ")

    for row in data:
        if row["id"] == id_order:
            print("ID sudah digunakan!")
            return

    nama = input("Nama Pelanggan : ")
    berat = input("Berat (kg) : ")

    print("1. Reguler")
    print("2. Express")

    pilih = input("Pilih Paket : ")
    paket = "Reguler" if pilih == "1" else "Express"

    order = {
        "id": id_order,
        "nama": nama,
        "berat": berat,
        "paket": paket,
        "tanggal_masuk": datetime.now().strftime("%Y-%m-%d"),
        "status": "Proses"
    }

    data.append(order)
    antrian.append(id_order)

    save_data(data)
    print("Laundry berhasil ditambahkan.")

def tampil_data():
    data = load_data()

    if not data:
        print("Data kosong.")
        return

    print("\n===== DATA LAUNDRY =====")

    for row in data:
        total = hitung_harga(row)

        print("-" * 40)
        print("ID      :", row["id"])
        print("Nama    :", row["nama"])
        print("Berat   :", row["berat"], "kg")
        print("Paket   :", row["paket"])
        print("Status  :", row["status"])
        print("Total   : Rp", format(int(total), ","))
        print("-" * 40)

def update_status():
    data = load_data()
    id_order = input("Masukkan ID : ")

    ditemukan = False

    for row in data:
        if row["id"] == id_order:
            print("1. Proses")
            print("2. Selesai")
            print("3. Diambil")

            pilih = input("Status Baru : ")

            if pilih == "1":
                row["status"] = "Proses"
            elif pilih == "2":
                row["status"] = "Selesai"
            elif pilih == "3":
                row["status"] = "Diambil"

            ditemukan = True
            break

    if ditemukan:
        save_data(data)
        print("Status berhasil diubah.")
    else:
        print("Data tidak ditemukan.")

def hapus_data():
    data = load_data()
    id_order = input("ID yang dihapus : ")

    data_baru = [row for row in data if row["id"] != id_order]

    save_data(data_baru)
    print("Data berhasil dihapus.")

def cari_data():
    keyword = input("Masukkan Nama / ID : ").lower()

    data = load_data()
    ditemukan = False

    for row in data:
        if keyword in row["id"].lower() or keyword in row["nama"].lower():
            total = hitung_harga(row)

            print("\nData Ditemukan")
            print("ID :", row["id"])
            print("Nama :", row["nama"])
            print("Total : Rp", format(int(total), ","))

            ditemukan = True

    if not ditemukan:
        print("Data tidak ditemukan.")

def sorting_harga():
    data = load_data()

    data.sort(
        key=lambda x: hitung_harga(x),
        reverse=True
    )

    print("\n===== HARGA TERTINGGI =====")

    for row in data:
        print(
            row["id"],
            row["nama"],
            "Rp",
            format(int(hitung_harga(row)), ",")
        )

def panggil_antrian():
    if len(antrian) == 0:
        print("Antrian kosong")
    else:
        print("Sedang diproses :", antrian.popleft())

def hashmap_pelanggan():
    data = load_data()

    pelanggan = {}

    for row in data:
        pelanggan[row["id"]] = row["nama"]

    print("\n===== HASH MAP PELANGGAN =====")

    for k, v in pelanggan.items():
        print(k, "=>", v)

def menu():
    init_csv()

    while True:
        print("""
===========================
SISTEM MANAJEMEN LAUNDRY
===========================
1. Tambah Laundry
2. Lihat Data
3. Update Status
4. Hapus Data
5. Cari Data
6. Sorting Harga
7. Panggil Antrian
8. Hash Map Pelanggan
9. Keluar
===========================
""")

        pilih = input("Pilih Menu : ")

        if pilih == "1":
            tambah_laundry()
        elif pilih == "2":
            tampil_data()
        elif pilih == "3":
            update_status()
        elif pilih == "4":
            hapus_data()
        elif pilih == "5":
            cari_data()
        elif pilih == "6":
            sorting_harga()
        elif pilih == "7":
            panggil_antrian()
        elif pilih == "8":
            hashmap_pelanggan()
        elif pilih == "9":
            print("Program selesai")
            break
        else:
            print("Menu tidak tersedia")

if __name__ == "__main__":
    menu()
