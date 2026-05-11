# Receipt-to-Form AI Auto-Fill Web App

This is a simple AI-powered web app that extracts key information from a receipt image and auto-fills an editable form.

Built for the AI Intern Assessment.

## Features

- Upload a receipt image
- Extract receipt details using Gemini AI
- Auto-fill an editable form
- Extracted fields:
  - Merchant name
  - Date
  - Total amount
  - Currency
- Currency normalization:
  - `$` → `USD`
  - `RM` → `MYR`
  - `S$` → `SGD`
- Submit extracted data
- Download submitted data as JSON

## Tech Stack

- Python
- Streamlit
- Google Gemini API
- Pillow
- python-dotenv

## Model Used

The app uses:

gemini-2.5-flash

Prompt Used :
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
How to Run Locally

1. Clone the repository
git clone https://github.com/salmanariffin31-create/receipt-to-form-ai-autofill.git
cd receipt-to-form-ai-autofill

2. Create a virtual environment
python -m venv .venv

3. Activate the virtual environment

For Windows:

.\.venv\Scripts\Activate.ps1

4. Install dependencies
pip install -r requirements.txt

5. Create a .env file
Create a .env file in the project root and add:
GEMINI_API_KEY=your_gemini_api_key_here

6. Run the app
streamlit run app.py

Notes:
-The .env file is not uploaded to GitHub for security reasons.

-If the Gemini API is experiencing high demand, extraction may temporarily fail. Try again after a short while.

-The extracted form is editable, so users can correct the AI output before submitting.
