import requests
import json
import time
import random
from threading import Thread

class Warna:
    HIJAU = '\033[92m'
    KUNING = '\033[93m'
    MERAH = '\033[91m'
    RESET = '\033[0m'

def ambil_pesan_dari_file():
    try:
        with open("chat.txt", "r") as file:
            pesan = [line.strip() for line in file if line.strip()]
            return pesan
    except FileNotFoundError:
        print(f"{Warna.MERAH}File chat.txt tidak ditemukan!{Warna.RESET}")
        return []

def hapus_pesan(channel_id, message_id, otorisasi, isi_pesan):
    header = {
        "Authorization": otorisasi,
        "Content-Type": "application/json",
    }
    time.sleep(waktu_hapus)  # Tunggu waktu sebelum menghapus pesan
    try:
        res = requests.delete(f"https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}", headers=header)
        if res.status_code == 204:
            print(f"{Warna.MERAH}Pesan: {Warna.KUNING}'{isi_pesan}'{Warna.MERAH} berhasil dihapus!{Warna.RESET}")
        else:
            print(f"{Warna.MERAH}Gagal menghapus pesan {Warna.KUNING}{message_id}{Warna.MERAH}. Status: {res.status_code}{Warna.RESET}")
    except Exception as e:
        print(f"{Warna.MERAH}Kesalahan saat menghapus pesan {Warna.KUNING}{message_id}{Warna.MERAH}: {e}{Warna.RESET}")

def kirim_pesan(channel_id, pesan, otorisasi, hapus_otomatis):
    header = {
        "Authorization": otorisasi,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, seperti Gecko) Chrome/94.0.4606.61 Safari/537.36",
    }
    msg = {
        "content": pesan,
        "nonce": "82329451214{}33232234".format(random.randrange(0, 1000)),
        "tts": False,
    }
    discord_url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
    try:
        res = requests.post(url=discord_url, headers=header, data=json.dumps(msg))
        if res.status_code == 200:
            message_id = res.json()["id"]
            print(f"{Warna.HIJAU}Pesan: {Warna.KUNING}'{pesan}'{Warna.HIJAU} berhasil dikirim!{Warna.RESET}")
            if hapus_otomatis:
                Thread(target=hapus_pesan, args=(channel_id, message_id, otorisasi, pesan)).start()
        else:
            print(f"{Warna.MERAH}Periksa kembali token {otorisasi[:10]}... (Status: {res.status_code}){Warna.RESET}")
    except Exception as e:
        print(f"{Warna.MERAH}Kesalahan dengan token {otorisasi[:10]}...: {e}{Warna.RESET}")

if __name__ == "__main__":
    channel = ["1260240731726151721"]  # ID Channel Discord
    pesan = ambil_pesan_dari_file()
    if not pesan:
        exit()

    try:
        with open("token.txt", "r") as file:
            token = [line.strip() for line in file.readlines() if line.strip()]
        
        delay_pesan = input("Jeda waktu antar pesan (default 25-30 detik): ").strip()
        delay_pesan = random.randint(25, 30) if not delay_pesan.isdigit() else int(delay_pesan)

        hapus_otomatis = input("Apakah Anda ingin menghapus pesan secara otomatis? (ya/tidak): ").strip().lower() == "ya"
        global waktu_hapus
        waktu_hapus = 10
        if hapus_otomatis:
            waktu_hapus_input = input("Berapa lama pesan harus dihapus? (default 10 detik): ").strip()
            waktu_hapus = 10 if not waktu_hapus_input.isdigit() else int(waktu_hapus_input)

        while True:
            try:
                for token_satu in token:
                    for pesan_satu in pesan:
                        for channel_id in channel:
                            kirim_pesan(channel_id, pesan_satu, token_satu, hapus_otomatis)
                        time.sleep(delay_pesan)
            except KeyboardInterrupt:
                print(f"{Warna.MERAH}\nPengiriman pesan dihentikan!{Warna.RESET}")
                break
    except FileNotFoundError:
        print(f"{Warna.MERAH}File token.txt tidak ditemukan. Silakan buat file dan tambahkan token Discord Anda.{Warna.RESET}")