# CyberShield 🛡️🤖

Live On--- https://cybershield-q3je.onrender.com 


**Protecting Digital Spaces with AI – Stopping Cyberbullying**

## 🌟 Overview

CyberShield is an AI-powered tool designed to detect and prevent cyberbullying using **machine learning models**, **natural language processing (NLP)**, and a **Flask-based web service**.
By analyzing online conversations, CyberShield helps create a safer digital environment.

## ✨ Features

✔️ **AI-driven cyberbullying detection** using NLP models
✔️ **Flask-based web service** for API integration
✔️ **Interactive Web Interface** for analysis and insights
✔️ **Google Gemini AI-powered conclusions** for better contextual assessment

## 🛠️ Tech Stack

🔹 **Jupyter Notebook** – Model development & experimentation
🔹 **HTML** – Web interface for user interaction
🔹**Python 3.8+** – Core programming language
🔹 **Flask** – Web framework for API deployment
🔹 **ML Models (NLP-based)** – Detect toxic speech and cyberbullying

## 📦 Dependencies

CyberShield requires the following dependencies (found in `requirements.txt`):
🔹 Flask
🔹 joblib
🔹 nltk
🔹 google-generativeai
🔹 python-dotenv
🔹 gunicorn
🔹 scikit-learn

## ⚙️ Installation

### 🔽 Step 1: Clone the Repository

```sh
git clone <your-repo-url>
cd cybershield
```

### 🔽 Step 2: Set Up a Virtual Environment (Optional)

```
### Linux/macOS 🐧🍏
python3 -m venv venv
source venv/bin/activate

### Windows 🏁
python3 -m venv venv
.\venv\Scripts\activate
```

### 📌 Step 3: Install Dependencie

```
pip install -r requirements.txt
```

## 🚀 Usage

🔹 Start the Flask server to serve the AI-powered detection API.

```
python app.py
```

🔹 Submit comments for toxicity analysis using the /predict endpoint.
🔹 Generate AI-powered conclusions using the /conclude endpoint.
🔹 Integrate the API into existing platforms to enhance online safety.

## 🚀 Docker Installation & Setup
This project, CyberShield, can be containerized using Docker. Follow the steps below to build and run it.

### 📦 Build the Docker Image
Run the following command in the root of the project (where the Dockerfile is located):


docker build -t mpawank/cybershield:latest .

### ▶️ Run the Container

docker run -p 5000:5000 mpawank/cybershield:latest

Your Flask app will be available at: http://localhost:5000


## 👑 Project Owner

Built with 💡, 💻, and ❤️ by:

## [MpawanK](https://github.com/mpawank)

--🚀 Visionary behind CyberShield

--🔧 Developer • Designer • Defender of Digital Spaces

--📬 Connect: [GitHub](https://github.com/mpawank) | [LinkedIn](https://www.linkedin.com/in/m-pawan-kumar-b3978424b/)

"Building tools that protect, empower, and inspire safer online communities."

## 🤝 Contributing

We’re actively looking for contributors to help make the UI mobile responsive.
If you’re passionate about UX/UI, feel free to submit a pull request!

## ⭐ Star the repo and spread the word!

## 👥 Contributors

Thanks to all the amazing contributors helping make CyberShield better!<br> <br>
<a href="https://github.com/denshaw-09/contribute-Cybershield" target="_blank" rel="noopener noreferrer" style="text-decoration:none; text-align:center; display:inline-block;">
  <img src="https://github.com/denshaw-09.png" width="60" alt="denshaw-09 GitHub Avatar" style="border-radius:50%;" />
  <br />
  <sub>
    <b>denshaw-09</b>
  </sub>
</a>
