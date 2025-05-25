from builder import create_app
from flask import send_from_directory
import os
import logging
from logging.handlers import RotatingFileHandler
from services.prometheus_metrics import setup_prometheus

config_class = os.environ.get("CONFIG_CLASS", "config.DatabaseConfig")
app = create_app(config_class)


@app.route("/storage/images/<path:filename>")
def get_image(filename):
    return send_from_directory("/app/storage/images", filename)


# Configuração do logger para logs de acesso
access_handler = RotatingFileHandler("access.log", maxBytes=0, backupCount=1)
access_handler.setLevel(logging.INFO)
access_formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s"
)
access_handler.setFormatter(access_formatter)
app.logger.addHandler(access_handler)

app.logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler = RotatingFileHandler("app.log", maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)

app.logger.addHandler(handler)
setup_prometheus(app)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 80))
    app.run(host="0.0.0.0", port=port, debug=False)
