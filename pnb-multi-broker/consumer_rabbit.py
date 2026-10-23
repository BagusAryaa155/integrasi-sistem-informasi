import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='antrean-notifikasi')

TXT_FILE = "notifikasi_terkirim.txt"
print(f' [*] KONSUMEN RABBITMQ: Menunggu tugas masuk... (Menyimpan ke {TXT_FILE})')

def callback(ch, method, properties, body):
    data = json.loads(body)
    log_line = f"[NOTIFIKASI] Kirim konfirmasi ke {data['customer']} | Nominal: Rp {data['nominal']}"
    print(f" [PROSES] {log_line.strip()}")
    
    with open(TXT_FILE, "a") as f:
        f.write(log_line)

channel.basic_consume(queue='antrean-notifikasi', on_message_callback=callback, auto_ack=True)
channel.start_consuming()