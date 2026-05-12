# Receipt-to-Form AI Auto-Fill Web App

An AI-powered web app that extracts key information from a receipt image and auto-fills an editable form.  
Built for the AI Intern Assessment — TP Malaysia Innovation Team.

## 🔗 Live Demo
👉 Open the live app here

## Features

- Upload a receipt image or snap one using your camera directly.
- Gemini AI extracts receipt fields automatically.
- Auto-fills an editable form for review and correction.
- Currency normalization (e.g. RM → MYR, $ → USD, S$ → SGD).
- Submit and download extracted data as JSON or CSV.
- Session-based receipt history table with full CSV export.

## Extracted Fields

| Field            | Description                                       |
|------------------|---------------------------------------------------|
| `merchant_name`  | Store or restaurant name                          |
| `date`           | Date as printed on the receipt                    |
| `total_amount`   | Numeric total (no currency symbol)                |
| `currency`       | ISO 4217 code (MYR, USD, SGD, etc.)               |

## Tech Stack

| Layer            | Technology                   |
|------------------|------------------------------|
| Language         | Python                       |
| Framework        | Streamlit                    |
| AI Model         | Google Gemini 2.5 Flash      |
| Image Processing | Pillow                       |
| Deployment       | Streamlit Community Cloud    |

## Why Gemini?

This app uses **Google Gemini 2.5 Flash** as the AI model.  
Both Claude (Anthropic) and ChatGPT (OpenAI) require a paid API subscription for image capabilities. Gemini was chosen because it offers a free tier that supports image input, making it accessible for this assessment without any cost barrier.

## Model & Prompt Used

- **Model**: `gemini-2.5-flash`
- **Prompt**: 
  Extract the following fields from this receipt image:
  
  - `merchant_name`
  - `date`
  - `total_amount`
  - `currency`
  
  Return ONLY valid JSON in this exact format:
  
  ```json
  {
    "merchant_name": "",
    "date": "",
    "total_amount": "",
    "currency": ""
  }
