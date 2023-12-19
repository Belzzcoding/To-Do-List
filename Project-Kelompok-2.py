import os
os.system('cls')


import datetime as dt
FILE_NAME = "tugas.txt"

def save_task_to_file(tugas, waktu):
    with open(FILE_NAME, "a") as file:
        file.write(f"{tugas}|{waktu.strftime('%d-%m-%Y')}\n")

def save_tasks_to_file(tasks):
    with open(FILE_NAME, "w") as file:
        for task in tasks:
            file.write(f"{task['tugas']}|{task['waktu'].strftime('%d-%m-%Y')}\n")

def load_tasks_from_file():
    tasks = []
    try:
        with open(FILE_NAME, "r") as file:
            for line in file:
                task_data = line.strip().split("|")
                tugas = task_data[0]
                waktu = dt.datetime.strptime(task_data[1], '%d-%m-%Y')
                tasks.append({"tugas": tugas, "waktu": waktu})
    except FileNotFoundError:
        pass  # Jika file tidak ditemukan, tidak masalah; akan dibuat nanti
    return tasks

def urutkan_task():
    tasks = load_tasks_from_file()
    tasks_sorted = sorted(tasks, key=lambda x: x['waktu'])
    save_tasks_to_file(tasks_sorted)

def tambah_task():
    tugas = input('\nMasukkan tugas baru : ')
    waktu = input('Kapan waktunya? (contoh: dd-mm-yyyy): ')
    try:
        waktu = dt.datetime.strptime(waktu, '%d-%m-%Y')
    except ValueError:
        print("Format waktu tidak valid. Gunakan format seperti 'DD-MM-YYYY' ")
        return tambah_task()
    save_task_to_file(tugas, waktu)
    urutkan_task()
    print(f'\nTugas: `{tugas}`, berhasil ditambahkan.')

def lihat_task():
    tasks = load_tasks_from_file()
    if not tasks:
        print("\nTidak ada tugas tersedia.")
    else:
        # Mengurutkan tugas berdasarkan deadline terdekat
        urut_tugas = sorted(tasks, key=lambda x: x['waktu'])

        print()
        print("|" + "Daftar Tugas:".center(73) + "|")
        print('-'*75)
        print("|" + " ID "+"|" + " Deskripsi ".center(25) + "|" + " Waktu ".center(19) + "|" + " Deadline Dalam ".center(22) + "|")
        print('-'*75)
        for task_id, task in enumerate(urut_tugas, start=1):
            deskripsi = task['tugas']
            waktu = task['waktu'].strftime('%d-%m-%Y')
            hari_sisa = (task['waktu'].date() - dt.datetime.now().date()).days
            hari_sisa_str = f"{hari_sisa} hari" if hari_sisa > 0 else "Hari ini" if hari_sisa == 0 else "Telah lewat deadline"

            deskripsi_split = [deskripsi[i:i+23] for i in range(0, len(deskripsi), 23)]
            for i, deskripsi_part in enumerate(deskripsi_split):
                if i == 0:
                    print(f"| {task_id}. | {deskripsi_part.center(23)} | {waktu.center(17)} | {hari_sisa_str.center(20)} |")
                else:
                    print("|"+"    "+"|" f" {deskripsi_part.ljust(23)} " "|" +" ".center(19) + "|" + " ".center(22) + "|")
        print('-'*75)

def ubah_task():
    tasks = load_tasks_from_file()
    if not tasks:
        print("\nTidak ada tugas yang tersedia.")
        return

    lihat_task()
    try:
        task_index = int(input('\nMasukkan id tugas yang akan diedit: '))
        if 1 <= task_index <= len(tasks):
            edited_task = tasks[task_index - 1]
            tugas_baru = input('Masukkan tugas baru: ')
            waktu_baru = input('Masukkan waktunya (contoh: dd-mm-yyyy): ')
            try:
                waktu_baru = dt.datetime.strptime(waktu_baru, '%d-%m-%Y')
            except ValueError:
                print("Format waktu tidak valid. Gunakan format seperti 'DD-MM-YYYY' ")
                return ubah_task()

            edited_task['tugas'] = tugas_baru
            edited_task['waktu'] = waktu_baru

            with open(FILE_NAME, "w") as file:
                for task in tasks:
                    file.write(f"{task['tugas']}|{task['waktu'].strftime('%d-%m-%Y')}\n")

            urutkan_task()
            print('Tugas berhasil diubah.')
        else:
            print('Id tugas tidak valid. Silahkan coba lagi.')
            return ubah_task()
    except ValueError:
        print('Id tugas tidak valid. Silahkan coba lagi.')
        return ubah_task()

def hapus_task():
    tasks = load_tasks_from_file()
    if not tasks:
        print("\nTidak ada tugas yang tersedia.")
        return

    lihat_task()
    try:
        task_index = int(input('\nMasukkan id tugas yang akan dihapus: '))
        if 1 <= task_index <= len(tasks):
            with open(FILE_NAME, "w") as file:
                for i, task in enumerate(tasks):
                    if i != task_index - 1:
                        file.write(f"{task['tugas']}|{task['waktu'].strftime('%d-%m-%Y')}\n")
            urutkan_task()
            print('Tugas berhasil dihapus.')
        else:
            print('Id tugas tidak valid. Silahkan coba lagi.')
            return hapus_task()
    except ValueError:
        print('Id tugas tidak valid. Silahkan coba lagi.')
        return hapus_task()

while True:
    print('\n===Aplikasi To-Do List===')
    print("1. Tambah Tugas")
    print("2. Tampilkan Tugas")
    print("3. Edit Tugas")
    print("4. Hapus Tugas")
    print("5. Keluar")

    pilih = input("Pilih opsi (1/2/3/4/5): ")

    if pilih == '1':
        print('1. Tambah Tugas')
        tambah_task()
    elif pilih == '2':
        print('2. Tampilkan Tugas')
        lihat_task()
    elif pilih == '3':
        print('3. Edit Tugas')
        ubah_task()
    elif pilih == '4':
        print('4. Hapus Tugas')
        hapus_task()
    elif pilih == '5':
        print('Goodbye:)\n')
        break
    else:
        print("Pilihan tidak valid. Silakan pilih 1, 2, 3, 4, atau 5.")
