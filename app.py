import os
from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
import requests
from config import ACCESS_TOKEN, PHONE_NUMBER_ID, API_VERSION

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Set upload folder and ensure it exists
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # ✅ Ensures 'uploads/' exists
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        message = request.form["message"]

        if file.filename.endswith(".csv"):
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)

            df = pd.read_csv(filepath)
            for number in df["phone"]:
                send_message(number, message)

            flash("Messages sent successfully!", "success")
            return redirect(url_for("index"))
        else:
            flash("Only CSV files are allowed!", "danger")
            return redirect(url_for("index"))

    return render_template("index.html")

def send_message(phone_number, message):
    url = f"https://graph.facebook.com/{API_VERSION}/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": str(phone_number),
        "type": "text",
        "text": {"body": message}
    }
    response = requests.post(url, headers=headers, json=payload)
    print(response.status_code, response.text)

if __name__ == "__main__":
    app.run(debug=True)
