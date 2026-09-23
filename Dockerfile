FROM ghcr.io/ismola/selenium-scraper-runtime:v0.2.3

USER root
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY --chown=scraper:scraper . .
RUN chmod +x /app/docker-entrypoint.sh
USER scraper

ENV BASE_URL=https://asismetro.org/ \
    BROWSER_LANGUAGE=es \
    SELENIUM_STEALTH=true \
    SELENIUM_FORCE_INTERACTABLE=true \
    PAGE_MAX_TIMEOUT=7 \
    PAGE_LOAD_TIMEOUT=120 \
    SCRIPT_TIMEOUT=60 \
    WEBDRIVER_COMMAND_TIMEOUT=120 \
    WEBDRIVER_MAX_LIFETIME=1800

EXPOSE 3000 9090
ENTRYPOINT ["/app/docker-entrypoint.sh"]
