FROM python:3.12-slim

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files
COPY requirements.txt .

# Install dependencies
RUN uv pip install --system --no-cache -r requirements.txt

# Copy project
COPY . .

# Download HF dataset (optional, for local development)
# RUN python -c "from datasets import load_dataset; load_dataset('NoeFlandre/herero-dataset')"

CMD ["python", "-m", "pytest", "tests/", "-v"]
