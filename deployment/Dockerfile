FROM python:3.14.9-slim-trixie@sha256:35caba83af2fe6da9a5d922f9b0156f21d1246a48278c58a08bd253303ba42e8

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY pipeline.bin .
COPY predict.py .

EXPOSE 9696
CMD ["uvicorn", "predict:app", "--host", "0.0.0.0", "--port", "9696"]

