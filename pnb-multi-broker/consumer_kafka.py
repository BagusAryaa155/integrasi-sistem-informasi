from kafka import KafkaConsumer
import json
import csv
import os

CSV_FILE = "arsip_audit.csv"

if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["ID_Transaksi", "Customer", "Nominal", "Timestamp"])

consumer = KafkaConsumer(
    'stream-log-audit',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print(f' [*] KONSUMEN KAFKA: Menunggu aliran log audit... (Menyimpan ke {CSV_FILE})')

for message in consumer:
    log = message.value
    print(f" [AUDIT DATA] Memproses riwayat transaksi {log['id_transaksi']}...")
    
    with open(CSV_FILE, mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([log['id_transaksi'], log['customer'], log['nominal'], log['timestamp']])
    print(f"   [✓] Sukses diarsip secara permanen ke {CSV_FILE}")