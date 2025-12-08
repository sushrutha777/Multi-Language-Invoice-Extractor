# 🧾 Multi-Language Invoice Q&A System Using Gemini

A simple Streamlit app where you can upload an invoice (PDF or image) and ask questions about it in **English or any languages Suported by Gemini**.  
The system converts PDF pages into images and uses **Gemini 2.5 Pro** (multimodal) to understand the invoice — **no separate OCR required**.

## 🚀 Features

- Upload PDF / JPG / PNG invoices
- PDF pages automatically converted to images
- Powered by Gemini-2.5-flash which natively understands text inside images
- Works perfectly with **English + any languages Suported by Gemini** (Hindi, Tamil, Telugu, Bengali, Gujarati, etc.)
- Extract totals, invoice number, GST, items, dates, vendor details, etc.
- Clean and intuitive Streamlit UI

## 📦 Installation and Setup

1. Clone this repository (or download the files):
   ```bash
   git clone https://github.com/sushrutha777/Multi-Language-Invoice-Extractor.git
   cd multi-language-invoice-extractor
2. Create Virtual Environment:
   ```bash
    python -m venv venv
   .\venv\Scripts\activate
3. Install the required dependencies:
   ```bash
    pip install -r requirements.txt
4. Create a .env file in the project root and add your Google Gemini API key:
   ```bash
    GOOGLE_API_KEY=your_api_key_here
5. Run the Streamlit app:
   ```bash
    streamlit run app.py
