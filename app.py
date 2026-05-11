import streamlit as st
from PIL import Image
from dotenv import load_dotenv
from google import genai
import os
import json

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Better UI
st.markdown(
    """
    <div style="text-align: center; padding: 20px 0;">
        <h1>🧾 Receipt AI Extractor</h1>
        <p style="font-size: 18px; color: gray;">
            Upload a receipt image and let Gemini AI auto-fill the form.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()

st.title("🧾 Receipt-to-Form Auto-Fill Web App")

st.write(
    "Upload a receipt image and Gemini AI will extract the receipt details automatically."
)

uploaded_file = st.file_uploader(
    "Upload receipt image",
    type=["png", "jpg", "jpeg"]
)

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

if uploaded_file:

    image = Image.open(uploaded_file)

    st.image(
        image,
        caption="Uploaded Receipt",
        use_container_width=True
    )

    if st.button("Extract Receipt Details"):

        with st.spinner("Gemini AI is extracting receipt details..."):

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

            try:

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[prompt, image]
                )

                result_text = response.text.strip()

                # Remove markdown formatting if Gemini adds it
                if result_text.startswith("```json"):
                    result_text = result_text.replace("```json", "").replace("```", "").strip()

                elif result_text.startswith("```"):
                    result_text = result_text.replace("```", "").strip()

                data = json.loads(result_text)

                # Normalize currency
                data["currency"] = normalize_currency(
                    data.get("currency", "")
                )

                st.session_state["receipt_data"] = data

            except Exception as e:

                st.error(
                    "AI extraction failed. Gemini may currently be experiencing high demand."
                )

                st.write(e)

                st.stop()

if "receipt_data" in st.session_state:

    data = st.session_state["receipt_data"]

    st.markdown("### 📋 Extracted Receipt Details")
    st.caption("Review and edit the extracted fields before submitting.")

    merchant_name = st.text_input(
        "Merchant Name",
        value=data.get("merchant_name", "")
    )

    date = st.text_input(
        "Date",
        value=data.get("date", "")
    )

    total_amount = st.text_input(
        "Total Amount",
        value=data.get("total_amount", "")
    )

    currency = st.text_input(
        "Currency",
        value=data.get("currency", "")
    )

    submitted_data = {
        "merchant_name": merchant_name,
        "date": date,
        "total_amount": total_amount,
        "currency": currency
    }

    if st.button("Submit"):

        st.success("Receipt submitted successfully!")

        st.json(submitted_data)

        # Download JSON feature
        st.download_button(
            label="⬇ Download Extracted Data (JSON)",
            data=json.dumps(submitted_data, indent=4),
            file_name="receipt_data.json",
            mime="application/json"
        )

else:

    st.info("Upload a receipt and click 'Extract Receipt Details'.")