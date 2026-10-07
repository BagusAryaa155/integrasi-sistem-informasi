# Jawaban Tugas Analisis Jobsheet 3

## 1. Analisis Pola Arsitektur

Rancangan pada praktikum ini termasuk **Adapter Pattern** dalam arsitektur **Enterprise Application Integration (EAI)** karena terdapat sebuah komponen perantara, yaitu `adapter_service.py`, yang menghubungkan sistem modern dengan sistem legacy. Sistem legacy menggunakan program C dan file `students_db.txt` sebagai tempat penyimpanan data, sedangkan sistem dari luar berkomunikasi melalui HTTP dan XML. Adapter menerjemahkan permintaan HTTP/XML menjadi operasi terhadap file teks legacy, sehingga kode pada sistem legacy tidak perlu diubah.

Keuntungan bagi klien web luar adalah klien tidak perlu mengetahui bagaimana sistem legacy bekerja atau bagaimana data disimpan. Klien cukup mengakses endpoint yang disediakan adapter, seperti `GET /students`, `GET /students/{nim}`, dan `POST /students`. Dengan demikian, komunikasi menjadi lebih sederhana dan kedua sistem tidak terlalu bergantung satu sama lain.

## 2. Analisis Overhead Serialisasi Data

Data aktual pada mahasiswa dengan NIM `2415354001` adalah:

- `2415354001` = 10 byte
- `I Made Sujana` = 13 byte
- `Teknologi Informasi` = 19 byte
- `ACTIVE` = 6 byte

Total data aktual:

**10 + 13 + 19 + 6 = 48 byte**

Response XML hasil pengujian `GET /students/2415354001` adalah:

```xml
<?xml version='1.0' encoding='utf-8'?><StudentResponse><NIM>2415354001</NIM><Nama>I Made Sujana</Nama><Jurusan>Teknologi Informasi</Jurusan><Status>ACTIVE</Status></StudentResponse>
```

Ukuran seluruh response XML tersebut adalah **181 byte** jika dihitung dalam UTF-8.

Maka overhead XML:

**Overhead = Total XML - Data Aktual**

**Overhead = 181 - 48 = 133 byte**

Persentase overhead:

**Overhead (%) = (133 / 48) × 100% = 277,08%**

Jadi, data aktual hanya berukuran **48 byte**, sedangkan seluruh response XML berukuran **181 byte**. Terdapat tambahan **133 byte** atau sekitar **277,08%** dibandingkan ukuran data aktual. Besarnya overhead berasal dari XML declaration, tag pembuka dan penutup, serta struktur pembungkus data.

## 3. Prediksi Keterbatasan Integrasi

Jika 500 permintaan `POST` datang secara bersamaan pada detik yang sama, adapter akan menerima banyak operasi penulisan ke file `students_db.txt`. Karena penyimpanan masih menggunakan file teks dan setiap request langsung melakukan penulisan, dapat terjadi persaingan akses (*race condition*), antrean operasi I/O, dan risiko data menjadi tidak konsisten atau proses penulisan gagal.

Kondisi tersebut menunjukkan keterbatasan penggunaan file teks sebagai media penyimpanan ketika jumlah request semakin besar. Untuk mengatasinya, **Message Broker** dapat digunakan sebagai antrean antara adapter dan proses penulisan data. Request dari client dimasukkan terlebih dahulu ke dalam queue, kemudian diproses oleh worker secara terkontrol. Dengan cara ini, beban penulisan dapat diatur, request yang belum diproses tidak langsung berebut mengakses file, dan sistem menjadi lebih mudah dikembangkan ketika jumlah permintaan meningkat.
