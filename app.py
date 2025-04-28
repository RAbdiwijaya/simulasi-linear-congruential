from flask import Flask, render_template, request, make_response
from static.python.simulasi import simulasi_antrian
import pandas as pd
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def index():
    # Kirim stats kosong ke template
    stats = {
        "jumlah_nasabah": 0,
        "jumlah_antar_kedatangan": 0,
        "jumlah_pelayanan": 0,
        "jumlah_waktu_tunggu": 0,
        "jumlah_waktu_dalam_sistem": 0,
        "jumlah_idle_time_teller": 0,
        "waktu_selesai_terakhir": 0,
        "rata_waktu_tunggu": 0,
        "peluang_nasabah_menunggu": 0,
        "rata_waktu_pelayanan": 0,
        "rata_waktu_dalam_sistem": 0,
        "persentase_teller_menganggur": 0,
        "rata_waktu_antar_kedatangan": 0,
    }
    return render_template('index.html', rows=[], stats=stats, error=None)

@app.route('/submit_all', methods=['POST'])
def submit_all():
    try:
        # Ambil input dari form
        nasabah = int(request.form.get('nasabah'))
        max_kedatangan = int(request.form.get('max_kedatangan'))
        max_pelayanan = int(request.form.get('max_pelayanan'))

        # Validasi input
        if nasabah <= 0 or max_kedatangan <= 0 or max_pelayanan <= 0:
            raise ValueError("Semua input numerik harus lebih besar dari 0.")

        # Panggil fungsi simulasi
        rows = simulasi_antrian(nasabah, max_kedatangan, max_pelayanan)

        # Hitung statistik
        jumlah_nasabah = len(rows)
        jumlah_antar_kedatangan = sum(row[1] for row in rows)
        jumlah_pelayanan = sum(row[3] for row in rows)
        jumlah_waktu_tunggu = sum(row[6] for row in rows)
        jumlah_waktu_dalam_sistem = sum(row[7] for row in rows)
        jumlah_idle_time_teller = sum(row[8] for row in rows)
        waktu_selesai_terakhir = max(row[5] for row in rows)
        rata_waktu_tunggu = jumlah_waktu_tunggu / jumlah_nasabah
        peluang_nasabah_menunggu = (max(row[7] for row in rows) / jumlah_nasabah) * 100
        rata_waktu_pelayanan = jumlah_pelayanan / jumlah_nasabah
        rata_waktu_dalam_sistem = jumlah_waktu_dalam_sistem / jumlah_nasabah
        persentase_teller_menganggur = (jumlah_waktu_tunggu / waktu_selesai_terakhir) * 100
        rata_waktu_antar_kedatangan = jumlah_antar_kedatangan / jumlah_nasabah

        if peluang_nasabah_menunggu > 100:
            keterangan = "Belum Bagus"
            keterangan_tingkat = "Tinggi"
        else:
            keterangan = "Bagus"
            keterangan_tingkat = "Rendah"

        # Kirim data ke template
        stats = {
            "jumlah_nasabah": jumlah_nasabah,
            "jumlah_antar_kedatangan": jumlah_antar_kedatangan,
            "jumlah_pelayanan": jumlah_pelayanan,
            "jumlah_waktu_tunggu": jumlah_waktu_tunggu,
            "jumlah_waktu_dalam_sistem": jumlah_waktu_dalam_sistem,
            "jumlah_idle_time_teller": jumlah_idle_time_teller,
            "waktu_selesai_terakhir": waktu_selesai_terakhir,
            "rata_waktu_tunggu": rata_waktu_tunggu,
            "peluang_nasabah_menunggu": peluang_nasabah_menunggu,
            "rata_waktu_pelayanan": rata_waktu_pelayanan,
            "rata_waktu_dalam_sistem": rata_waktu_dalam_sistem,
            "persentase_teller_menganggur": persentase_teller_menganggur,
            "rata_waktu_antar_kedatangan": rata_waktu_antar_kedatangan,
            "keterangan": keterangan,
            "keterangan_tingkat": keterangan_tingkat,
        }

        return render_template('index.html', rows=rows, stats=stats, error=None)
    except ValueError as e:
        return render_template('index.html', rows=[], stats={}, error=str(e))

@app.route('/save_to_excel', methods=['POST'])
def save_to_excel():
    try:
        # Ambil data dari form
        rows_data = request.form.get('rows_data')
        rows = eval(rows_data)  # Konversi string JSON ke list
        
        # Buat DataFrame
        df = pd.DataFrame(rows, columns=[
            "Nasabah",
            "Waktu Antar Kedatangan",
            "Waktu Kedatangan",
            "Waktu Pelayanan",
            "Waktu Mulai",
            "Waktu Selesai",
            "Waktu Menunggu",
            "Waktu Sistem",
            "Teller Menganggur"
        ])
        
        # Simpan ke Excel dalam memory
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        df.to_excel(writer, index=False, sheet_name='Simulasi')
        writer.close()
        output.seek(0)
        
        # Buat response file
        response = make_response(output.getvalue())
        response.headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response.headers['Content-Disposition'] = 'attachment; filename=simulasi_antrian.xlsx'
        return response
        
    except Exception as e:
        return str(e), 400

if __name__ == '__main__':
    app.run(debug=True)