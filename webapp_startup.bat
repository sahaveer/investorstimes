@echo off
call C:\Users\sahaveer\PycharmProjects\webapp\Scripts\activate.bat

cd /d C:\Users\sahaveer\PycharmProjects\webapp\Scripts\investortimes

python -m streamlit run main.py

pause