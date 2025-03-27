FROM python:3.9

WORKDIR /app

COPY . /app

RUN pip uninstall -y elasticsearch

RUN pip install "elasticsearch<8.0.0" fastapi uvicorn

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
