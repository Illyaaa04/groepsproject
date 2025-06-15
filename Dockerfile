FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Maak noodzakelijke directories aan
RUN mkdir -p /app/instance /app/certs

# ✅ Voeg dit toe zodat Python de 'app' module vindt
ENV PYTHONPATH=/app

EXPOSE 5000

CMD ["python", "start.py"]
