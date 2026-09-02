FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies separately to make better use of Docker layer caching.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy only the files required to run and test the solution.
COPY solution.py .
COPY test/ ./test/

# Run the application as a non-root user.
RUN useradd --create-home --uid 10001 appuser
USER appuser

CMD ["python", "solution.py"]