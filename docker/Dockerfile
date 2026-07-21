FROM python:3.13-slim
WORKDIR /app
COPY main.py main.py
RUN pip install "fastapi[standard]"
CMD ["fastapi", "dev", "--host", "0.0.0.0"]