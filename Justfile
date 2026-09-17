setup:
    pip install -r requirements.txt
    cp .env.example .env
    mkdir -p driver/stable

install:
    pip install -r requirements.txt

run:
    python src/app.py
