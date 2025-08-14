FROM ubuntu:25.10

# Install dependencies
RUN apt-get update && apt-get install -y \
    python3-dev \
    gcc \
    python3-venv \
    curl \
    unzip

COPY requirements.txt .

# Install packages with CodeArtifact as additional index
RUN python3 -m venv alethiomics
RUN alethiomics/bin/pip3 install -r requirements.txt

# Activate the virtual environment by default
ENV PATH="/alethiomics/bin:$PATH"