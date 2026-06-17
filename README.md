# FastAPI Task Management API (CI/CD Demo)

Proyek ini adalah API sederhana untuk manajemen tugas (*Task Management*) yang dibangun dengan **FastAPI** dan **SQLAlchemy** (SQLite). Proyek ini dirancang secara khusus untuk mendemonstrasikan konsep **Continuous Integration (CI)** dan **Continuous Deployment/Delivery (CD)** dengan standar industri modern.

---

## 🚀 Fitur Utama

- **RESTful API**: CRUD untuk entitas `Task` dengan validasi data yang ketat menggunakan Pydantic.
- **Continuous Testing**: Uji otomatis terisolasi menggunakan `pytest`, `TestClient` FastAPI, dan database SQLite in-memory.
- **Continuous Inspection**: Analisis kualitas dan keamanan kode menggunakan Ruff, Mypy, dan Bandit.
- **Continuous Deployment/Delivery**: Konfigurasi build Docker multi-stage dan workflow integrasi otomatis GitHub Actions.

---

## 🛠️ Konsep CI/CD yang Diimplementasikan

### 1. Continuous Testing (Pengujian Berkelanjutan)
- **Framework**: `pytest`
- **Cakupan Kode**: `pytest-cov` untuk mengukur cakupan testing. Ambang batas kegagalan diatur minimal **80%**.
- **Isolasi Database**: Menggunakan database SQLite `:memory:` saat tes berlangsung (dikonfigurasi pada `tests/conftest.py`) agar pengujian tidak memengaruhi database utama.

### 2. Continuous Inspection (Inspeksi Berkelanjutan)
Kualitas kode dijaga secara ketat melalui:
- **Linting & Formatting**: `ruff` digunakan untuk memformat kode secara otomatis dan menemukan pelanggaran gaya pemrograman (linting) berdasarkan aturan PEP 8.
- **Static Typing**: `mypy` dengan mode ketat (`disallow_untyped_defs = true`) memastikan seluruh fungsi memiliki penandaan tipe data yang jelas dan bebas bug tipe data.
- **Security Check**: `bandit` memindai kode secara statis untuk mendeteksi celah keamanan umum pada Python.

### 3. Continuous Deployment/Delivery (Pengiriman/Penyebaran Berkelanjutan)
- **Containerization**: `Dockerfile` menggunakan teknik *multi-stage build* untuk memisahkan kompilasi dependensi (builder stage) dengan gambar rilis akhir yang ringan (runner stage).
- **Automation Pipeline**: `.github/workflows/ci-cd.yml` otomatis berjalan saat Anda melakukan `push` atau `pull request` ke cabang `main` atau `master`.

---

## 💻 Panduan Instalasi Lokal

### Prasyarat
- Python 3.10 ke atas
- Docker & Docker Compose (Opsional, untuk pengujian kontainer)

### Langkah Setup

1. **Clone Repositori**:
   ```bash
   git clone <url-repositori-anda>
   cd Tubes
   ```

2. **Buat Virtual Environment**:
   ```bash
   python -m venv .venv
   ```

3. **Aktifkan Virtual Environment**:
   - **Windows (PowerShell)**:
     ```powershell
     .venv\Scripts\Activate.ps1
     ```
   - **Linux / macOS**:
     ```bash
     source .venv/bin/activate
     ```

4. **Instal Dependensi**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Jalankan Aplikasi secara Lokal**:
   ```bash
   uvicorn app.main:app --reload
   ```
   Aplikasi akan berjalan di `http://127.0.0.1:8000`. Buka `http://127.0.0.1:8000/docs` untuk mengakses dokumentasi interaktif Swagger UI.

---

## 🧪 Menjalankan Pengujian dan Inspeksi Mandiri

Sebelum melakukan *push* kode ke repositori, jalankan perintah berikut secara lokal untuk memastikan pipeline CI tidak gagal:

### 1. Jalankan Analisis Kualitas Kode (Inspection)
```bash
# Cek format kode
ruff format --check .

# Format ulang kode secara otomatis jika ada ketidaksesuaian
ruff format .

# Jalankan linter
ruff check .

# Jalankan pengecekan tipe data static
mypy app

# Jalankan audit keamanan
bandit -r app
```

### 2. Jalankan Pengujian (Testing & Coverage)
```bash
pytest
```
*Catatan: Konfigurasi pytest di `pyproject.toml` otomatis mencakup pelaporan cakupan tes ke layar terminal dan pembuatan file `coverage.xml`.*

---

## 🐳 Menggunakan Docker Lokal

Anda dapat membangun dan menjalankan seluruh stack API ini dalam kontainer terisolasi:

1. **Jalankan Container**:
   ```bash
   docker compose up --build
   ```
2. **Hentikan Container**:
   ```bash
   docker compose down
   ```

---

## 🔧 Penjelasan Pipeline GitHub Actions (`ci-cd.yml`)

Pipeline didefinisikan dalam tiga tahap (*jobs*):
1. **`inspect`**: Menginstal python, menginstal dependensi, kemudian menjalankan `ruff`, `mypy`, dan `bandit`. Jika salah satu gagal, pipeline berhenti.
2. **`test`**: Berjalan setelah tahap inspeksi lulus. Menjalankan seluruh pengujian pytest dan memastikan coverage keseluruhan minimal 80%.
3. **`deploy`**: Berjalan setelah tes sukses. Melakukan kompilasi Docker image locally untuk memastikan tidak ada kesalahan dalam build configuration.
   - *Tip CD*: Di dalam file `.github/workflows/ci-cd.yml`, terdapat contoh baris yang di-komentar untuk mengirimkan (push) Docker image ke Docker Hub atau men-trigger deploy webhook Render/Railway. Anda cukup mengaktifkan baris tersebut dan menyeting GitHub repository secrets.
