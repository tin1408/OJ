FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    gcc \
    g++ \
    make \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    gettext \
    curl \
    pkg-config \
    libmariadb-dev-compat \
    libmariadb-dev \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js 18
RUN curl -sL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Copy and prepare entrypoint
COPY entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["entrypoint.sh"]
