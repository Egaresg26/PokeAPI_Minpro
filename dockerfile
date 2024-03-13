FROM python:latest

# Set working directory di dalam container
WORKDIR /app

# Install dependensi proyek
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install gunicorn
RUN pip install gunicorn

COPY . /app

CMD ["gunicorn", "-b", "0.0.0.0:8080", "run:app"]
