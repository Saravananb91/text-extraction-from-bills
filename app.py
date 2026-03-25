"""
app.py
------
Streamlit entry point for the Invoice Information Extraction app.
Run with:  streamlit run app.py
"""

import streamlit as st

from src.ocr_engine import extract_text_from_bytes
from src.parser    import parse_invoice
from src.database  import save_invoice, invoice_to_dataframe
from src.accuracy  import calculate_accuracy
from src.config    import APP_TITLE, SUPPORTED_TYPES

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🧾",
    layout="wide",
)

st.title(f"🧾 {APP_TITLE}")
st.markdown(
    "Upload an invoice image to extract structured data using OCR, "
    "store it in MySQL, and evaluate extraction accuracy."
)
st.divider()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Settings")
    save_to_db = st.toggle("Save extracted data to database", value=True)
    st.caption("Configure DB credentials in your `.env` file.")

# ── File upload ───────────────────────────────────────────────────────────────
uploaded_file = st.file_uploader(
    "📤 Upload Invoice Image",
    type=SUPPORTED_TYPES,
    help="Supported formats: JPG, JPEG, PNG",
)

if uploaded_file is None:
    st.info("Upload an invoice image to get started.")
    st.stop()

# ── Process ───────────────────────────────────────────────────────────────────
col_img, col_text = st.columns([1, 1])

with col_img:
    st.subheader("📸 Uploaded Image")
    st.image(uploaded_file, use_column_width=True)

with st.spinner("🔍 Running OCR…"):
    image_bytes   = uploaded_file.read()
    extracted_text = extract_text_from_bytes(image_bytes)

with col_text:
    st.subheader("📄 Extracted Text")
    st.text_area("Raw OCR output", extracted_text, height=300, label_visibility="collapsed")

st.divider()

# ── Parse ─────────────────────────────────────────────────────────────────────
invoice = parse_invoice(extracted_text)

if not invoice.is_valid():
    st.warning(
        "⚠️ Could not detect invoice number or date. "
        "The image may not be a supported invoice format."
    )

# Invoice header metrics
st.subheader("📋 Invoice Summary")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Invoice Number",   invoice.invoice_number   or "—")
m2.metric("Invoice Date",     invoice.invoice_date     or "—")
m3.metric("CGST Amount",      invoice.cgst_amount      or "—")
m4.metric("Total GST Amount", invoice.total_gst_amount or "—")

# Product line table
st.subheader("🛒 Product Lines")
df = invoice_to_dataframe(invoice)
if df.empty:
    st.warning("No product lines were detected in this invoice.")
else:
    st.dataframe(df, use_container_width=True)

st.divider()

# ── Database save ─────────────────────────────────────────────────────────────
if save_to_db:
    with st.spinner("💾 Saving to database…"):
        success, message = save_invoice(invoice)
    if success:
        st.success(message)
    else:
        st.error(message)

# ── Accuracy evaluation ───────────────────────────────────────────────────────
st.subheader("✅ Accuracy Evaluation (Optional)")
st.markdown(
    "Paste the correct text from the invoice below to compare "
    "it against the OCR output and get an accuracy score."
)

ground_truth = st.text_area(
    "Ground truth text",
    placeholder="Paste the actual invoice text here…",
    height=150,
)

if ground_truth.strip():
    result = calculate_accuracy(ground_truth.strip(), extracted_text)
    a1, a2 = st.columns(2)
    a1.metric("Levenshtein Distance", result["distance"])
    a2.metric("OCR Accuracy",         f"{result['accuracy']}%")

    if result["accuracy"] >= 90:
        st.success("🟢 Excellent extraction quality!")
    elif result["accuracy"] >= 70:
        st.warning("🟡 Moderate quality — consider a higher-resolution image.")
    else:
        st.error("🔴 Low accuracy — the image may be blurry or poorly lit.")
