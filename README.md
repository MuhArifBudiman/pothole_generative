# Pothole Generative – Road Pothole Detection & Mapping System

## 📌 Overview

**Pothole Generative** adalah project end-to-end untuk mendeteksi lubang jalan (*pothole detection*) dari **video** menggunakan **YOLO**, kemudian menggabungkannya dengan data **GPS (GPX)** untuk divisualisasikan dalam bentuk **peta interaktif di Streamlit**.

Project ini dirancang dengan arsitektur **job-based asynchronous processing**, di mana proses berat (ekstraksi frame, GPS, dan inference) dijalankan sebagai *background job* di service backend, sementara Streamlit berperan sebagai frontend visualisasi.

---

## 🎯 Tujuan Project

* Mendeteksi lubang jalan dari video menggunakan YOLO
* Menghubungkan hasil deteksi dengan koordinat GPS
* Menyimpan hasil per *job* untuk ditampilkan kembali
* Memvisualisasikan hasil deteksi dalam bentuk **map + image preview** di Streamlit

---

## 🧠 High-Level Workflow

1. **Upload Data**

   * User meng-upload **video** dan **file GPX** melalui Streamlit
   * File disimpan di cloud / storage

2. **Create Job**

   * Streamlit memanggil API backend
   * Backend mengembalikan **Job ID / Ticket**

3. **Background Processing (Worker)**
   Worker menjalankan pipeline berikut:

   * Ekstraksi GPS dari GPX
   * Ekstraksi frame dari video
   * Sinkronisasi frame & GPS berdasarkan timestamp
   * Pembuatan metadata awal

4. **Inference Engine**

   * YOLO inference dijalankan secara **bulk** berdasarkan metadata
   * Model di-load dari **Hugging Face** (tidak membebani storage lokal)
   * Metadata hasil inference dibuat (lokasi image + hasil deteksi)

5. **Result Checking**

   * Streamlit melakukan polling ke API untuk mengecek status job

6. **Visualization**

   * Data ditampilkan dalam bentuk **map interaktif**
   * Setiap titik memiliki preview image hasil deteksi
   * Streamlit mengambil image via API dengan path file

---

## 🏗️ Arsitektur Project

```
streamlit (frontend)
   |
   | REST API
   v
api (FastAPI)
   |
   | background workers
   v
jobs/<job_id>/
   ├── frames/
   ├── gps/
   ├── metadata.json
   └── inference_result.json
```

---

## 📂 Struktur Repository

```
FINAL_PROJECT/
│
├── api/                    # Backend service (FastAPI)
│   ├── app.py              # Entry point API
│   ├── job_manager.py      # Job & lifecycle management
│   ├── workers.py          # Background workers (extract, combine, inference)
│   └── logger.py
│
├── engines/                # Data processing engine
│   ├── frame.py            # Video frame extraction
│   ├── gps.py              # GPX parsing & GPS extraction
│   └── combine.py          # Frame-GPS synchronization
│
├── src/                    # Model & inference logic
│   ├── inference.py        # YOLO bulk inference
│   ├── model_v1.py
│   └── model_v2.py         # HuggingFace-based model loader
│
├── streamlit/              # Frontend visualization
│   ├── pages/              # Multi-page Streamlit app
│   ├── components/         # Reusable UI components
│   │   ├── map_view.py
│   │   ├── frame_viewer.py
│   │   └── filters.py
│   └── services/api.py     # API client
│   └── main.py 
│
├── utils/                  # Utility functions
│   └── json_parser.py
│
├── jobs/                   # Generated per Job ID (runtime)
├── logs/                   # Service logs
│
├── requirements.txt
```

---

## ⚙️ Tech Stack

* **Backend**: FastAPI
* **Worker**: Background task (job-based)
* **Model**: YOLO (Hugging Face)
* **Frontend**: Streamlit
* **Mapping**: Streamlit Map / Folium
* **Deployment**: Local server + Ngrok

---

## 🚀 Cara Menjalankan Project

### 1️⃣ Setup Environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

### 2️⃣ Jalankan Backend Service

```bash
uvicorn api.app:app --host 0.0.0.0 --port 9000
```

Gunakan **ngrok** agar Streamlit bisa mengakses service:

```bash
ngrok http 9000
```

---

### 3️⃣ Jalankan Streamlit

```bash
streamlit run streamlit/main.py
```

---

## 📊 Output

* Map dengan marker pothole
* Preview image hasil deteksi
* Metadata berbasis Job ID

---

## 🧩 Konsep Desain Penting

* **Job-based processing** → scalable & aman untuk proses berat
* **Decoupled API & UI** → Streamlit hanya fokus visualisasi
* **File-based job storage** → mudah ditrack & debug
* **Model loading via HuggingFace** → ringan di local storage

---

## 📌 Catatan

* Folder `jobs/` dibuat otomatis per Job ID
* Folder ini menjadi *single source of truth* untuk Streamlit
* Sistem cocok untuk **research / prototype / thesis project**

---

## 👤 Author

**Muhammad Arif Budiman**
Project: *Road Pothole Detection & Mapping*

---

## ⭐ Future Improvement

* Queue system (Redis / Celery)
* Cloud worker deployment
* Auto clustering pothole area
* Dashboard analytics

---
