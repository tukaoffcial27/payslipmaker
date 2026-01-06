import pandas as pd
import os
import shutil

# Konfigurasi
base_url = "https://payslip.guidify.app" 
output_dir = "public/layanan"

# 1. Reset folder public agar bersih
if os.path.exists('public'): 
    shutil.rmtree('public')
os.makedirs(output_dir, exist_ok=True)

# 2. Load Data & Template
if not os.path.exists('database_pseo.csv'):
    print("❌ Error: database_pseo.csv tidak ditemukan! Jalankan generate_database.py dulu.")
    exit()

df = pd.read_csv('database_pseo.csv')
with open('template.html', 'r', encoding='utf-8') as f:
    template_content = f.read()

sitemap_urls = []

print("🚀 Generating Pages & Sitemap...")

for index, row in df.iterrows():
    # Logika slug (prof_slug + city_slug) sesuai dengan api/index.py
    prof_slug = str(row['prof_slug']).replace("/", "-")
    slug = f"{prof_slug}-{row['city_slug']}"
    url = f"{base_url}/layanan/{slug}"
    sitemap_urls.append(url)
    
    # Generate 200 Halaman Statis Pertama (Fisik)
    if index < 200:
        content = template_content
        # Mengganti SEMUA variabel termasuk title_page, h1_header, dan product_image
        for col in df.columns:
            placeholder = f"{{{{{col}}}}}"
            content = content.replace(placeholder, str(row[col]))
        
        with open(f"{output_dir}/{slug}.html", "w", encoding='utf-8') as f:
            f.write(content)

# 3. Generate sitemap.xml (Berisi 1.000 URL)
sitemap_content = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for loc in sitemap_urls:
    sitemap_content += f'  <url><loc>{loc}</loc><priority>0.8</priority></url>\n'
sitemap_content += '</urlset>'

with open("public/sitemap.xml", "w", encoding='utf-8') as f:
    f.write(sitemap_content)

# 4. REVISI UTAMA: Otomasi Copy File Statis & Foto Produk
files_to_copy = [
    'index.html', 
    'robots.txt', 
    'preview-payslip.jpg', 
    'preview-payslip1.jpg', 
    'preview-payslip2.jpg'
]

for file_name in files_to_copy:
    if os.path.exists(file_name):
        shutil.copy(file_name, f"public/{file_name}")
        print(f"✅ Berhasil menyalin: {file_name}")
    else:
        print(f"⚠️ Peringatan: {file_name} tidak ditemukan di folder utama.")

print("✅ Sukses! 200 Halaman fisik, Sitemap, dan Foto Produk sudah siap di folder /public")