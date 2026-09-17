# Student Placement Data Collection System

Module 1 of “An Advanced Machine Learning Approach for Student Placement Prediction and Analysis”.

39 attributes are collected through a web form and stored in SQLite. Records can be viewed and exported as CSV for Module 2.

## Windows PowerShell
py -3.11 -m venv venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m uvicorn app.main:app --reload

Open http://127.0.0.1:8000
Docs: http://127.0.0.1:8000/docs
