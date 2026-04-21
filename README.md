# :musical_score: PENGANALISIS GELOMBANG

> *"Di dalam setiap alun gelombang suara, tersembunyi lukisan yang menanti untuk dizahirkan; di dalam setiap detik masa, harmoni yang merindukan kanvasnya."*
> — **misyaz-pelitari**

---

## :seedling: Pengenalan

**Penganalisis-Gelombang** adalah sebuah naskhah Python yang indah, yang terhasil daripada pertemuan antara keelokanseni bunyi dan ketepatan sains. Naskhah ini berupaya menterjemahkan setiap fail audio (WAV, MP3, FLAC, OGG, dan lain-lain) ke dalam pelbagai bentuk lukisan visual yang memukau mata dan menyentuh jiwa.

Melaluinya, anda boleh melihat:
- **Bentuk Gelombang** — :water_wave: anak-anak yang naik turun sepanjang garisan masa
- **Spektrogram** — :artist_palette: warna-warni yang bercerita tentang frekuensi sepanjang detik
- **Fitur-Fitur Canggih** — khazanah berharga yang dihimpun dari pelbagai sumber:
  - MFCC (cap jari akustik yang unik)
  - Kromagram (12 nada kromatik dalam harmoni)
  - Sentroid Spektrum (kecerahan suara)
  - Lebar Jalur & Rolloff Spektrum
  - Kadar Lintas Sifar (ZCR)
  - Pembahagian Harmonik-Perkusif (HPSS)
- **Analisis Lanjutan** — pengesanan onset, penjejakan rentak, tempogram, kontras spektrum, dan Tonnetz
- **Visual 3D Interaktif** — pandangan tiga dimensi yang boleh diputar, dizum, dan digerakkan

---

## :sparkles: Keistimewaan

| Ciri | Huraian |
|------|---------|
| :globe_with_meridians: **Pengesanan Automatik** | Mengenal pasti platform dengan sendiri (Termux/Android/Windows/Linux) |
| :artist_palette: **Terminal yang Cantik (Rich)** | Menggunakan library Rich untuk output terminal yang berwarna-warni dan tersusun |
| :bar_chart: **Visualisasi 3D Interaktif** | Menggunakan Plotly untuk pandangan tiga dimensi yang boleh diputar, dizum, dan digerakkan |
| :repeat_button: **Fitur Delta** | MFCC beserta Delta (terbitan pertama) dan Delta-Delta (terbitan kedua) |
| :artist_palette: **Palet Warna Istimewa** | Warnawarni yang direka khas untuk pengalaman visual yang memikat |
| :rocket: **Fitur Terkini** | RMS, Spectral Flatness, Chroma CQT/CENS, Poly Features |
| :file_folder: **Simpanan Automatik** | Semua hasil analisis disimpan dengan kemas dalam folder pilihan |
| :desktop_computer: **Antara Muka Baris Perintah** | Penggunaan yang mudah, sama ada untuk analisis penuh atau pilihan tertentu sahaja |
| :bar_chart: **Ringkasan Teks** | Menghasilkan fail ringkasan yang mengandungi statistik penting audio |
| :wrench: **Virtual Environment** | Menyediakan fungsi untuk cipta persekitaran virtual secara automatik |
| :clipboard: **Menu Interaktif** | Menu berwarna-warni dengan panduan lengkap |
| :hourglass_flowing_sand: **Progress Bars** | Paparan kemajuan analisis yang jelas dan menarik |
| :grinning: **Emoji Library** | Penggunaan emoji yang elegan dan konsisten dalam antara muka |

---

## :package: Keperluan Asas

Pastikan Python 3.7 atau versi yang lebih baharu telah terpasang di peranti anda.

### :wrench: Pasang Pustaka

Pasang semua pustaka yang diperlukan dengan satu perintah:

```bash
pip install -r requirements_windows.txt   # Untuk Windows
pip install -r requirements_linux.txt     # Untuk Linux
pip install -r requirements_termux.txt    # Untuk Termux/Android
```

Atau gunakan fungsi setup dalam skrip:

```bash
python penganalisis-gelombang.py --setup-venv
```

### :clapper: Menjalankan Analisis

Setelah persekitaran sedia, jalankan analisis:

```bash
# Menu Interaktif ( cara paling mudah)
python penganalisis-gelombang.py --menu

# Analisis penuh (semua visualisasi)
python penganalisis-gelombang.py audio.wav --penuh

# Hanya bentuk gelombang
python penganalisis-gelombang.py audio.wav --bentuk-gelombang

# Spektrogram jenis Mel sahaja
python penganalisis-gelombang.py audio.wav --spektrogram mel

# Fitur canggih sahaja
python penganalisis-gelombang.py audio.wav --fitur

# Visual 3D interaktif
python penganalisis-gelombang.py audio.wav --visual3d

# Fitur Delta MFCC
python penganalisis-gelombang.py audio.wav --delta

# Fitur terkini (RMS, Spectral Flatness, dll)
python penganalisis-gelombang.py audio.wav --canggih

# Analisis lanjutan (onset, rentak, harmoni)
python penganalisis-gelombang.py audio.wav --lanjutan

# Folder output sendiri
python penganalisis-gelombang.py audio.wav --penuh -o hasil_analisis_saya/

# Gabungan pelbagai pilihan
python penganalisis-gelombang.py audio.wav --bentuk-gelombang --spektrogram mel --visual3d -o output/
```

---

## :satellite: Pilihan Platform

Skrip ini mengesan platform secara automatik:
- **Termux/Android** — Diserasikan untuk peranti Android dan iOS
- **Windows** — Dioptimumkan untuk Windows
- **Linux** — Sokongan penuh untuk Linux

---

## :clipboard: Hasil Keputusan

Selepas analisis tamat, anda akan menjumpai fail-fail berikut dalam folder output:

```
hasil_analisis/
├── nama_fail_bentuk_gelombang.png
├── nama_fail_spektrogram_mel.png
├── nama_fail_spektrogram_linear.png
├── nama_fail_spektrogram_log.png
├── nama_fail_fitur_canggih.png
├── nama_fail_analisis_lanjutan.png
├── nama_fail_delta.png
├── nama_fail_fitur_terkini.png
├── nama_fail_3d.png
└── nama_fail_ringkasan.txt
```

---

## :brain: Khazanah yang Diteroka

Naskhah ini menghimpunkan ilmu dari pelbagai sumber terkemuka di GitHub:

| Sumber | Fitur yang Diambil |
|--------|------------------|
| BlexBOTTT/Audio-Feat-Extraction | MFCC, Sentroid Spektrum |
| raj07a/Music-Analysis-and-Visualization-with-Librosa | Mel-spektrogram, Kromagram, HPSS |
| lyasantoscode/Exploring-Audio-with-3D-Visualization-in-Python | Analisis spektrum 2D, fitur sentroid |
| tyiannak/pyAudioAnalysis | Konsep pengekstrakan fitur menyeluruh |
| DavidHospinal/bioacoustic-perception | Visualisasi 3D, RMS, Spectral Flatness |
| librosa/librosa | Delta features, Chroma CQT/CENS, Poly Features |

---

## :scroll: Lesen

Projek ini dilesenkan di bawah Lesen MIT — bebas untuk digunakan, diubah suai, dan diedarkan dengan penuh hormat.

---

## :folded_hands: Penghargaan

- **Librosa** — pustaka utama yang menjadi tulang belakang analisis audio
- **Matplotlib & Seaborn** — untuk visualisasi yang memukau
- **Plotly** — untuk keajaiban visualisasi 3D interaktif
- **Rich** — untuk terminal yang cantik dan berwarna-warni
- **Emoji** — untuk keelegenan antara muka pengguna
- **Komuniti GitHub** — atas ilham dan perkongsian ilmu yang tidak ternilai

---

> *"Di dalam setiap gelombang suara, tersembunyi rahsia alam yang hanya dapat disingkap oleh mata yang terlatih. Biarlah naskhah ini menjadi cermin yang memantulkan keindahan itu kepada dunia."*

**misyaz-pelitari**
*Penulis & Penjaga Projek*