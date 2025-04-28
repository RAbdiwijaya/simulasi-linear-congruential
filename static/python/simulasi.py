from .logic import calculate_result

def simulasi_antrian(nasabah, max_kedatangan, max_pelayanan):
    """
    Simulasi antrian bank dengan ketentuan:
    - Kolom 1: No
    - Kolom 2: Waktu antar kedatangan
    - Kolom 3: Waktu kedatangan (kumulatif)
    - Kolom 4: Waktu pelayanan
    - Kolom 5: Waktu mulai dilayani
    - Kolom 6: Waktu selesai dilayani
    - Kolom 7: Waktu menunggu
    - Kolom 8: Waktu dalam sistem
    - Kolom 9: Waktu teller menganggur
    """
    # Generate data acak
    daftar_kedatangan = calculate_result(max_kedatangan)[:nasabah]
    daftar_pelayanan = calculate_result(max_pelayanan)[:nasabah]
    
    rows = []
    waktu_selesai_sebelumnya = 0  # Inisialisasi
    waktu_kedatangan_kumulatif = 0
    x = 0
    y = 0 
    z = 0

    for i in range(nasabah):
        # Kolom 1: Nomor
        nomor = i + 1

        # Kolom 2: Waktu antar kedatangan
        waktu_antar_kedatangan = daftar_kedatangan[i]
        waktu_kedatangan_kumulatif += waktu_antar_kedatangan

        # Kolom 4: Waktu pelayanan
        waktu_pelayanan = daftar_pelayanan[i]

        # Kolom 5: Waktu mulai dilayani
        if i == 0:
            waktu_mulai = waktu_kedatangan_kumulatif
        else:
            x = rows[i - 1][2]  # Waktu pelayanan dari baris sebelumnya
            y = rows[i - 1][3]  # Waktu mulai dilayani dari baris sebelumnya
            z = x + y           # Jumlahkan waktu pelayanan dan waktu mulai
            waktu_mulai = max(waktu_kedatangan_kumulatif, z)

        # Kolom 6: Waktu selesai dilayani
        waktu_selesai = waktu_mulai + waktu_pelayanan

        # Kolom 7: Waktu menunggu
        waktu_tunggu = waktu_mulai - waktu_kedatangan_kumulatif

        # Kolom 8: Waktu dalam sistem
        waktu_sistem = waktu_selesai - waktu_kedatangan_kumulatif

        # Kolom 9: Waktu teller menganggur
        waktu_menganggur = max(0, waktu_kedatangan_kumulatif - waktu_selesai_sebelumnya)

        # Simpan data ke dalam rows
        rows.append([
            nomor,
            waktu_antar_kedatangan,
            waktu_kedatangan_kumulatif,
            waktu_pelayanan,
            waktu_mulai,
            waktu_selesai,
            waktu_tunggu,
            waktu_sistem,
            waktu_menganggur
        ])


    return rows