# Use official slim Python image
FROM python:3.10-slim
WORKDIR /usr/src/app

# Install system dependencies for psycopg2 and osqp
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    python3-dev \
    build-essential \
    cmake \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy project code
COPY ./app ./app
COPY alembic.ini ./alembic.ini
COPY ./alembic ./alembic

# Expose port and run
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]