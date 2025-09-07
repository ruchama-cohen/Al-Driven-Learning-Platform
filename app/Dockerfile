# נשתמש ב-image רשמי של Python
FROM python:3.10

# נגדיר תיקיית עבודה
WORKDIR /app

# נעתיק את קבצי הדרישות
COPY requirements.txt .

# נתקין את הספריות
RUN pip install --no-cache-dir -r requirements.txt

# נעתיק את כל הקוד פנימה
COPY . .

# נריץ את FastAPI עם uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]