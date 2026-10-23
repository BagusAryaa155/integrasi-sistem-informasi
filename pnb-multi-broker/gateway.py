import pika
from kafka import KafkaProducer
import json
import time

try:
    rabbit_conn = pika.BlockingConnection(
        pika.ConnectionParameters('localhost')
    )
    rabbit_ch = rabbit_conn.channel()
    rabbit_ch.queue_declare(queue='antrean-notifikasi')

    kafka_prod = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    print("[INFO] Sukses terhubung ke broker RabbitMQ & Kafka di subsistem WSL 2.")
except Exception as e:
    print(f"[EROR] Koneksi gagal. Pastikan Docker Desktop & WSL Integration aktif. Detail: {e}")
    exit(1)

print("=============================================")
print("  GERBANG TRANSAKSI DINAMIS MULTI-BROKER PNB ")
print("  Ketik 'exit' pada nama customer untuk keluar ")
print("=============================================")

while True:
    try:
        print("--- Entri Transaksi Baru ---")
        customer_name = input("Masukkan Nama Customer: ").strip()

        if customer_name.lower() == 'exit':
            print("[INFO] Menutup koneksi gateway. Keluar...")
            break

        if not customer_name:
            print("[PENGINGAT] Nama tidak boleh kosong!")
            continue

        nominal_input = input("Masukkan Nominal Transaksi (Rp): ").strip()
        if not nominal_input.isdigit():
            print("[EROR] Nominal harus berupa angka bulat valid!")
            continue

        nominal_val = int(nominal_input)

        payload_transaksi = {
            "id_transaksi": f"TX-PNB-2026-DYN-{int(time.time())}",
            "customer": customer_name,
            "nominal": nominal_val,
            "timestamp": time.time()
        }

        rabbit_ch.basic_publish(
            exchange='',
            routing_key='antrean-notifikasi',
            body=json.dumps(payload_transaksi)
        )
        print(" [✓] Jalur A: Data terkirim ke antrean RabbitMQ.")

        kafka_prod.send('stream-log-audit', value=payload_transaksi)
        kafka_prod.flush()
        print(" [✓] Jalur B: Log digital dialirkan ke topik Kafka.")

    except KeyboardInterrupt:
        print("\n[INFO] Menghentikan program gateway...")
        break

rabbit_conn.close()
