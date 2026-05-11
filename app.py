import streamlit as st
from PIL import Image
from dotenv import load_dotenv
from google import genai
import os
import json
import csv
import io
 
load_dotenv()
 
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
 
# Initialize session state
if "receipt_data" not in st.session_state:
    st.session_state["receipt_data"] = None
 
if "history" not in st.session_state:
    st.session_state["history"] = []
 
# Header
st.markdown(
    """
    <div style="text-align: center; padding: 20px 0;">
        <h1>🧾 Receipt AI Extractor</h1>
        <p style="font-size: 18px; color: gray;">
            Upload a receipt image or use your camera and let Gemini AI auto-fill the form.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
 
st.divider()
 
 
# Currency normalization
def normalize_currency(currency):
    currency = currency.strip().upper()
    mapping = {
        "$": "USD",
        "USD": "USD",
        "US$": "USD",
        "RM": "MYR",
        "MYR": "MYR",
        "S$": "SGD",
        "SGD": "SGD",
        "€": "EUR",
        "EUR": "EUR",
        "£": "GBP",
        "GBP": "GBP"
    }
    return mapping.get(currency, currency)
 
 
def extract_from_image(image):
    prompt = """
Extract the following fields from this receipt image:
 
- merchant_name
- date
- total_amount
- currency
 
Return ONLY valid JSON in this exact format:
 
{
  "merchant_name": "",
  "date": "",
  "total_amount": "",
  "currency": ""
}
 
If a field is unclear or missing, use an empty string.
"""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[prompt, image]
    )
 
    result_text = response.text.strip()
 
    if result_text.startswith("```json"):
        result_text = result_text.replace("```json", "").replace("```", "").strip()
    elif result_text.startswith("```"):
        result_text = result_text.replace("```", "").strip()
 
    data = json.loads(result_text)
    data["currency"] = normalize_currency(data.get("currency", ""))
    return data
 
 
# Input tabs — upload or camera
tab1, tab2 = st.tabs(["📁 Upload Image", "📷 Use Camera"])
 
image = None
 
with tab1:
    uploaded_file = st.file_uploader(
        "Upload receipt image",
        type=["png", "jpg", "jpeg"]
    )
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Receipt", use_container_width=True)
 
with tab2:
    camera_photo = st.camera_input("Take a photo of your receipt")
    if camera_photo:
        image = Image.open(camera_photo)
        st.image(image, caption="Captured Receipt", use_container_width=True)
 
# Extract button
if image:
    if st.button("✨ Extract Receipt Details"):
        with st.spinner("Gemini AI is extracting receipt details..."):
            try:
                data = extract_from_image(image)
                st.session_state["receipt_data"] = data
            except Exception as e:
                st.error("AI extraction failed. Gemini may currently be experiencing high demand.")
                st.write(e)
                st.stop()
 
# Form
if st.session_state["receipt_data"]:
 
    data = st.session_state["receipt_data"]
 
    st.divider()
    st.markdown("### 📋 Extracted Receipt Details")
    st.caption("Review and edit the extracted fields before submitting.")
 
    merchant_name = st.text_input("Merchant Name", value=data.get("merchant_name", ""))
    date = st.text_input("Date", value=data.get("date", ""))
    total_amount = st.text_input("Total Amount", value=data.get("total_amount", ""))
    currency = st.text_input("Currency", value=data.get("currency", ""))
 
    submitted_data = {
        "merchant_name": merchant_name,
        "date": date,
        "total_amount": total_amount,
        "currency": currency
    }
 
    if st.button("✅ Submit"):
 
        # Add to history
        st.session_state["history"].append(submitted_data)
 
        st.success("Receipt submitted successfully!")
        st.json(submitted_data)
 
        # Download JSON
        st.download_button(
            label="⬇ Download as JSON",
            data=json.dumps(submitted_data, indent=4),
            file_name="receipt_data.json",
            mime="application/json"
        )
 
        # Download CSV
        csv_buffer = io.StringIO()
        writer = csv.DictWriter(csv_buffer, fieldnames=submitted_data.keys())
        writer.writeheader()
        writer.writerow(submitted_data)
        st.download_button(
            label="⬇ Download as CSV",
            data=csv_buffer.getvalue(),
            file_name="receipt_data.csv",
            mime="text/csv"
        )
 
else:
    st.info("Upload a receipt image or use your camera, then click 'Extract Receipt Details'.")
 
 
# Receipt history
if st.session_state["history"]:
 
    st.divider()
    st.markdown("### 🗂 Receipt History")
    st.caption("All receipts submitted in this session.")
 
    st.dataframe(
        st.session_state["history"],
        use_container_width=True
    )
 
    # Export full history as CSV
    csv_buffer = io.StringIO()
    writer = csv.DictWriter(csv_buffer, fieldnames=["merchant_name", "date", "total_amount", "currency"])
    writer.writeheader()
    writer.writerows(st.session_state["history"])
 
    st.download_button(
        label="⬇ Export Full History as CSV",
        data=csv_buffer.getvalue(),
        file_name="receipt_history.csv",
        mime="text/csv"
    )