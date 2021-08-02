from flask import Flask
from flask import render_template
from service import processor
import logging
import logging.handlers
import os
import sys

handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger = logging.getLogger("application")
logger.setLevel(os.environ.get("LOGLEVEL", "INFO"))
logger.addHandler(handler)


def create_app():
    app = Flask(__name__)

    @app.before_first_request
    def read_files():
        processor.read_and_process_files()

    @app.route("/", methods=["GET"])
    def index():
        return render_template("index.html")

    return app


app = create_app()

if __name__ == "__main__":
    app = create_app()
    app.run(debug=False, port=80)
