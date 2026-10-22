FROM python:3.12-slim

WORKDIR /app
COPY minidb.py main.py ./

CMD ["python", "main.py"]
