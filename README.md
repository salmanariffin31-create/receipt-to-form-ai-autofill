# Receipt AI Extractor

An AI-powered web app that extracts key information from a receipt image and auto-fills an editable form. Built with Flask and the Google Gemini API, deployed on Vercel.

Built for the **AI Intern Assessment — TP Malaysia Innovation Team**.

---

## Features

- Upload a receipt image (PNG, JPG, WEBP)
- Gemini AI extracts receipt fields automatically
- Auto-fills an editable form for review
- Currency normalization (e.g. `RM` → `MYR`, `$` → `USD`)
- Submit and download extracted data as JSON

### Extracted fields

| Field | Description |
|---|---|
| `merchant_name` | Store or restaurant name |
| `date` | Date as printed on the receipt |
| `total_amount` | Numeric total (no currency symbol) |
| `currency` | ISO 4217 code (MYR, USD, SGD, etc.) |

---

## Tech stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| AI | Google Gemini 2.5 Flash |
| Frontend | HTML, CSS, Vanilla JS |
| Deployment | Vercel |

---

## Model & prompt used

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

## Project structure

```
receipt-app/
├── api/
│   └── index.py          # Flask app (Vercel serverless entry point)
├── templates/
│   └── index.html        # Frontend UI
├── requirements.txt
├── vercel.json
├── .env.example
├── .gitignore
└── README.md
```

---

## How to run locally

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/receipt-ai-extractor.git
cd receipt-ai-extractor
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv

# Windows
.\.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your API key

Create a `.env` file in the project root:

```
GEMINI_API_KEY=your_gemini_api_key_here
```

### 5. Run the app

```bash
python api/index.py
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

---

## How to deploy on Vercel

### 1. Push your repo to GitHub

Make sure `.env` is in `.gitignore` — never commit your API key.

### 2. Import the repo on Vercel

Go to [vercel.com](https://vercel.com) → **Add New Project** → import your GitHub repo.

### 3. Add environment variable

In the Vercel project dashboard:  
**Settings → Environment Variables → Add**

```
Name:  GEMINI_API_KEY
Value: your_gemini_api_key_here
```

### 4. Deploy

Click **Deploy**. Vercel will detect `vercel.json` and deploy the Flask app as a serverless function automatically.

---
## Deployment

The app is deployed on **Streamlit Community Cloud**.

[View the live app here]([https://your-app-name.streamlit.app](https://receipt-to-form-ai-autofill-xttsb7seuqs5c82wkz6erh.streamlit.app/))

### Why not Vercel?

Vercel only supports static sites and serverless functions — it does not support persistent Python servers. Streamlit requires a running server process to handle state and re-renders, which makes it incompatible with Vercel's deployment model. Streamlit Community Cloud was chosen as it is purpose-built for Streamlit apps, offers free hosting, and deploys directly from a GitHub repository with no extra configuration needed.

## Notes

- The `.env` file is never committed to GitHub.
- The extracted form is fully editable before submitting.
- If Gemini is under high demand, the extraction may fail — retry after a moment.
## Notes

- The `.env` file is not committed to GitHub for security reasons.
- The extracted form is fully editable before submitting, so users can correct any AI errors.
- If the Gemini API is under high demand, extraction may temporarily fail — retry after a moment.
