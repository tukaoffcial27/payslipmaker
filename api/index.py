from flask import Flask, render_template_string, send_from_directory
import pandas as pd
import os

app = Flask(__name__)

# Menentukan lokasi folder utama (root) secara absolut
# Karena index.py ada di dalam folder 'api', kita naik satu tingkat ke atas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_PATH = os.path.join(BASE_DIR, 'database_pseo.csv')
PUBLIC_DIR = os.path.join(BASE_DIR, 'public')
TEMPLATE_PATH = os.path.join(BASE_DIR, 'template.html')

# Memuat database
if os.path.exists(DATABASE_PATH):
    df = pd.read_csv(DATABASE_PATH)
else:
    df = None

# 1. ROUTE UNTUK FILE STATIS (Sitemap, Robots, Foto, dan Halaman Statis .html)
@app.route('/<path:filename>')
def serve_public_files(filename):
    # Cek apakah file ada di folder public
    if os.path.exists(os.path.join(PUBLIC_DIR, filename)):
        return send_from_directory(PUBLIC_DIR, filename)
    
    # Cek apakah file .html statis ada di folder public/layanan/
    # (Penting untuk 200 halaman pertama yang sudah di-generate)
    html_file = filename + ".html"
    if os.path.exists(os.path.join(PUBLIC_DIR, html_file)):
        return send_from_directory(PUBLIC_DIR, html_file)
    
    return "File tidak ditemukan.", 404

# 2. ROUTE HALAMAN UTAMA
@app.route('/')
def home():
    if os.path.exists(os.path.join(PUBLIC_DIR, 'index.html')):
        return send_from_directory(PUBLIC_DIR, 'index.html')
    return "Halaman utama tidak ditemukan.", 404

# 3. ROUTE HALAMAN DINAMIS (pSEO)
@app.route('/layanan/<slug>')
def serve_dynamic_page(slug):
    if df is None:
        return "Database tidak ditemukan.", 500
        
    if not os.path.exists(TEMPLATE_PATH):
        return "File template.html tidak ditemukan.", 404

    with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        template_content = f.read()

    match = None
    # Mencari data di CSV berdasarkan slug
    for _, row in df.iterrows():
        p_slug = str(row['prof_slug']).replace("/", "-")
        c_slug = str(row['city_slug'])
        if f"{p_slug}-{c_slug}" == slug:
            match = row
            break
    
    if match is not None:
        content = template_content
        # Mengganti semua placeholder {{kolom}} dengan data asli
        for col in df.columns:
            placeholder = f"{{{{{col}}}}}"
            content = content.replace(placeholder, str(match[col]))
        
        return render_template_string(content)
    
    return f"Halaman '{slug}' tidak terdaftar di database.", 404

if __name__ == "__main__":
    app.run(debug=True)