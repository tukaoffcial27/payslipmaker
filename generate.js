const fs = require('fs');
const path = require('path');

const cities = JSON.parse(fs.readFileSync('cities.json', 'utf8'));
const template = fs.readFileSync('template.html', 'utf8');

const publicDir = path.join(__dirname, 'public');
const serviceDir = path.join(publicDir, 'layanan'); 

if (!fs.existsSync(serviceDir)) {
    fs.mkdirSync(serviceDir, { recursive: true });
}

// 1. DAFTAR FILE PENDUKUNG
const filesToCopy = [
    'index.html', 
    'robots.txt',
    'vercel.json',
    'preview-payslip.jpg',
    'preview-payslip1.jpg',
    'preview-payslip2.jpg'
];

filesToCopy.forEach(file => {
    if (fs.existsSync(file)) {
        fs.copyFileSync(file, path.join(publicDir, file));
    }
});

// 2. GENERATE HALAMAN KOTA & SITEMAP
let sitemapEntries = '';
const baseUrl = 'https://payslipmaker.guidify.app';

cities.forEach((data) => {
    let content = template.replace(/{{city}}/g, data.city);
    fs.writeFileSync(path.join(serviceDir, `${data.slug}.html`), content);
    sitemapEntries += `  <url>\n    <loc>${baseUrl}/layanan/${data.slug}</loc>\n    <priority>0.8</priority>\n  </url>\n`;
});

const fullSitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>${baseUrl}/</loc><priority>1.0</priority></url>
${sitemapEntries}
</urlset>`;

fs.writeFileSync(path.join(publicDir, 'sitemap.xml'), fullSitemap);
console.log(`✨ Sukses! 465 Halaman Payslip Maker Pro siap tanpa kebocoran.`);