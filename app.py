from flask import Flask
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "2023_May_15_19_57"

@app.route('/')
def home():
    return "Hello world"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))