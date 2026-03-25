# 🧾 Invoice Information Extraction

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32%2B-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![EasyOCR](https://img.shields.io/badge/EasyOCR-1.7-00C49A?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Tests](https://img.shields.io/badge/Tests-pytest-yellow?style=for-the-badge&logo=pytest)

> An end-to-end Streamlit application that extracts structured data from invoice images using **EasyOCR**, parses fields with regex, persists results in **MySQL**, and evaluates accuracy using **Levenshtein distance**.

---

## 📸 Demo

| Upload Image | Extracted Data | Accuracy Report |
|:---:|:---:|:---:|
| _Upload any JPG/PNG invoice_ | _Parsed into structured table_ | _Compare against ground truth_ |

---

## ✨ Features

- 📷 **Upload invoice images** — JPG, JPEG, PNG supported
- 🔍 **OCR extraction** — powered by EasyOCR with English language model
- 🧩 **Structured field parsing** — Invoice Number, Date, Products, Quantity, Rate, Value, CGST, SGST, Total GST
- 🗄️ **MySQL persistence** — data inserted via SQLAlchemy with auto table creation
- 📊 **Interactive DataFrame** — view all extracted fields in the browser
- ✅ **Accuracy evaluation** — Levenshtein distance + percentage accuracy vs ground truth

---

## 🏗️ Project Structure

```
invoice-ocr/
│
├── app.py                  # Streamlit entry point
│
├── src/
│   ├── config.py           # All config & env vars (no hardcoded secrets)
│   ├── ocr_engine.py       # EasyOCR image → text extraction
│   ├── parser.py           # Regex field parser → typed InvoiceData dataclass
│   ├── database.py         # SQLAlchemy DB operations (create table, insert)
│   └── accuracy.py         # Levenshtein distance & accuracy calculation
│
├── tests/
│   ├── test_parser.py      # Unit tests for invoice parser
│   └── test_accuracy.py    # Unit tests for accuracy module
│
├── .env.example            # Environment variable template
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🔄 Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Streamlit UI (app.py)                   │
└───────────────┬─────────────────────────────────────────────┘
                │
        ┌───────▼────────┐
        │  ocr_engine.py │  ← PIL opens image → EasyOCR reads text
        └───────┬────────┘
                │  raw text string
        ┌───────▼────────┐
        │   parser.py    │  ← Regex extracts invoice fields
        └───────┬────────┘
                │  InvoiceData dataclass
       ┌────────┴────────┐
       │                 │
┌──────▼──────┐   ┌──────▼──────┐
│ database.py │   │ accuracy.py │
│  (MySQL)    │   │ (Levenshtein│
└─────────────┘   └─────────────┘
```

---

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone https://github.com/Saravananb91/text-extraction-from-bills.git
cd invoice-ocr
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` with your MySQL credentials:

```env
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_NAME=invoice_db
```

### 5. Run the app

```bash
streamlit run app.py
```

---

## 🧪 Running Tests

```bash
pytest tests/ -v
```

Expected output:
```
tests/test_parser.py::TestParseInvoice::test_invoice_number_extracted  PASSED
tests/test_parser.py::TestParseInvoice::test_products_extracted        PASSED
tests/test_accuracy.py::TestCalculateAccuracy::test_identical_strings  PASSED
...
```

---

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| streamlit | ≥1.32 | Web UI |
| easyocr | ≥1.7.1 | OCR engine |
| Pillow | ≥10.0 | Image loading |
| pandas | ≥2.0 | Data manipulation |
| sqlalchemy | ≥2.0 | ORM / DB engine |
| pymysql | ≥1.1 | MySQL driver |
| editdistance | ≥0.6.3 | Levenshtein distance |
| python-dotenv | ≥1.0 | Env var loading |
| pytest | ≥8.0 | Testing |

---

## 🔮 Roadmap

- [ ] PDF invoice support
- [ ] Multi-language OCR
- [ ] Batch upload (multiple invoices at once)
- [ ] Export to Excel / CSV
- [ ] Docker containerization
- [ ] REST API endpoint (FastAPI)

---

## 🔐 Security Notes

> ⚠️ Never commit your `.env` file. It is already listed in `.gitignore`.  
> Use environment variables or a secrets manager (AWS Secrets Manager, HashiCorp Vault) in production.

---

## 👤 Author

Saravanan B - [mrsaravananb@gmail.com ](mrsaravananb@gmail.com)

Project Link: [https://github.com/Saravananb91/road-pothole-](https://github.com/Saravananb91/road-pothole-)

Portfolio website : [portfolio-saravananb.vercel.app](portfolio-saravananb.vercel.app ) 

Linkedin: [www.linkedin.com/in/saravanan-b-46244b290](www.linkedin.com/in/saravanan-b-46244b290)
---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
