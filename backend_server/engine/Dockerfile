FROM python:3.14-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

WORKDIR /app/src

EXPOSE 5000

CMD ["python", "-m", "gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "--access-logfile", "log/access.log", "--error-logfile", "log/error.log", "main.communication.komunikacja:app"]
