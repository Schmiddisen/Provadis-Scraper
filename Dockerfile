# Dockerfile
FROM python:3.8-alpine

# Install necessary dependencies
RUN apk update && \
    apk add --no-cache \
    gcc \
    g++ \
    make \
    git \
    bash \
    linux-headers \
    libffi-dev \
    musl-dev \
    firefox \
    xvfb \
    py3-pip \
    firefox-esr \
    firefox-esr-bin \
    ttf-freefont \
    fontconfig \
    msttcorefonts-installer

# Install Python dependencies
COPY requirements.txt /app/Provadis-Scraper/requirements.txt
RUN pip install --upgrade pip && \
    pip install -r /app/Provadis-Scraper/requirements.txt

# Copy application code
COPY . /app/Provadis-Scraper
WORKDIR /app/Provadis-Scraper

# Make sure main.py and docker_main.py are executable
RUN chmod +x main.py docker_main.py

# Create a directory for the scrapped files
RUN mkdir -p /app/Provadis-Coach-Mirror

# Copy the .env file and export variables
COPY .env /app/Provadis-Scraper/.env
RUN set -o allexport; source /app/Provadis-Scraper/.env; set +o allexport

# Clone the private repository using PAT
RUN git init && \
git remote add origin https://$GIT_USERNAME:$GIT_PAT@$GIT_REPO && \
git pull origin master

# Run the docker_main.py script
CMD ["python", "docker_main.py"]
