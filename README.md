# Flask ML App

Live On--- https://cybershield-q34je.onrender.com 

Requirements:
- Python 3.8+
- Dependencies in requirements.txt:
  Flask
  joblib
  nltk
  google-generativeai
  python-dotenv
  gunicorn
  scikit-learn

---

Installation:
1. Clone repo:
   git clone <your-repo-url>
   cd <your-repo-folder>

2. (Optional) Create and activate virtual environment:
   python3 -m venv venv
   source venv/bin/activate    # Linux/macOS
   .\venv\Scripts\activate     # Windows

3. Install dependencies:
   pip install -r requirements.txt


---

Run locally:
- Flask dev server:
  flask run

- Gunicorn (production):
  gunicorn app:app

---

Deployment notes:
- Ensure gunicorn and scikit-learn are in requirements.txt
- Use `gunicorn app:app` as start command
- Include nmodel.pkl in deployment

---




