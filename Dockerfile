FROM python:3.11

ENV PYTHONUNBUFFERED 1

WORKDIR /api

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade && pip install -r requirements.txt

EXPOSE 8000

COPY . .

HEALTHCHECK CMD ["curl", "--fail", "http://localhost:8000", "||", "exit 1"]

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]