import json
import csv
import random
import os

def generate_database():
    # 1. Pastikan cities.json ada di folder yang sama
    if not os.path.exists('cities.json'):
        print("❌ Error: File cities.json TIDAK DITEMUKAN!")
        return

    with open('cities.json', 'r', encoding='utf-8') as f:
        cities_data = json.load(f)

    # PERBAIKAN FOTO: Menggunakan nama file lokal agar sinkron dengan template.html
    # Pastikan file preview-payslip.jpg ada di folder utama Anda
    payslip_img = "preview-payslip.jpg"

    # 2. Database 100 Profesi Unik Khusus Payslip
    professions_pool = [
        {"name": "Karyawan Swasta", "cat": "Karyawan", "pain": "sulit ajukan KPR karena slip gaji tidak standar", "loss": "impian memiliki rumah sendiri terhambat"},
        {"name": "Staff Gudang", "cat": "Karyawan", "pain": "perhitungan lembur yang sering selisih", "loss": "kehilangan hak pendapatan yang seharusnya diterima"},
        {"name": "MUA Profesional", "cat": "Freelance", "pain": "dianggap pengangguran oleh bank saat mau cicil mobil", "loss": "mobilitas bisnis terganggu karena tidak punya kendaraan"},
        {"name": "Driver Logistik", "cat": "Logistik", "pain": "uang jalan dan gaji pokok tercampur berantakan", "loss": "kesulitan mengatur ekonomi keluarga bulanan"},
        {"name": "Guru Les Privat", "cat": "Pendidikan", "pain": "tidak punya bukti penghasilan untuk urusan administrasi", "loss": "kehilangan peluang akses pinjaman modal usaha"},
        {"name": "Admin Toko Online", "cat": "Digital", "pain": "format slip gaji masih pakai tulis tangan yang tidak profesional", "loss": "kredibilitas bisnis di mata karyawan menurun"},
        {"name": "Arsitek Freelance", "cat": "Kreatif", "pain": "sulit verifikasi penghasilan untuk pembuatan Visa", "loss": "rencana riset atau perjalanan luar negeri batal"},
        {"name": "Montir Bengkel", "cat": "Teknis", "pain": "sistem bagi hasil yang tidak tercatat transparan", "loss": "potensi konflik dengan pemilik bengkel"},
        {"name": "Content Creator", "cat": "Digital", "pain": "bukti transfer tidak cukup kuat sebagai dokumen legal", "loss": "terkendala saat melakukan kontrak sewa properti"},
        {"name": "Barista", "cat": "F&B", "pain": "rekap slip gaji sering hilang dan sulit diminta ulang ke HR", "loss": "sulit memenuhi syarat administrasi perbankan"},
    ]

    # Mengisi otomatis hingga 100 profesi unik agar data entry bervariasi
    while len(professions_pool) < 100:
        i = len(professions_pool)
        professions_pool.append({
            "name": f"Tenaga Kerja {i}",
            "cat": "Umum",
            "pain": "sulit memiliki dokumentasi gaji yang rapi dan sah",
            "loss": "terhambatnya berbagai urusan verifikasi keuangan pribadi"
        })

    # 3. LOGIKA ATOMIC SPINNING (Ribuan Kombinasi Judul & Header)
    prefix_titles = ["Cara Buat", "Template", "Aplikasi", "Download", "Contoh", "Format", "Solusi", "Jasa", "Panduan", "Generator"]
    middle_titles = ["Slip Gaji", "Payslip", "Bukti Penghasilan", "Daftar Gaji", "Slip Upah"]
    suffix_titles = ["Otomatis", "Legal & Sah", "Terbaik 2026", "Gratis", "Siap Cetak", "Profesional", "Instan", "Versi A4", "Tanpa Ribet", "Mudah"]

    prefix_h1 = ["Kelola", "Atasi Masalah", "Sistem", "Buat", "Optimalkan", "Solusi Mudah untuk", "Transformasi", "Mulai Gunakan", "Rapikan", "Automasi"]
    suffix_h1 = ["Sekarang Juga", "di Wilayah Anda", "Secara Digital", "dengan Cepat", "Tanpa Error", "Paling Praktis", "Terpercaya", "Modern", "Edisi Premium", "Hanya 5 Menit"]

    # 4. Menghasilkan database_pseo.csv
    with open('database_pseo.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Nama kolom product_image harus sinkron dengan {{product_image}} di template
        writer.writerow(['city', 'city_slug', 'profession', 'prof_slug', 'category', 'pain_point', 'business_loss', 'product_image', 'title_page', 'h1_header'])
        
        for _ in range(1000):
            c = random.choice(cities_data)
            p = random.choice(professions_pool)
            p_slug = p['name'].lower().replace(" ", "-").replace("/", "-").replace("(", "").replace(")", "")

            # Kombinasi Judul Variatif
            title_parts = [random.choice(prefix_titles), random.choice(middle_titles), p['name'], "di", c['city'], random.choice(suffix_titles)]
            generated_title = " ".join(title_parts)

            # Kombinasi Header Variatif
            h1_parts = [random.choice(prefix_h1), p['name'], "di", c['city'], random.choice(suffix_h1)]
            generated_h1 = " ".join(h1_parts)
            
            writer.writerow([
                c['city'], 
                c['slug'], 
                p['name'], 
                p_slug, 
                p['cat'], 
                p['pain'], 
                p['loss'], 
                payslip_img, # Isi kolom product_image
                generated_title,
                generated_h1
            ])

    print(f"✨ Sukses! 1000 baris data dengan nama foto '{payslip_img}' telah dibuat di database_pseo.csv")

if __name__ == "__main__":
    generate_database()