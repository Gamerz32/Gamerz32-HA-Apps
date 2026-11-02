FROM enricoflammini/eero-dashboard:latest

# Add Home Assistant Supervisor option and MQTT service handling around the
# upstream image. The upstream image is multi-architecture (amd64/arm64).
COPY launcher.py /ha-addon/launcher.py

ENTRYPOINT ["python3", "/ha-addon/launcher.py"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1", "--log-level", "info"]
