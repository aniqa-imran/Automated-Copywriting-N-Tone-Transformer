# ⚡ Automated Copywriting & Tone Transformer

An enterprise-grade, dual-pipeline Generative AI content orchestration engine built with Python, Streamlit, Google Gemini API, and Pydantic. 

Developed as part of the **DecodeLab Generative AI Engineering Internship (Project 2)**.

---

## 📌 Table of Contents
- [Project Overview](#-project-overview)
- [Key Features](#-key-features)
- [Project Architecture](#-project-architecture)
- [Prerequisites](#-prerequisites)
- [Installation & Setup](#-installation--setup)
- [How to Run the Project](#-how-to-run-the-project)
  - [1. Running the Web UI (Streamlit)](#1-running-the-web-ui-streamlit)
  - [2. Running via Command Line (CLI)](#2-running-via-command-line-cli)
  - [3. Bulk CSV Batch Processing](#3-bulk-csv-batch-processing)
- [Inference Parameter Tuning Guide](#-inference-parameter-tuning-guide)
- [Troubleshooting Common Issues](#-troubleshooting-common-issues)
- [License](#-license)

---

## 📌 Project Overview

The **Automated Copywriting & Tone Transformer** transforms raw product descriptions into structured, high-converting marketing copy tailored for platforms like LinkedIn, Instagram, Email, and Twitter/X.

Rather than relying on basic text prompting, this engine implements:
1. **Dynamic Prompt Compilation:** Injects target variables securely using master f-string templates.
2. **Pydantic Validation:** Enforces strict structural output (Headline, Body, CTA, Hashtags).
3. **Asynchronous Execution:** Handles single and batch requests concurrently using `asyncio` and `Semaphore` rate-limiting.
4. **Resilience Engineering:** Integrates `tenacity` retry logic to guard against API rate limits and network drops.

---

## ✨ Key Features

- **Modern Enterprise Dark UI:** Responsive Streamlit interface with dynamic layout styling.
- **Pydantic Schema Enforcement:** Guarantees standard JSON structure across all model outputs.
- **Dual Pipeline Execution:** Real-time single-prompt processing & bulk dataset generation.
- **CLI Argparse Support:** Flexible command-line flags including custom prefix operators (`--tone`, `+a`).
- **Resilience Shield:** Automatic exponential backoff retries on API rate limits.

---

## 📂 Project Architecture

```text
Tone_transformer/
│
├── .env                # Secret environment variables (GEMINI_API_KEY)
├── .gitignore          # Prevents pushing .env and cached files to GitHub
├── requirements.txt    # Project Python dependencies
├── schemas.py          # Pydantic data schemas for output validation
├── engine.py           # Gemini API logic, prompt templates, & async runner
├── app.py              # Streamlit Web Dashboard application
├── main.py             # CLI entry point using argparse
└── README.md           # Documentation
📋 Prerequisites
Make sure you have the following installed on your machine:

Python: Version 3.10 or higher

Git: Installed on your system

Google Gemini API Key: Get your key from Google AI Studio

🚀 Installation & Setup
Step 1: Clone the Repository

git clone https://github.com/aniqa-imran/Automated-Copywriting-N-Tone-Transformer
Step 2: Create a Virtual Environment (Optional but Recommended)
Bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
Step 3: Install Required Dependencies
Bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
Step 4: Configure API Key
Create a .env file in the root directory:

Bash
# Windows PowerShell
New-Item -ItemType File .env

# Mac/Linux
touch .env
Open .env in VS Code and paste your Gemini API Key:

Code snippet
GEMINI_API_KEY=your_actual_gemini_api_key_here
💻 How to Run the Project
1. Running the Web UI (Streamlit)
To launch the interactive dashboard in your browser:

Bash
python -m streamlit run app.py
The browser will automatically open at http://localhost:8501.

2. Running via Command Line (CLI)
To run generation directly from your terminal without opening the UI:

Bash
python main.py --product "Zenith Earbuds" --desc "Active noise cancellation with 40-hour battery life" --platform "LinkedIn" --tone "Professional" --temp 0.7
CLI Flags Available:

--product (Required): Name of the product

--desc (Required): Raw features and description

--platform (Optional): Target platform (LinkedIn, Instagram, Email, Twitter) [Default: LinkedIn]

--tone (Optional): Desired tone (Professional, Witty & Casual, Urgent, Technical) [Default: Professional]

--temp (Optional): Model temperature from 0.0 to 1.0 [Default: 0.7]

3. Bulk CSV Batch Processing
Prepare a CSV file with headers: product_name, description, platform, tone.

Open the Streamlit App (python -m streamlit run app.py).

Select "Bulk Batch Processing" from the sidebar menu.

Upload your CSV and click "Run Bulk Engine".

Download the final generated dataset as a CSV.

⚙️ Inference Parameter Tuning Guide
Temperature (0.0 – 1.0):

0.2 (Low): Best for structured, factual, and corporate emails.

0.8 (High): Ideal for creative, witty, and viral social media posts.

Semaphore Gate Limit (1 – 10):

Controls the max number of concurrent API requests to avoid rate limiting during bulk processing.

🛠️ Troubleshooting Common Issues
Issue 1: streamlit: The term 'streamlit' is not recognized...

Solution: Always run Streamlit through the Python module runner:

Bash
python -m streamlit run app.py
Issue 2: GEMINI_API_KEY environment variable not detected

Solution: Ensure your .env file exists in the main Tone_transformer folder and contains GEMINI_API_KEY=....

📜 License
Distributed under the MIT License. Built for portfolio and educational purposes for DecodeLab.
