# CyberShield

Live On--- https://cybershield-q3je.onrender.com 


**Protecting Digital Spaces with AI – Stopping Cyberbullying**

## Overview

CyberShield is an AI-powered tool designed to detect and prevent cyberbullying using **machine learning models**, **natural language processing (NLP)**, and a **Flask-based web service**. 
By analyzing online conversations, CyberShield helps create a safer digital environment.

## Features

- **AI-driven cyberbullying detection** using NLP models
- **Flask-based web service** for API integration
- **Interactive Web Interface** for analysis and insights
- **Google Gemini AI-powered conclusions** for better contextual assessment

## Tech Stack

- **Jupyter Notebook** – Model development & experimentation
- **HTML** – Web interface for user interaction
- **Python 3.8+** – Core programming language
- **Flask** – Web framework for API deployment
- **ML Models (NLP-based)** – Detect toxic speech and cyberbullying

## Dependencies

CyberShield requires the following dependencies (found in `requirements.txt`):
- Flask
- joblib
- nltk
- google-generativeai
- python-dotenv
- gunicorn
- scikit-learn

## Installation

### Step 1: Clone the Repository
```sh
git clone <your-repo-url>
cd cybershield

## Set Up a Virtual Environment (Optional)

### Linux/macOS
python3 -m venv venv
source venv/bin/activate

### Windows
python3 -m venv venv
.\venv\Scripts\activate

## Install Dependencies
pip install -r requirements.txt

## Usage
- Start the Flask server to serve the AI-powered detection API.
python app.py

- Submit comments for toxicity analysis using the /predict endpoint.
- Generate AI-powered conclusions using the /conclude endpoint.
- Integrate the API into existing platforms to enhance online safety.

## Deployment

For production deployment, follow these steps:
- Ensure gunicorn and scikit-learn are listed in requirements.txt.
- Use Gunicorn to serve the application:
gunicorn app:app

- Include nmodel.pkl in your deployment to ensure the ML model is loaded correctly.

## Contribution

We welcome contributions! To contribute:
- Fork the repository
- Create a new branch (git checkout -b feature-name)
- Commit changes (git commit -m "Added new feature")
- Push to the branch (git push origin feature-name)
- Open a Pull Request
