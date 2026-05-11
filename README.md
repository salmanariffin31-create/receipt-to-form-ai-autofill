# Receipt-to-Form AI Auto-Fill Web App

An AI-powered web app that extracts key information from a receipt image and auto-fills an editable form.

Built for the **AI Intern Assessment — TP Malaysia Innovation Team**.

---

## Features

- Upload a receipt image (PNG, JPG, JPEG)
- Gemini AI extracts receipt fields automatically
- Auto-fills an editable form for review and correction
- Currency normalization (e.g. `RM` → `MYR`, `$` → `USD`, `S$` → `SGD`)
- Submit extracted data
- Download submitted data as JSON

### Extracted fields

| Field | Description |
|---|---|
| `merchant_name` | Store or restaurant name |
| `date` | Date as printed on the receipt |
| `total_amount` | Numeric total (no currency symbol) |
| `currency` | ISO 4217 code (MYR, USD, SGD, etc.) |

---

## Tech Stack

- Python
- Streamlit
- Google Gemini API
- Pillow
- python-dotenv

---

## Why Gemini?

This app uses **Google Gemini 2.5 Flash** as the AI model. Claude (Anthropic) and ChatGPT (OpenAI) both require a paid API subscription to access their vision/image capabilities. Gemini was chosen because it offers a **free tier** that supports image input, making it accessible for this assessment without any cost barrier.

---

## Model & Prompt Used

**Model:** `gemini-2.5-flash`

**Prompt:**

```
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
```

---

## How to Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/salmanariffin31-create/receipt-to-form-ai-autofill.git
cd receipt-to-form-ai-autofill
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

Windows:

```bash
.\.venv\Scripts\Activate.ps1
```

macOS / Linux:

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Create a `.env` file

```
GEMINI_API_KEY=your_gemini_api_key_here
```

### 6. Run the app

```bash
streamlit run app.py
```

---

## Notes

- The `.env` file is not committed to GitHub for security reasons.
- The extracted form is fully editable before submitting, so users can correct any AI errors.
- If the Gemini API is under high demand, extraction may temporarily fail — retry after a moment.
